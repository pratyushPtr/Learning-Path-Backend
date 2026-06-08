from fastapi import FastAPI
from routes.generate import router as generate_router
from services.gemini import configure_gemini
from dotenv import load_dotenv
from routes.quiz import router as quiz_router
import os

load_dotenv()

app = FastAPI(title="Learning Path Generator")

configure_gemini(api_key = os.getenv("LLM_API_KEY"))

app.include_router(generate_router)
app.include_router(quiz_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}


