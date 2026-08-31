"""
Traffic Prediction Model - City Vantage AI
Simple regression model for traffic congestion prediction
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
from pathlib import Path
from typing import Dict, Optional

from utils.data_loader import load_traffic_data


class TrafficModel:
    """Traffic congestion prediction model"""
    
    def __init__(self):
        self.model = None
        self.feature_names = ["hour", "day_of_week", "is_rush_hour", "road_work"]
        self.is_trained = False
        self.metrics = {}
        self.congestion_mapping = {"Low": 1, "Medium": 2, "High": 3}
        self.reverse_mapping = {1: "Low", 2: "Medium", 3: "High"}
    
    def train(self, test_size: float = 0.2, random_state: int = 42) -> bool:
        """Train the traffic prediction model"""
        try:
            df = load_traffic_data()
            
            df["congestion_numeric"] = df["congestion"].map(self.congestion_mapping)
            
            X = df[self.feature_names]
            y = df["congestion_numeric"]
            
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state
            )
            
            self.model = RandomForestRegressor(
                n_estimators=50,
                max_depth=6,
                random_state=random_state,
                n_jobs=-1
            )
            
            self.model.fit(X_train, y_train)
            
            y_pred = self.model.predict(X_test)
            
            self.metrics = {
                "mae": mean_absolute_error(y_test, y_pred),
                "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
                "r2": r2_score(y_test, y_pred),
                "test_samples": len(y_test),
                "train_samples": len(y_train)
            }
            
            self.is_trained = True
            return True
            
        except Exception as e:
            print(f"Error training traffic model: {e}")
            self.is_trained = False
            return False
    
    def predict(self, features: Dict) -> Optional[Dict]:
        """
        Predict traffic congestion for given features
        
        Returns dict with prediction, risk_score, risk_level
        """
        if not self.is_trained:
            return None
        
        try:
            X = pd.DataFrame([features])[self.feature_names]
            
            prediction = self.model.predict(X)[0]
            prediction_rounded = round(prediction)
            
            congestion_level = self.reverse_mapping.get(prediction_rounded, "Medium")
            
            risk_score = (prediction / 3.0) * 100

            from utils.helpers import risk_level_from_score
            risk_level = risk_level_from_score(risk_score)
            
            explanation = self._generate_explanation(features, prediction)
            
            return {
                "congestion_prediction": float(prediction),
                "congestion_level": congestion_level,
                "risk_score": float(risk_score),
                "risk_level": risk_level,
                "explanation": explanation,
                "model_status": "Trained Random Forest Regressor",
                "data_provenance": "Demonstration data - not live Karachi traffic",
                "metrics": self.metrics
            }
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            return None
    
    def _generate_explanation(self, features: Dict, prediction: float) -> str:
        """Generate explanation for traffic prediction"""
        reasons = []
        
        hour = features.get("hour", 12)
        if 7 <= hour <= 9 or 17 <= hour <= 19:
            reasons.append(f"Rush hour period ({hour}:00)")
        
        if features.get("is_rush_hour", 0) == 1:
            reasons.append("Peak traffic time")
        
        if features.get("road_work", 0) == 1:
            reasons.append("Road work in progress")
        
        day = features.get("day_of_week", 1)
        if day >= 5:
            reasons.append("Weekend - typically lower traffic")
        elif day == 0:
            reasons.append("Monday - high traffic volume")
        
        if not reasons:
            reasons.append("Normal traffic conditions expected")
        
        return " | ".join(reasons)
    
    def save(self, path: str):
        """Save model to disk"""
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        
        with open(path, "wb") as f:
            pickle.dump({
                "model": self.model,
                "metrics": self.metrics,
                "is_trained": self.is_trained,
                "congestion_mapping": self.congestion_mapping,
                "reverse_mapping": self.reverse_mapping
            }, f)
    
    def load(self, path: str) -> bool:
        """Load model from disk"""
        try:
            with open(path, "rb") as f:
                data = pickle.load(f)
                self.model = data["model"]
                self.metrics = data["metrics"]
                self.is_trained = data["is_trained"]
                self.congestion_mapping = data["congestion_mapping"]
                self.reverse_mapping = data["reverse_mapping"]
                return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False


# Singleton instance
_model_instance = None


def get_traffic_model() -> TrafficModel:
    """Get or create traffic model instance"""
    global _model_instance
    if _model_instance is None:
        _model_instance = TrafficModel()
        _model_instance.train()
    return _model_instance
