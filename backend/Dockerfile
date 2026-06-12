# Use an official lightweight Python runtime
FROM python:3.11-slim

# Set system environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed for compiling certain python packages if necessary
RUN apt-get update && apt-get install -y --no-install-recommends gcc g++ && rm -rf /lib/apt/lists/*

# Copy requirements or install core dependencies directly
RUN pip install --no-cache-dir fastapi uvicorn google-genai pydantic redis python-dotenv

# Copy the rest of your local backend application code into the container
COPY . /app

# Expose port 8080 for Cloud Run traffic routing
EXPOSE 8080

# Command to run the application using uvicorn
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
