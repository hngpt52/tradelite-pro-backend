import openai
import random
from app.core.config import settings
from app.schemas.schemas import EducationalFeedbackResponse

# Configure OpenAI API
openai.api_key = settings.OPENAI_API_KEY

# Configure DeepSeek API (using OpenAI client with custom base URL)
deepseek_client = openai.OpenAI(
    api_key=settings.DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

def get_educational_feedback(asset: str, strategy: str, timeframe: int, performance: dict) -> EducationalFeedbackResponse:
    """
    Generate AI-powered educational feedback for trading simulations
    
    This function tries to use DeepSeek API first, then falls back to OpenAI,
    and finally uses a template-based approach if both APIs fail.
    """
    try:
        # Try DeepSeek API first
        if settings.DEEPSEEK_API_KEY:
            try:
                return _get_deepseek_feedback(asset, strategy, timeframe, performance)
            except Exception as e:
                print(f"DeepSeek API error: {str(e)}")
                # Fall through to OpenAI
        
        # Try OpenAI API next
        if settings.OPENAI_API_KEY:
            try:
                return _get_openai_feedback(asset, strategy, timeframe, performance)
            except Exception as e:
                print(f"OpenAI API error: {str(e)}")
                # Fall through to template
        
        # Fallback to template-based feedback
        return _get_template_feedback(asset, strategy, timeframe, performance)
    
    except Exception as e:
        # Final fallback
        print(f"Error generating feedback: {str(e)}")
        return EducationalFeedbackResponse(
            feedback="Unable to generate feedback at this time. Please try again later.",
            key_points=["System is currently experiencing issues."],
            improvement_suggestions=["Please try again later."]
        )

def _get_deepseek_feedback(asset: str, strategy: str, timeframe: int, performance: dict) -> EducationalFeedbackResponse:
    """Generate feedback using DeepSeek API"""
    
    # Format the strategy name for better readability
    strategy_name = {
        "sma_crossover": "Simple Moving Average Crossover",
        "ema_crossover": "Exponential Moving Average Crossover",
        "macd": "Moving Average Convergence Divergence (MACD)",
        "rsi": "Relative Strength Index (RSI)",
        "bollinger": "Bollinger Bands"
    }.get(strategy, strategy)
    
    # Create prompt for DeepSeek
    prompt = f"""
    Generate educational feedback for a trading simulation with the following parameters:
    - Asset: {asset}
    - Strategy: {strategy_name}
    - Timeframe: {timeframe} days
    - Performance: ROI of {performance.get('roi', 'unknown')}%, Final capital: ${performance.get('final_capital', 'unknown')}
    
    Provide detailed educational feedback explaining how this strategy works, what factors might have influenced the performance,
    and what the user could learn from this simulation. Include key points and improvement suggestions.
    
    Format the response as:
    1. Detailed feedback paragraph
    2. List of 3-5 key points
    3. List of 2-3 improvement suggestions
    
    Remember this is for educational purposes only and not financial advice.
    """
    
    # Call DeepSeek API
    response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are an educational assistant for trading simulations."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    # Parse response
    content = response.choices[0].message.content
    
    # Extract sections (simple parsing)
    sections = content.split("\n\n")
    feedback = sections[0] if len(sections) > 0 else ""
    
    # Extract key points and suggestions
    key_points = []
    improvement_suggestions = []
    
    for section in sections:
        if "key point" in section.lower():
            points = [p.strip("- ") for p in section.split("\n")[1:] if p.strip()]
            key_points.extend(points)
        elif "improvement" in section.lower() or "suggestion" in section.lower():
            suggestions = [s.strip("- ") for s in section.split("\n")[1:] if s.strip()]
            improvement_suggestions.extend(suggestions)
    
    # Ensure we have some content
    if not key_points:
        key_points = ["Understanding market trends", "Risk management is essential", "Past performance is not indicative of future results"]
    
    if not improvement_suggestions:
        improvement_suggestions = ["Consider backtesting with different parameters", "Combine with other indicators for confirmation"]
    
    return EducationalFeedbackResponse(
        feedback=feedback,
        key_points=key_points[:5],  # Limit to 5 key points
        improvement_suggestions=improvement_suggestions[:3]  # Limit to 3 suggestions
    )

def _get_openai_feedback(asset: str, strategy: str, timeframe: int, performance: dict) -> EducationalFeedbackResponse:
    """Generate feedback using OpenAI API"""
    
    # Format the strategy name for better readability
    strategy_name = {
        "sma_crossover": "Simple Moving Average Crossover",
        "ema_crossover": "Exponential Moving Average Crossover",
        "macd": "Moving Average Convergence Divergence (MACD)",
        "rsi": "Relative Strength Index (RSI)",
        "bollinger": "Bollinger Bands"
    }.get(strategy, strategy)
    
    # Create prompt for OpenAI
    prompt = f"""
    Generate educational feedback for a trading simulation with the following parameters:
    - Asset: {asset}
    - Strategy: {strategy_name}
    - Timeframe: {timeframe} days
    - Performance: ROI of {performance.get('roi', 'unknown')}%, Final capital: ${performance.get('final_capital', 'unknown')}
    
    Provide detailed educational feedback explaining how this strategy works, what factors might have influenced the performance,
    and what the user could learn from this simulation. Include key points and improvement suggestions.
    
    Format the response as:
    1. Detailed feedback paragraph
    2. List of 3-5 key points
    3. List of 2-3 improvement suggestions
    
    Remember this is for educational purposes only and not financial advice.
    """
    
    # Call OpenAI API
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an educational assistant for trading simulations."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    # Parse response
    content = response.choices[0].message.content
    
    # Extract sections (simple parsing)
    sections = content.split("\n\n")
    feedback = sections[0] if len(sections) > 0 else ""
    
    # Extract key points and suggestions
    key_points = []
    improvement_suggestions = []
    
    for section in sections:
        if "key point" in section.lower():
            points = [p.strip("- ") for p in section.split("\n")[1:] if p.strip()]
            key_points.extend(points)
        elif "improvement" in section.lower() or "suggestion" in section.lower():
            suggestions = [s.strip("- ") for s in section.split("\n")[1:] if s.strip()]
            improvement_suggestions.extend(suggestions)
    
    # Ensure we have some content
    if not key_points:
        key_points = ["Understanding market trends", "Risk management is essential", "Past performance is not indicative of future results"]
    
    if not improvement_suggestions:
        improvement_suggestions = ["Consider backtesting with different parameters", "Combine with other indicators for confirmation"]
    
    return EducationalFeedbackResponse(
        feedback=feedback,
        key_points=key_points[:5],  # Limit to 5 key points
        improvement_suggestions=improvement_suggestions[:3]  # Limit to 3 suggestions
    )

def _get_template_feedback(asset: str, strategy: str, timeframe: int, performance: dict) -> EducationalFeedbackResponse:
    """Generate template-based feedback when APIs are unavailable"""
    
    # Format the strategy name for better readability
    strategy_name = {
        "sma_crossover": "Simple Moving Average Crossover",
        "ema_crossover": "Exponential Moving Average Crossover",
        "macd": "Moving Average Convergence Divergence (MACD)",
        "rsi": "Relative Strength Index (RSI)",
        "bollinger": "Bollinger Bands"
    }.get(strategy, strategy)
    
    # Template feedback based on strategy
    strategy_templates = {
        "sma_crossover": {
            "feedback": f"This simulation demonstrates a Simple Moving Average (SMA) Crossover strategy applied to {asset} over {timeframe} days. The strategy involves tracking two moving averages - typically a short-term and long-term SMA - and generating buy signals when the short-term SMA crosses above the long-term SMA, and sell signals when it crosses below. This strategy aims to identify trend changes and can be effective in trending markets, but may generate false signals in sideways or highly volatile markets.",
            "key_points": [
                "SMA Crossover strategies work best in trending markets",
                "The choice of SMA periods significantly impacts performance",
                "This strategy typically lags behind price movements due to the nature of moving averages",
                "False signals are common during sideways market conditions"
            ],
            "improvement_suggestions": [
                "Consider adding a confirmation indicator like volume or RSI",
                "Test different SMA period combinations to optimize for your asset",
                "Implement a stop-loss strategy to manage downside risk"
            ]
        },
        "ema_crossover": {
            "feedback": f"This simulation demonstrates an Exponential Moving Average (EMA) Crossover strategy applied to {asset} over {timeframe} days. EMA crossover strategies are similar to SMA crossovers but give more weight to recent price data, making them more responsive to new information. The strategy generates buy signals when a shorter-term EMA crosses above a longer-term EMA, and sell signals when it crosses below. EMA crossovers can respond faster to trend changes than SMA crossovers, but this responsiveness can also lead to more false signals in volatile markets.",
            "key_points": [
                "EMA Crossover strategies respond faster to price changes than SMA strategies",
                "The strategy is more sensitive to recent price movements",
                "While more responsive, EMA crossovers can generate more false signals in volatile markets",
                "The choice of EMA periods significantly impacts performance"
            ],
            "improvement_suggestions": [
                "Consider using a price filter to reduce false signals",
                "Test different EMA period combinations to find optimal settings",
                "Combine with volatility indicators to avoid trading during choppy markets"
            ]
        },
        "macd": {
            "feedback": f"This simulation demonstrates a Moving Average Convergence Divergence (MACD) strategy applied to {asset} over {timeframe} days. MACD is a trend-following momentum indicator that shows the relationship between two moving averages of an asset's price. The MACD line is calculated by subtracting the 26-period EMA from the 12-period EMA. A 9-period EMA of the MACD, called the 'signal line', is then plotted on top of the MACD line. Buy signals typically occur when the MACD line crosses above the signal line, and sell signals when it crosses below. MACD can also show divergence with price, potentially indicating trend reversals.",
            "key_points": [
                "MACD combines trend following and momentum in one indicator",
                "Signal line crossovers are the primary trading signals",
                "Divergence between MACD and price can indicate potential reversals",
                "MACD histogram shows the difference between MACD and signal line"
            ],
            "improvement_suggestions": [
                "Use MACD in conjunction with price action analysis",
                "Consider the overall trend direction before taking MACD signals",
                "Look for MACD divergence to identify potential trend exhaustion"
            ]
        },
        "rsi": {
            "feedback": f"This simulation demonstrates a Relative Strength Index (RSI) strategy applied to {asset} over {timeframe} days. RSI is a momentum oscillator that measures the speed and change of price movements on a scale from 0 to 100. Traditional interpretation considers RSI values over 70 as overbought and under 30 as oversold, potentially signaling reversal points. RSI strategies can be effective for identifying potential reversal points in the market, but can lead to premature entries during strong trends. The indicator works best in ranging markets and should be used with caution during strong trending periods.",
            "key_points": [
                "RSI measures the magnitude of recent price changes to evaluate overbought or oversold conditions",
                "Traditional overbought level is 70 and oversold level is 30",
                "RSI can remain in overbought/oversold territory during strong trends",
                "RSI divergence with price can signal potential trend reversals"
            ],
            "improvement_suggestions": [
                "Adjust the RSI overbought/oversold levels based on the asset's volatility",
                "Combine RSI with trend indicators to avoid counter-trend trades",
                "Look for RSI divergence to confirm potential reversal signals"
            ]
        },
        "bollinger": {
            "feedback": f"This simulation demonstrates a Bollinger Bands strategy applied to {asset} over {timeframe} days. Bollinger Bands consist of a middle band (typically a 20-period SMA) with an upper and lower band set at standard deviations away from the middle band. The bands expand and contract based on volatility. Common strategies include buying when the price touches the lower band and selling when it touches the upper band (mean reversion), or entering trades when the price breaks out of the bands after a period of low volatility (volatility expansion). Bollinger Bands are versatile and can be used in both trending and ranging markets with appropriate adjustments.",
            "key_points": [
                "Bollinger Bands adapt to market volatility by widening and narrowing",
                "Price touching the bands alone is not necessarily a signal to trade",
                "Band width indicates market volatility - narrow bands often precede significant moves",
                "The middle band (SMA) can act as support/resistance in trending markets"
            ],
            "improvement_suggestions": [
                "Combine with volume indicators to confirm breakouts",
                "Use additional indicators to determine if the market is trending or ranging",
                "Consider using Bollinger Band %B or Bandwidth for additional insights"
            ]
        }
    }
    
    # Get template for the strategy or use a default template
    template = strategy_templates.get(strategy, {
        "feedback": f"This simulation demonstrates a {strategy_name} strategy applied to {asset} over {timeframe} days. The performance shows an ROI of {performance.get('roi', 'unknown')}%. Trading strategies can perform differently depending on market conditions, timeframes, and specific assets. It's important to understand the underlying principles of the strategy and how various market factors can influence its performance.",
        "key_points": [
            "Different strategies perform better in different market conditions",
            "Risk management is essential for long-term success",
            "Past performance is not indicative of future results",
            "Understanding the underlying principles of a strategy is more valuable than blindly following signals"
        ],
        "improvement_suggestions": [
            "Backtest the strategy across different market conditions",
            "Consider combining multiple indicators for confirmation",
            "Implement proper position sizing and risk management rules"
        ]
    })
    
    # Add performance-specific feedback
    roi = performance.get('roi', 0)
    if roi > 15:
        performance_feedback = f"The strategy performed well with an ROI of {roi}%, but remember that past performance doesn't guarantee future results. Market conditions can change rapidly."
    elif roi > 0:
        performance_feedback = f"The strategy showed a positive ROI of {roi}%, which is a moderate result. Consider how different market conditions might affect performance."
    else:
        performance_feedback = f"The strategy resulted in a negative ROI of {roi}%. This provides a valuable learning opportunity to understand what factors contributed to the underperformance."
    
    # Combine template feedback with performance feedback
    combined_feedback = f"{template['feedback']} {performance_feedback}"
    
    return EducationalFeedbackResponse(
        feedback=combined_feedback,
        key_points=template['key_points'],
        improvement_suggestions=template['improvement_suggestions']
    )
