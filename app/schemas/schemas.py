from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any

# Authentication schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Simulation schemas
class SimulationCreate(BaseModel):
    asset: str
    strategy: str
    timeframe: int
    initial_capital: float = 10000.0

class SimulationDataPoint(BaseModel):
    day: int
    price: float
    sma20: Optional[float] = None
    ema10: Optional[float] = None

class SimulationResult(BaseModel):
    id: str
    user_id: str
    asset: str
    strategy: str
    timeframe: int
    initial_capital: float
    final_capital: float
    roi: float
    data: List[SimulationDataPoint]
    created_at: str

# AI schemas
class SentimentAnalysisRequest(BaseModel):
    text: str

class SentimentAnalysisResponse(BaseModel):
    sentiment: str
    score: float
    explanation: str

class AnomalyDetectionRequest(BaseModel):
    data: List[float]
    window_size: int = 20

class AnomalyDetectionResponse(BaseModel):
    anomalies: List[int]
    scores: List[float]
    threshold: float

class EducationalFeedbackRequest(BaseModel):
    asset: str
    strategy: str
    timeframe: int
    performance: Dict[str, Any]

class EducationalFeedbackResponse(BaseModel):
    feedback: str
    key_points: List[str]
    improvement_suggestions: List[str]
