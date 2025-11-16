"""
Configuration file for Energy Dashboard
"""

import os

# Flask Configuration
FLASK_ENV = 'development'
FLASK_DEBUG = True
SECRET_KEY = 'your-secret-key-here'

# Data Configuration
DATA_PATH = '../energydata_complete.csv'

# Model Configuration
MODEL_CONFIG = {
    'algorithm': 'RandomForest',
    'n_estimators': 100,
    'max_depth': 15,
    'random_state': 42,
    'test_size': 0.2
}

# API Configuration
API_PORT = 5000
API_HOST = '0.0.0.0'

# Streamlit Configuration
STREAMLIT_PORT = 8501

# Feature Columns
FEATURE_COLUMNS = [
    'lights', 'T1', 'RH_1', 'T2', 'RH_2', 'T3', 'RH_3', 'T4', 'RH_4',
    'T5', 'RH_5', 'T6', 'RH_6', 'T7', 'RH_7', 'T8', 'RH_8', 'T9', 'RH_9',
    'T_out', 'Press_mm_hg', 'RH_out', 'Windspeed', 'Visibility', 'Tdewpoint',
    'rv1', 'rv2', 'hour', 'day', 'month', 'weekday'
]

# Prediction Configuration
PREDICTION_RANGES = {
    'temperature': {'min': 5, 'max': 30},
    'humidity': {'min': 0, 'max': 100},
    'hour': {'min': 0, 'max': 23}
}

# Chart Configuration
CHART_CONFIG = {
    'color_primary': '#2563eb',
    'color_secondary': '#f59e0b',
    'color_success': '#10b981',
    'color_danger': '#ef4444'
}
