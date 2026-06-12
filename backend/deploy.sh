#!/bin/bash

# Learning Path Generator - Google Cloud Deployment Script
# This script deploys your backend to Google Cloud Run

set -e

# Configuration
PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-your-project-id}"
REGION="${GOOGLE_CLOUD_REGION:-us-central1}"
SERVICE_NAME="learning-path-generator"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "=========================================="
echo "Learning Path Generator Deployment"
echo "=========================================="
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"
echo "Image: $IMAGE_NAME"
echo "=========================================="

# Step 1: Build Docker image
echo ""
echo "Step 1: Building Docker image..."
gcloud builds submit --tag "$IMAGE_NAME" --platform container

# Step 2: Deploy to Cloud Run
echo ""
echo "Step 2: Deploying to Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
  --image "$IMAGE_NAME" \
  --platform managed \
  --region "$REGION" \
  --allow-unauthenticated \
  --set-env-vars=GEMINI_API_KEY=$GEMINI_API_KEY \
  --set-env-vars=REDIS_URL=$REDIS_URL \
  --set-env-vars=CACHE_TTL_SECONDS=$CACHE_TTL_SECONDS \
  --min-instances=1 \
  --timeout 300s

# Step 3: Verify deployment
echo ""
echo "Step 3: Verifying deployment..."
sleep 10
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --region "$REGION" --format="value(status.url)")
echo "Service URL: $SERVICE_URL"

# Step 4: Test health endpoint
echo ""
echo "Step 4: Testing health endpoint..."
curl -s "$SERVICE_URL/health" | python3 -m json.tool

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo "Your service is now running at: $SERVICE_URL"
echo ""
echo "To update the service, run this script again with updated env vars."
echo "To scale the service, use: gcloud run services scale $SERVICE_NAME --region $REGION --min-instances=3"
