"""
Tests for Flood Model
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from models.flood_model import FloodModel, get_flood_model


def test_flood_model_trains():
    """Test that flood model can train successfully"""
    model = FloodModel()
    result = model.train()
    assert result is True
    assert model.is_trained is True


def test_flood_model_predicts():
    """Test that flood model can make predictions"""
    model = FloodModel()
    model.train()
    
    features = {
        "rainfall_1h": 45.0,
        "rainfall_3h": 120.0,
        "rainfall_24h": 180.0,
        "previous_rainfall": 85.0,
        "historical_flood": 1,
        "drainage_capacity": 0.45,
        "soil_saturation": 0.78
    }
    
    result = model.predict(features)
    
    assert result is not None
    assert "probability" in result
    assert "risk_score" in result
    assert "risk_level" in result
    assert "explanation" in result


def test_flood_probability_valid():
    """Test that flood probability is between 0 and 1"""
    model = FloodModel()
    model.train()
    
    features = {
        "rainfall_1h": 50.0,
        "rainfall_3h": 130.0,
        "rainfall_24h": 190.0,
        "previous_rainfall": 90.0,
        "historical_flood": 1,
        "drainage_capacity": 0.40,
        "soil_saturation": 0.80
    }
    
    result = model.predict(features)
    
    assert 0 <= result["probability"] <= 1


def test_flood_risk_score_range():
    """Test that flood risk score is between 0 and 100"""
    model = FloodModel()
    model.train()
    
    features = {
        "rainfall_1h": 50.0,
        "rainfall_3h": 130.0,
        "rainfall_24h": 190.0,
        "previous_rainfall": 90.0,
        "historical_flood": 1,
        "drainage_capacity": 0.40,
        "soil_saturation": 0.80
    }
    
    result = model.predict(features)
    
    assert 0 <= result["risk_score"] <= 100


def test_flood_risk_level_valid():
    """Test that flood risk level is valid"""
    model = FloodModel()
    model.train()
    
    features = {
        "rainfall_1h": 50.0,
        "rainfall_3h": 130.0,
        "rainfall_24h": 190.0,
        "previous_rainfall": 90.0,
        "historical_flood": 1,
        "drainage_capacity": 0.40,
        "soil_saturation": 0.80
    }
    
    result = model.predict(features)
    
    assert result["risk_level"] in ["LOW", "MEDIUM", "HIGH"]


def test_flood_model_metrics():
    """Test that model metrics are calculated"""
    model = FloodModel()
    model.train()
    
    assert "accuracy" in model.metrics
    assert "precision" in model.metrics
    assert "recall" in model.metrics
    assert "f1_score" in model.metrics
    assert model.metrics["accuracy"] > 0


def test_flood_explanation_generated():
    """Test that explanation is generated"""
    model = FloodModel()
    model.train()
    
    features = {
        "rainfall_1h": 45.0,
        "rainfall_3h": 120.0,
        "rainfall_24h": 180.0,
        "previous_rainfall": 85.0,
        "historical_flood": 1,
        "drainage_capacity": 0.45,
        "soil_saturation": 0.78
    }
    
    result = model.predict(features)
    
    assert result["explanation"] is not None
    assert len(result["explanation"]) > 0


def test_get_flood_model_singleton():
    """Test that get_flood_model returns trained model"""
    model = get_flood_model()
    
    assert model is not None
    assert model.is_trained is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
