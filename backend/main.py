import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

# Import your custom modules
from services import cache, llm_client
from routes import quiz

# Set up logging format for Cloud Run logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PathCraft API",
    description="Production backend service for streaming AI-generated learning paths",
    version="1.0.0"
)

# =====================================================================
# CORS Configuration (Allows frontend to talk securely to backend)
# =====================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",                            # Local development
        "https://gen-lang-client-0112839296.web.app",       # Production Firebase Domain
        "https://gen-lang-client-0112839296.firebaseapp.com" # Production Firebase Backup
    ],
    allow_credentials=True,
    allow_methods=["*"],                                    # Allow GET, POST, OPTIONS, etc.
    allow_headers=["*"],                                    # Allow all headers (Content-Type, Authorization, etc.)
)

# Register routers
app.include_router(quiz.router)

# =====================================================================
# Pydantic Schemas for Request & Response validation
# =====================================================================
class RoadmapRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=100, description="The skill or domain to generate a path for")
    experience_level: str = Field("Beginner", description="User's current profile level (Beginner, Intermediate, Advanced)")
    weekly_hours: int = Field(15, ge=1, le=100, description="Weekly hours dedicated to study")

class Milestone(BaseModel):
    title: str
    description: str
    estimated_weeks: int
    key_topics: List[str]

class RoadmapResponse(BaseModel):
    topic: str
    experience_level: str
    total_estimated_weeks: int
    milestones: List[Milestone]

# =====================================================================
# API Endpoints
# =====================================================================

@app.get("/health", tags=["System"])
def health_check():
    """
    Cloud Run service startup health probe string.
    Ensures container is live and capable of listening on port 8080.
    """
    return {"status": "ok"}


@app.post("/api/generate-roadmap", response_model=RoadmapResponse, tags=["Core AI"])
def generate_roadmap(request: RoadmapRequest):
    """
    Fetches an optimized structured learning path blueprint.
    Checks Upstash Redis cache first before falling back to Gemini 2.5 Flash.
    """
    logger.info("Received roadmap request for topic: '%s' (%s)", request.topic, request.experience_level)

    # 1. Construct a deterministic caching key based on request parameters
    cache_key = cache.make_key(
        prefix="roadmap",
        topic=request.topic.strip().lower(),
        level=request.experience_level.strip().lower(),
        hours=request.weekly_hours
    )

    # 2. Check the Upstash Redis active cache
    try:
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info("Serving roadmap from Upstash Redis cache hit.")
            return cached_data
    except Exception as e:
        logger.warning("Bypassing cache read due to exception: %s", e)

    # 3. Cache Miss — Fall back to calling Gemini using structured data outputs
    num_weeks = max(4, min(24, round(180 / request.weekly_hours)))
    prompt = (
        f"Create an optimized structured learning roadmap to master the following topic: '{request.topic}'.\n"
        f"Target User Experience Level: {request.experience_level}.\n"
        f"Time Allocation Available: {request.weekly_hours} hours per week.\n"
        f"Generate exactly {num_weeks} weekly milestones, one per week, each with estimated_weeks set to 1. Each milestone should represent one focused week of learning."
    )

    try:
        logger.info("Cache miss. Querying Gemini API structure ecosystem...")
        # Call the resilient, runtime-validated client helper
        roadmap_json = llm_client._call_gemini_structured(
            prompt=prompt,
            response_schema=RoadmapResponse
        )
    except llm_client.LLMError as le:
        logger.error("Core AI model processing error: %s", le)
        raise HTTPException(status_code=502, detail=f"AI model service failure: {str(le)}")
    except Exception as e:
        logger.critical("Unhandled generation error: %s", e)
        raise HTTPException(status_code=500, detail="Internal processing error generation loop failure.")

    # 4. Asynchronously commit the clean result back to the Upstash Redis ring
    try:
        cache.set(cache_key, roadmap_json)
        logger.info("Successfully populated Upstash Redis cache for key: %s", cache_key)
    except Exception as e:
        logger.warning("Failed to save generation output to cache layer: %s", e)

    return roadmap_json