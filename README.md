# Learning Path Generator API 🚀

An intelligent, production-ready backend API that utilizes FastAPI and local LLM integration (via Ollama) to generate highly structured, dynamically personalized 3-step learning roadmaps. 

The API accepts user constraints—such as learning goals, current tech background, skill levels, and weekly time commitments—and uses strict Pydantic parsing schemas to ensure clean JSON responses.

---

## 🛠️ Tech Stack
* **Framework:** FastAPI (Python)
* **LLM Engine:** Ollama (Mistral / Gemini Integration)
* **Data Validation:** Pydantic v2
* **Server:** Uvicorn

---

## 🚀 Getting Started

Follow these step-by-step instructions to get your local development environment up and running.

### 1. Prerequisites
Make sure you have Python 3.11+ installed on your machine. You will also need **Ollama** installed and running locally.
* Download Ollama: [ollama.com](https://ollama.com)
* Pull the required model in your main system terminal:
  ```bash
  ollama run mistral
