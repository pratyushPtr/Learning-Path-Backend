🧭 Learning Path Generator — Backend
An AI-powered backend that generates personalized, structured learning roadmaps based on your goal, experience level, and available time. Built with FastAPI and Google Gemini AI.

🚀 What It Does

Takes a learning goal, experience level, and weekly hours as input
Uses Gemini AI to generate a 12-week structured learning path
Returns clean, structured JSON with weekly milestones, resources, and checkpoints
Generates milestone quizzes with multiple choice and open-ended questions
Grades quiz submissions with per-question feedback and an overall score


🛠️ Tech Stack

Python 3.11+
FastAPI — web framework
Google Gemini AI (google-genai) — AI backend
Uvicorn — ASGI server
Pydantic — data validation
python-dotenv — environment variable management


📁 Project Structure
learning-path-generator/
├── main.py               # App entry point
├── requirements.txt      # Dependencies
├── .env                  # API key (create this yourself — see below)
├── .gitignore
├── models/
│   └── schemas.py        # Pydantic data models
├── routes/
│   ├── generate.py       # /generate endpoint
│   ├── quiz.py           # /quiz endpoints
│   └── health.py         # /health endpoint
└── services/
    └── gemini.py         # Gemini AI logic

⚙️ Setup Instructions
1. Clone the Repository
bashgit clone https://github.com/pratyushPtr/Learning-Path-Backend.git
cd Learning-Path-Backend
2. Create a Virtual Environment (Recommended)
bashpython -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
3. Install Dependencies
bashpip install -r requirements.txt
4. Get a Gemini API Key

Go to aistudio.google.com
Sign in with Google
Click "Get API Key" → Create a new key
Copy it

5. Create Your .env File
In the project root, create a file named .env (no extension) with:
LLM_API_KEY=your_gemini_api_key_here

⚠️ Never share this file or commit it to GitHub. It is already in .gitignore.

6. Run the Server
bashuvicorn main:app --reload
The server will start at http://127.0.0.1:8000

📖 API Endpoints
Once running, open Swagger UI at:
http://127.0.0.1:8000/docs
GET /health
Check if the server is running.
Response:
json{ "status": "ok" }

POST /generate
Generate a personalized 12-week learning path.
Request Body:
json{
  "goal": "Learn Python",
  "experience_level": "beginner",
  "hours_per_week": 5
}
Response:
json{
  "goal": "Learn Python",
  "experience_level": "beginner",
  "hours_per_week": 5,
  "total_weeks": 12,
  "weeks": [
    {
      "week": 1,
      "milestone": "...",
      "resources": ["...", "..."],
      "checkpoint": "..."
    }
  ]
}

POST /quiz/generate
Generate a quiz for a specific week's milestone.
Request Body:
json{
  "milestone": "Understanding Python Variables and Data Types",
  "week_number": 1
}
Response: Returns 3 multiple choice + 2 open-ended questions.

POST /quiz/submit
Submit quiz answers and receive graded feedback.
Request Body: Pass the original questions back along with answers:
json{
  "week_number": 1,
  "milestone": "Understanding Python Variables and Data Types",
  "questions": [...],
  "answers": [
    { "question_number": 1, "answer": "A" },
    { "question_number": 2, "answer": "B" },
    { "question_number": 4, "answer": "A variable stores data that can change." }
  ]
}
Response:
json{
  "week_number": 1,
  "score": 4,
  "total": 5,
  "passed": true,
  "feedback": [...],
  "overall_feedback": "Great understanding of the basics!"
}

🧪 Testing the API
The easiest way is through Swagger UI at http://127.0.0.1:8000/docs:

Click an endpoint
Click "Try it out"
Fill in the request body
Click "Execute"


📦 Requirements
If requirements.txt is missing any packages, install manually:
bashpip install fastapi uvicorn google-genai python-dotenv

👥 Team
RoleResponsibilityAI EngineerLLM integration, FastAPI backend, prompt engineeringAI Project ManagerProject planning, timeline, coordinationAI AnalystResearch, output evaluation, improvementAI Data EngineerDatabase, progress tracking, data persistenceEthical AI AnalystBias review, responsible AI practices

📌 Notes for Team Members

The .env file is not included in the repo — you must create your own with your own Gemini API key
Always run pip install -r requirements.txt after pulling new changes
Use --reload flag during development so the server auto-restarts on file changes
All AI logic lives in services/gemini.py — that's the core file
