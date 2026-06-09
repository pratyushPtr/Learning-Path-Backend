# Import FastAPI framework for building the web application
from fastapi import FastAPI

# Import the router for the generate learning path functionality
from routes.generate import router as generate_router

# Import the service for configuring the Gemini LLM API
from services.gemini import configure_gemini

# Import dotenv module for loading environment variables from .env file
from dotenv import load_dotenv

# Import the router for the quiz functionality
from routes.quiz import router as quiz_router

# Import os module for accessing environment variables
import os

# Load environment variables from the .env file
load_dotenv()

# Create a FastAPI application instance with title "Learning Path Generator"
app = FastAPI(title="Learning Path Generator")

# Configure the Gemini LLM API with the API key from environment variables
configure_gemini(api_key = os.getenv("LLM_API_KEY"))

# Include the generate router in the application
app.include_router(generate_router)

# Include the quiz router in the application
app.include_router(quiz_router)

# Define a GET endpoint at /health path for health check
@app.get("/health")

# Define the health check function
def health_check():

    # Return a JSON response with status "ok"
    return {"status": "ok"}
