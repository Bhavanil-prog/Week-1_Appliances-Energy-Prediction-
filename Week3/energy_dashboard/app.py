from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Global variables
df = None
model = None
scaler = None
feature_columns = None

def load_and_prepare_data():
    """Load and preprocess the energy data"""
    global df, model, scaler, feature_columns
    
    csv_path = '../energydata_complete.csv'
    df = pd.read_csv(csv_path)
    
    # Parse date
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y %H:%M')
    
    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)
    
    # Create time-based features
    df['hour'] = df['date'].dt.hour
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['weekday'] = df['date'].dt.dayofweek
    
    return df

def train_model():
    """Train the energy consumption prediction model"""
    global model, scaler, feature_columns
    
    # Prepare features and target
    feature_cols = [col for col in df.columns if col not in ['date', 'Appliances']]
    feature_columns = feature_cols
    
    X = df[feature_cols].fillna(df[feature_cols].mean())
    y = df['Appliances']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)
    
    return {
        'train_score': float(train_score),
        'test_score': float(test_score)
    }

def get_data_summary():
    """Get summary statistics of the data"""
    return {
        'total_records': len(df),
        'date_range': {
            'start': df['date'].min().strftime('%Y-%m-%d'),
            'end': df['date'].max().strftime('%Y-%m-%d')
        },
        'appliances': {
            'mean': float(df['Appliances'].mean()),
            'min': float(df['Appliances'].min()),
            'max': float(df['Appliances'].max()),
            'std': float(df['Appliances'].std())
        },
        'lights': {
            'mean': float(df['lights'].mean()),
            'min': float(df['lights'].min()),
            'max': float(df['lights'].max())
        },
        'temperature': {
            'mean': float(df['T1'].mean()),
            'min': float(df['T1'].min()),
            'max': float(df['T1'].max())
        }
    }

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/api/summary')
def api_summary():
    """API endpoint for data summary"""
    try:
        summary = get_data_summary()
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/hourly-avg')
def api_hourly_avg():
    """API endpoint for hourly average consumption"""
    try:
        hourly = df.groupby('hour').agg({
            'Appliances': 'mean',
            'lights': 'mean'
        }).reset_index()
        
        return jsonify({
            'hours': hourly['hour'].tolist(),
            'appliances': hourly['Appliances'].tolist(),
            'lights': hourly['lights'].tolist()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/daily-avg')
def api_daily_avg():
    """API endpoint for daily average consumption"""
    try:
        df_copy = df.copy()
        df_copy['day_date'] = df_copy['date'].dt.date
        daily = df_copy.groupby('day_date').agg({
            'Appliances': 'mean',
            'lights': 'mean'
        }).reset_index()
        
        return jsonify({
            'dates': [str(d) for d in daily['day_date'].tolist()],
            'appliances': daily['Appliances'].tolist(),
            'lights': daily['lights'].tolist()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/top-consumers')
def api_top_consumers():
    """API endpoint for top energy consumers"""
    try:
        temp_cols = [col for col in df.columns if col.startswith('T')]
        consumer_data = []
        
        for col in temp_cols[:6]:  # Top 6 rooms
            consumer_data.append({
                'name': col,
                'avg_temp': float(df[col].mean()),
                'max_temp': float(df[col].max())
            })
        
        return jsonify(consumer_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for energy prediction"""
    try:
        data = request.json
        
        # Prepare prediction data
        pred_data = []
        for col in feature_columns:
            if col in data:
                pred_data.append(float(data[col]))
            else:
                pred_data.append(df[col].mean())
        
        # Scale and predict
        pred_scaled = scaler.transform([pred_data])
        prediction = model.predict(pred_scaled)[0]
        
        return jsonify({
            'prediction': float(max(0, prediction)),
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/model-info')
def api_model_info():
    """API endpoint for model information"""
    try:
        metrics = train_model()
        return jsonify({
            'model_type': 'Random Forest Regressor',
            'n_estimators': 100,
            'train_score': metrics['train_score'],
            'test_score': metrics['test_score'],
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    try:
        # Load data and train model
        print("Loading data...")
        load_and_prepare_data()
        print("Data loaded successfully!")
        
        print("Training model...")
        train_model()
        print("Model trained successfully!")
        
        # Run Flask app
        print("Starting Flask app on http://localhost:5000")
        app.run(debug=True, port=5000)
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
