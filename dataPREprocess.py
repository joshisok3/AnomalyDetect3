import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_and_preprocess_data(file_path):
    #load data
    data = pd.read_csv(file_path)

    #convert timestamp to datetime (this does not work perfectly, try is not needed due to fallback feature for time)
    data['timestamp'] = pd.to_datetime(data['timestamp'])

    #extract hour from login_time for anomaly detection
    data['login_hour'] = pd.to_datetime(data['login_time']).dt.hour

    #features to use for anomaly detection
    features = data[['login_hour', 'action_duration']]

    #normalize the data using StandardScaler
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    return data, scaled_features

