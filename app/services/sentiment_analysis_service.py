import re
from typing import Dict
from app.schemas.schemas import SentimentAnalysisResponse

def analyze_sentiment(text: str) -> SentimentAnalysisResponse:
    """
    Analyze sentiment of financial text using a keyword-based approach
    
    This is a simplified implementation that uses keyword matching.
    In a production environment, a pre-trained model like FinBERT would be used.
    """
    # Convert to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Define positive and negative keywords for financial text
    positive_keywords = [
        'bullish', 'uptrend', 'growth', 'profit', 'gain', 'outperform',
        'buy', 'strong', 'positive', 'up', 'rise', 'rising', 'rally',
        'opportunity', 'optimistic', 'confident', 'exceed', 'beat',
        'momentum', 'recovery', 'upgrade', 'success', 'improve'
    ]
    
    negative_keywords = [
        'bearish', 'downtrend', 'decline', 'loss', 'risk', 'underperform',
        'sell', 'weak', 'negative', 'down', 'fall', 'falling', 'drop',
        'threat', 'pessimistic', 'concerned', 'miss', 'below',
        'slowdown', 'recession', 'downgrade', 'failure', 'worsen'
    ]
    
    # Count occurrences of keywords
    positive_count = sum(1 for keyword in positive_keywords if re.search(r'\b' + keyword + r'\b', text_lower))
    negative_count = sum(1 for keyword in negative_keywords if re.search(r'\b' + keyword + r'\b', text_lower))
    
    # Calculate sentiment score (-1 to 1)
    total_count = positive_count + negative_count
    if total_count == 0:
        # No sentiment keywords found
        sentiment_score = 0.0
        sentiment = "neutral"
        explanation = "No clear sentiment indicators found in the text."
    else:
        sentiment_score = (positive_count - negative_count) / total_count
        
        # Determine sentiment category
        if sentiment_score > 0.25:
            sentiment = "positive"
            explanation = f"The text contains more positive financial indicators ({positive_count}) than negative ones ({negative_count})."
        elif sentiment_score < -0.25:
            sentiment = "negative"
            explanation = f"The text contains more negative financial indicators ({negative_count}) than positive ones ({positive_count})."
        else:
            sentiment = "neutral"
            explanation = f"The text contains a balanced mix of positive ({positive_count}) and negative ({negative_count}) financial indicators."
    
    return SentimentAnalysisResponse(
        sentiment=sentiment,
        score=sentiment_score,
        explanation=explanation
    )
