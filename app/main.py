from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, simulations, ai

app = FastAPI(
    title="TradeLite Pro API",
    description="Backend API for TradeLite Pro educational trading platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(simulations.router, prefix="/api/simulations", tags=["Simulations"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])

@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint for health check
    """
    return {"status": "ok", "message": "TradeLite Pro API is running"}

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "version": "1.0.0"}
