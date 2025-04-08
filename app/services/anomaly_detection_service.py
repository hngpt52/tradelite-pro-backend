import random
import numpy as np
from typing import List
from app.schemas.schemas import AnomalyDetectionResponse

def detect_anomalies(data: List[float], window_size: int = 20) -> AnomalyDetectionResponse:
    """
    Detect anomalies in time series data using a simple statistical approach
    
    This is a simplified implementation that uses Z-scores to detect anomalies.
    In a production environment, more sophisticated methods like Isolation Forest,
    DBSCAN, or LSTM autoencoders would be used.
    """
    if len(data) < window_size:
        # Not enough data points
        return AnomalyDetectionResponse(
            anomalies=[],
            scores=[0.0] * len(data),
            threshold=3.0
        )
    
    # Convert to numpy array for easier manipulation
    data_array = np.array(data)
    scores = []
    anomalies = []
    threshold = 3.0  # Z-score threshold for anomaly detection
    
    # Calculate rolling mean and std
    for i in range(len(data_array)):
        if i < window_size:
            # Not enough data for the window yet
            scores.append(0.0)
            continue
        
        # Get window of data
        window = data_array[i-window_size:i]
        
        # Calculate mean and std of window
        window_mean = np.mean(window)
        window_std = np.std(window)
        
        if window_std == 0:
            # Avoid division by zero
            scores.append(0.0)
            continue
        
        # Calculate z-score
        z_score = abs((data_array[i] - window_mean) / window_std)
        scores.append(float(z_score))
        
        # Check if anomaly
        if z_score > threshold:
            anomalies.append(i)
    
    return AnomalyDetectionResponse(
        anomalies=anomalies,
        scores=[float(s) for s in scores],
        threshold=float(threshold)
    )
