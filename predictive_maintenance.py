import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import IsolationForest
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import pickle

# Load and preprocess data
def load_data(file_path):
    data = pd.read_csv(file_path)
    # Assume the dataset includes columns 'timestamp' and 'sensor_value'
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data = data.set_index('timestamp')
    # Scaling the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    data['sensor_value'] = scaler.fit_transform(data[['sensor_value']])
    return data, scaler

def prepare_data(data, time_steps):
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:i + time_steps])
        y.append(data[i + time_steps])
    return np.array(X), np.array(y)

def build_lstm_model(input_shape):
    model = Sequential([
        LSTM(50, activation='relu', input_shape=input_shape),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def train_predictive_model(file_path, time_steps=10):
    data, scaler = load_data(file_path)
    X, y = prepare_data(data['sensor_value'].values, time_steps)

    model = build_lstm_model((X.shape[1], X.shape[2]))
    model.fit(X, y, epochs=10, batch_size=32, verbose=1)

    # Save model and scaler
    model.save('predictive_model.h5')
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

# Example of using these functions
# train_predictive_model('sensor_data.csv')
