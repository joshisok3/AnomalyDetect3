from sklearn.ensemble import IsolationForest

def detect_anomalies(scaled_features, contamination=0.1):
    """
    Detect anomalies using Isolation Forest.
    
    """
    #initialize and train Isolation Forest
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(scaled_features)

    #predict anomalies (-1 for anomaly, 1 for normal)
    predictions = model.predict(scaled_features)
    
    return predictions

