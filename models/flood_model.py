"""
Flood Risk Model - City Vantage AI
Random Forest classifier for flood risk prediction
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.preprocessing import StandardScaler
import pickle
from pathlib import Path
from typing import Dict, Tuple, Optional

from utils.data_loader import load_flood_data


class FloodModel:
    """Flood risk prediction model using Random Forest"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            "rainfall_1h", "rainfall_3h", "rainfall_24h", 
            "previous_rainfall", "historical_flood", 
            "drainage_capacity", "soil_saturation"
        ]
        self.is_trained = False
        self.metrics = {}
    
    def train(self, test_size: float = 0.2, random_state: int = 42) -> bool:
        """Train the flood prediction model"""
        try:
            df = load_flood_data()
            
            X = df[self.feature_names]
            y = df["flood_occurred"]
            
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state, stratify=y
            )
            
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=8,
                min_samples_split=3,
                random_state=random_state,
                n_jobs=-1
            )
            
            self.model.fit(X_train_scaled, y_train)
            
            y_pred = self.model.predict(X_test_scaled)
            y_pred_proba = self.model.predict_proba(X_test_scaled)
            
            self.metrics = {
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred, zero_division=0),
                "recall": recall_score(y_test, y_pred, zero_division=0),
                "f1_score": f1_score(y_test, y_pred, zero_division=0),
                "test_samples": len(y_test),
                "train_samples": len(y_train)
            }
            
            self.is_trained = True
            return True
            
        except Exception as e:
            print(f"Error training flood model: {e}")
            self.is_trained = False
            return False
    
    def predict(self, features: Dict) -> Optional[Dict]:
        """
        Predict flood risk for given features
        
        Returns dict with probability, risk_score, risk_level, explanation
        """
        if not self.is_trained:
            return None
        
        try:
            X = pd.DataFrame([features])[self.feature_names]
            X_scaled = self.scaler.transform(X)
            
            probability = self.model.predict_proba(X_scaled)[0][1]
            risk_score = probability * 100

            from utils.helpers import risk_level_from_score
            risk_level = risk_level_from_score(risk_score)
            
            explanation = self._generate_explanation(features, probability)
            
            return {
                "probability": float(probability),
                "risk_score": float(risk_score),
                "risk_level": risk_level,
                "explanation": explanation,
                "model_status": "Trained Random Forest",
                "metrics": self.metrics
            }
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            return None
    
    def _generate_explanation(self, features: Dict, probability: float) -> str:
        """Generate explanation based on feature importance and values"""
        reasons = []
        
        if features.get("rainfall_1h", 0) > 30:
            reasons.append(f"High recent rainfall ({features['rainfall_1h']:.1f}mm in last hour)")
        
        if features.get("rainfall_24h", 0) > 150:
            reasons.append(f"Elevated 24-hour rainfall accumulation ({features['rainfall_24h']:.1f}mm)")
        
        if features.get("previous_rainfall", 0) > 100:
            reasons.append(f"High previous rainfall ({features['previous_rainfall']:.1f}mm)")
        
        if features.get("historical_flood", 0) == 1:
            reasons.append("History of flooding in this location")
        
        if features.get("drainage_capacity", 1) < 0.5:
            reasons.append(f"Low drainage capacity ({features['drainage_capacity']:.2f})")
        
        if features.get("soil_saturation", 0) > 0.7:
            reasons.append(f"High soil saturation ({features['soil_saturation']:.2f})")
        
        if not reasons:
            reasons.append("Multiple moderate risk factors combined")
        
        return " | ".join(reasons)
    
    def get_feature_importance(self) -> Optional[Dict]:
        """Get feature importance from trained model"""
        if not self.is_trained or self.model is None:
            return None
        
        importance = dict(zip(
            self.feature_names,
            self.model.feature_importances_
        ))
        return dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
    
    def save(self, path: str):
        """Save model to disk"""
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        
        with open(path, "wb") as f:
            pickle.dump({
                "model": self.model,
                "scaler": self.scaler,
                "metrics": self.metrics,
                "is_trained": self.is_trained
            }, f)
    
    def load(self, path: str) -> bool:
        """Load model from disk"""
        try:
            with open(path, "rb") as f:
                data = pickle.load(f)
                self.model = data["model"]
                self.scaler = data["scaler"]
                self.metrics = data["metrics"]
                self.is_trained = data["is_trained"]
                return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False


# Singleton instance
_model_instance = None


def get_flood_model() -> FloodModel:
    """Get or create flood model instance"""
    global _model_instance
    if _model_instance is None:
        _model_instance = FloodModel()
        _model_instance.train()
    return _model_instance
