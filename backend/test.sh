#!/bin/bash

# Local Development Testing Script
# Tests the backend locally before deployment

set -e

echo "=========================================="
echo "Local Development Test"
echo "=========================================="

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the server
echo "Starting server on http://localhost:8080..."
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
