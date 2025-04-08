# TradeLite Pro - Backend Deployment Guide

This guide provides detailed instructions for deploying the TradeLite Pro backend to Render using Docker.

## Prerequisites

- GitHub repository with the TradeLite Pro code
- Render account
- API keys for Supabase, DeepSeek, and OpenAI

## Deployment Steps

1. **Push code to GitHub**
   - Ensure your code is pushed to GitHub following the frontend deployment instructions

2. **Create a Render Web Service**
   - Log in to your Render account
   - Click "New" and select "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - Name: tradelite-pro-backend
     - Environment: Docker
     - Branch: main
     - Root Directory: / (or specify the backend directory if needed)
   - Add the following environment variables:
     - SUPABASE_URL
     - SUPABASE_KEY
     - DEEPSEEK_API_KEY
     - OPENAI_API_KEY
     - REDIS_URL (Render will provide a Redis instance URL if you create one)
   - Click "Create Web Service"

3. **Create a Render Redis Instance (Optional)**
   - In Render dashboard, click "New" and select "Redis"
   - Configure your Redis instance
   - Once created, copy the internal URL to use as REDIS_URL environment variable

4. **Verify Deployment**
   - Once deployed, Render will provide a URL for your backend API
   - Test the API by visiting `https://your-backend-url.onrender.com/docs`
   - Update your frontend configuration with the new backend URL

## Docker Configuration

The backend is configured with Docker for easy deployment:

- **Dockerfile**: Defines the container environment for the FastAPI backend
- **docker-compose.yml**: Sets up both the backend and Redis services for local development
- **requirements.txt**: Lists all Python dependencies

## Troubleshooting

- Check Render logs if deployment fails
- Verify all environment variables are correctly set
- Ensure the Dockerfile is in the root directory of your repository
- Make sure all API keys are valid

## Local Docker Testing

To test the Docker setup locally before deployment:

```bash
docker-compose up
```

This will start both the backend and Redis services locally.
