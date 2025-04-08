from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.schemas import (
    SentimentAnalysisRequest, SentimentAnalysisResponse,
    AnomalyDetectionRequest, AnomalyDetectionResponse,
    EducationalFeedbackRequest, EducationalFeedbackResponse
)
from app.services.ai_service import get_educational_feedback
from app.services.sentiment_analysis_service import analyze_sentiment
from app.services.anomaly_detection_service import detect_anomalies
from app.db.redis import get_redis_client
import json

router = APIRouter()

@router.post("/sentiment", response_model=SentimentAnalysisResponse)
async def sentiment_analysis(
    request: SentimentAnalysisRequest,
    redis=Depends(get_redis_client)
):
    """
    Analyze sentiment of financial text
    """
    try:
        # Check cache first
        cache_key = f"sentiment:{hash(request.text)}"
        cached_result = redis.get(cache_key)
        
        if cached_result:
            return SentimentAnalysisResponse.parse_raw(cached_result)
        
        # Perform sentiment analysis
        result = analyze_sentiment(request.text)
        
        # Cache result
        redis.setex(
            cache_key,
            3600,  # Cache for 1 hour
            result.json()
        )
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/anomalies", response_model=AnomalyDetectionResponse)
async def anomaly_detection(
    request: AnomalyDetectionRequest,
    redis=Depends(get_redis_client)
):
    """
    Detect anomalies in time series data
    """
    try:
        # Check cache first
        cache_key = f"anomalies:{hash(json.dumps(request.data))}-{request.window_size}"
        cached_result = redis.get(cache_key)
        
        if cached_result:
            return AnomalyDetectionResponse.parse_raw(cached_result)
        
        # Perform anomaly detection
        result = detect_anomalies(request.data, request.window_size)
        
        # Cache result
        redis.setex(
            cache_key,
            3600,  # Cache for 1 hour
            result.json()
        )
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/feedback", response_model=EducationalFeedbackResponse)
async def educational_feedback(
    request: EducationalFeedbackRequest,
    redis=Depends(get_redis_client)
):
    """
    Generate AI-powered educational feedback for trading simulations
    """
    try:
        # Check cache first
        cache_key = f"feedback:{request.asset}-{request.strategy}-{request.timeframe}"
        cached_result = redis.get(cache_key)
        
        if cached_result:
            return EducationalFeedbackResponse.parse_raw(cached_result)
        
        # Generate educational feedback
        result = get_educational_feedback(
            asset=request.asset,
            strategy=request.strategy,
            timeframe=request.timeframe,
            performance=request.performance
        )
        
        # Cache result
        redis.setex(
            cache_key,
            3600,  # Cache for 1 hour
            result.json()
        )
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
