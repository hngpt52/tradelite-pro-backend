from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
import random
import time
import uuid
from app.schemas.schemas import SimulationCreate, SimulationResult, SimulationDataPoint
from app.db.supabase import get_supabase_client
from app.db.redis import get_redis_client

router = APIRouter()

# Helper function to generate mock simulation data
def generate_mock_data(asset: str, strategy: str, timeframe: int, initial_capital: float) -> SimulationResult:
    """
    Generate mock simulation data for educational purposes
    """
    # Generate unique ID
    sim_id = str(uuid.uuid4())
    
    # Mock user ID
    user_id = "mock-user-id"
    
    # Generate price data with random walk
    data = []
    start_price = 100
    if asset == "BTC":
        start_price = 30000
        volatility = 0.03
    elif asset == "ETH":
        start_price = 2000
        volatility = 0.04
    else:
        start_price = 100
        volatility = 0.02
    
    current_price = start_price
    
    for i in range(timeframe):
        # Random walk price model with some volatility
        change = current_price * volatility * (random.random() - 0.5)
        current_price = max(current_price + change, 0.1)  # Ensure price doesn't go negative
        
        # Calculate indicators based on strategy
        sma20 = None
        ema10 = None
        
        if i >= 19:
            # Calculate SMA for last 20 days
            sma_prices = [data[j].price for j in range(i-19, i)]
            sma20 = sum(sma_prices) / 20
        
        if i >= 9:
            # Calculate EMA for last 10 days
            ema_prices = [data[j].price for j in range(i-9, i)]
            ema10 = sum(ema_prices) / 10
        
        data.append(SimulationDataPoint(
            day=i+1,
            price=round(current_price, 2),
            sma20=round(sma20, 2) if sma20 is not None else None,
            ema10=round(ema10, 2) if ema10 is not None else None
        ))
    
    # Calculate final capital and ROI based on strategy performance
    strategy_performance = {
        "sma_crossover": random.uniform(-0.1, 0.3),
        "ema_crossover": random.uniform(-0.05, 0.25),
        "macd": random.uniform(-0.15, 0.35),
        "rsi": random.uniform(-0.2, 0.4),
        "bollinger": random.uniform(-0.1, 0.3)
    }
    
    performance = strategy_performance.get(strategy, 0.1)
    final_capital = initial_capital * (1 + performance)
    roi = performance * 100
    
    # Create simulation result
    result = SimulationResult(
        id=sim_id,
        user_id=user_id,
        asset=asset,
        strategy=strategy,
        timeframe=timeframe,
        initial_capital=initial_capital,
        final_capital=round(final_capital, 2),
        roi=round(roi, 2),
        data=data,
        created_at=time.strftime("%Y-%m-%d %H:%M:%S")
    )
    
    return result

@router.post("/", response_model=SimulationResult)
async def create_simulation(
    simulation: SimulationCreate,
    supabase=Depends(get_supabase_client),
    redis=Depends(get_redis_client)
):
    """
    Create a new simulation
    """
    try:
        # Generate simulation data
        result = generate_mock_data(
            asset=simulation.asset,
            strategy=simulation.strategy,
            timeframe=simulation.timeframe,
            initial_capital=simulation.initial_capital
        )
        
        # In a real implementation, we would store this in Supabase
        # For now, we'll just cache it in Redis
        redis.setex(
            f"simulation:{result.id}",
            3600,  # Cache for 1 hour
            result.json()
        )
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{simulation_id}", response_model=SimulationResult)
async def get_simulation(
    simulation_id: str,
    redis=Depends(get_redis_client)
):
    """
    Get simulation by ID
    """
    try:
        # Try to get from Redis cache
        cached_simulation = redis.get(f"simulation:{simulation_id}")
        
        if cached_simulation:
            return SimulationResult.parse_raw(cached_simulation)
        
        # If not in cache, return 404
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Simulation not found"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/", response_model=List[SimulationResult])
async def list_simulations(
    limit: Optional[int] = 10,
    offset: Optional[int] = 0
):
    """
    List simulations (mock implementation)
    """
    # In a real implementation, we would fetch from Supabase
    # For now, return mock data
    mock_simulations = [
        generate_mock_data(
            asset=random.choice(["BTC", "ETH", "AAPL", "MSFT", "TSLA"]),
            strategy=random.choice(["sma_crossover", "ema_crossover", "macd", "rsi", "bollinger"]),
            timeframe=random.choice([7, 14, 30, 60, 90]),
            initial_capital=10000.0
        )
        for _ in range(min(limit, 5))  # Limit to 5 for mock data
    ]
    
    return mock_simulations
