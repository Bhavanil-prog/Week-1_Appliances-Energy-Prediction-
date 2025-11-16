"""
Utility functions for the Energy Dashboard
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import logging

logger = logging.getLogger(__name__)

class EnergyDataHandler:
    """Handle energy data loading and preprocessing"""
    
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None
        self.feature_columns = None
    
    def load_data(self):
        """Load and preprocess energy data"""
        try:
            self.df = pd.read_csv(self.csv_path)
            self.df['date'] = pd.to_datetime(self.df['date'], format='%d-%m-%Y %H:%M')
            self.df = self.df.sort_values('date').reset_index(drop=True)
            
            # Create time features
            self.df['hour'] = self.df['date'].dt.hour
            self.df['day'] = self.df['date'].dt.day
            self.df['month'] = self.df['date'].dt.month
            self.df['weekday'] = self.df['date'].dt.dayofweek
            
            logger.info(f"Data loaded: {self.df.shape[0]} records")
            return self.df
        
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def get_summary_stats(self):
        """Get summary statistics"""
        if self.df is None:
            raise ValueError("Data not loaded")
        
        return {
            'total_records': len(self.df),
            'date_range': (self.df['date'].min(), self.df['date'].max()),
            'appliances_mean': self.df['Appliances'].mean(),
            'appliances_std': self.df['Appliances'].std(),
            'lights_mean': self.df['lights'].mean(),
            'temperature_mean': self.df['T1'].mean()
        }
    
    def get_hourly_pattern(self):
        """Get hourly consumption pattern"""
        if self.df is None:
            raise ValueError("Data not loaded")
        
        hourly = self.df.groupby('hour').agg({
            'Appliances': ['mean', 'std'],
            'lights': ['mean', 'std']
        }).round(2)
        
        return hourly
    
    def get_daily_pattern(self):
        """Get daily consumption pattern"""
        if self.df is None:
            raise ValueError("Data not loaded")
        
        self.df['date_only'] = self.df['date'].dt.date
        daily = self.df.groupby('date_only').agg({
            'Appliances': 'mean',
            'lights': 'mean'
        }).round(2)
        
        return daily

class EnergyPredictionModel:
    """Machine learning model for energy prediction"""
    
    def __init__(self, data):
        self.data = data
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.metrics = {}
    
    def prepare_features(self):
        """Prepare features for model training"""
        self.feature_columns = [col for col in self.data.columns 
                               if col not in ['date', 'Appliances', 'date_only']]
        
        X = self.data[self.feature_columns].fillna(self.data[self.feature_columns].mean())
        y = self.data['Appliances']
        
        return X, y
    
    def train(self):
        """Train the prediction model"""
        try:
            X, y = self.prepare_features()
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                random_state=42,
                n_jobs=-1
            )
            self.model.fit(X_train_scaled, y_train)
            
            # Calculate metrics
            train_pred = self.model.predict(X_train_scaled)
            test_pred = self.model.predict(X_test_scaled)
            
            self.metrics = {
                'train_r2': r2_score(y_train, train_pred),
                'test_r2': r2_score(y_test, test_pred),
                'train_mae': mean_absolute_error(y_train, train_pred),
                'test_mae': mean_absolute_error(y_test, test_pred),
                'train_rmse': np.sqrt(mean_squared_error(y_train, train_pred)),
                'test_rmse': np.sqrt(mean_squared_error(y_test, test_pred))
            }
            
            logger.info(f"Model trained. Test R²: {self.metrics['test_r2']:.4f}")
            return self.metrics
        
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise
    
    def predict(self, features_dict):
        """Make prediction for given features"""
        if self.model is None:
            raise ValueError("Model not trained")
        
        try:
            # Prepare input
            input_data = []
            for col in self.feature_columns:
                if col in features_dict:
                    input_data.append(float(features_dict[col]))
                else:
                    input_data.append(self.data[col].mean())
            
            # Scale and predict
            input_scaled = self.scaler.transform([input_data])
            prediction = self.model.predict(input_scaled)[0]
            
            return max(0, prediction)
        
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            raise
    
    def get_feature_importance(self, top_n=10):
        """Get top N important features"""
        if self.model is None:
            raise ValueError("Model not trained")
        
        importance_df = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False).head(top_n)
        
        return importance_df

def create_visualizations(data):
    """Helper function to create visualization data"""
    viz_data = {
        'hourly': data.groupby('hour')['Appliances'].mean().to_dict(),
        'daily_avg': data.groupby(data['date'].dt.date)['Appliances'].mean().tail(30).to_dict(),
        'by_weekday': data.groupby('weekday')['Appliances'].mean().to_dict(),
        'temperature_rooms': {}
    }
    
    temp_cols = [col for col in data.columns if col.startswith('T')][:8]
    for col in temp_cols:
        viz_data['temperature_rooms'][col] = {
            'mean': float(data[col].mean()),
            'max': float(data[col].max()),
            'min': float(data[col].min())
        }
    
    return viz_data
