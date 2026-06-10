import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes.generate import router as generate_router
from routes.quiz import router as quiz_router
from services.gemini import configure_gemini

# Load environment variables from the .env file
load_dotenv()

# Create a FastAPI application instance
app = FastAPI(title="Learning Path Generator")

# Configure CORS Middleware to allow cross-origin requests from your React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows your Vite React app to connect safely
    allow_credentials=True,
    allow_methods=["*"],  # Allows OPTIONS, POST, GET, etc.
    allow_headers=["*"],
)

# Configure the Gemini LLM API with safety check
llm_api_key = os.getenv("LLM_API_KEY")
if not llm_api_key:
    raise ValueError("LLM_API_KEY environment variable is missing. Please set it in your .env file.")
configure_gemini(api_key=llm_api_key)

# Include the application routers
app.include_router(generate_router)
app.include_router(quiz_router)

@app.get("/health", tags=["System Health"])
def health_check():
    return {"status": "ok"}