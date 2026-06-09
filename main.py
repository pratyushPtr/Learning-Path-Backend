# Import the os module for accessing environment variables
import os

# Import FastAPI framework for building the web application
from fastapi import FastAPI

# Import dotenv loader to read environment variables from .env file
from dotenv import load_dotenv

# Import the generate router from routes module
from routes.generate import router as generate_router

# Import the quiz router from routes module
from routes.quiz import router as quiz_router

# Import the configure_gemini function from services module
from services.gemini import configure_gemini

# Load environment variables from the .env file
load_dotenv()

# Create a FastAPI application instance
app = FastAPI(title="Learning Path Generator")

# Configure the Gemini LLM API with safety check
llm_api_key = os.getenv("LLM_API_KEY")
if not llm_api_key:
    raise ValueError("LLM_API_KEY environment variable is missing. Please set it in your .env file.")
configure_gemini(api_key=llm_api_key)

# Include the application routers
app.include_router(generate_router)
app.include_router(quiz_router)

# Define a GET endpoint for health check
@app.get("/health", tags=["System Health"])
def health_check():
    return {"status": "ok"}
