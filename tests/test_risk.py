"""
Tests for Risk Engine
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from services.risk_engine import RiskEngine, RiskSignal


def test_create_risk_signal():
    """Test creating a risk signal"""
    engine = RiskEngine()
    
    signal = engine.create_risk_signal(
        location_id="KHI-001",
        risk_type="flood",
        risk_score=75.5,
        explanation="High rainfall detected",
        confidence_or_model_status="Trained Model",
        data_source="Test data"
    )
    
    assert signal.location_id == "KHI-001"
    assert signal.risk_type == "flood"
    assert signal.risk_score == 75.5
    assert signal.risk_level == "HIGH"


def test_risk_score_normalization():
    """Test that risk scores are normalized to 0-100"""
    engine = RiskEngine()
    
    signal = engine.create_risk_signal(
        location_id="KHI-001",
        risk_type="flood",
        risk_score=150,  # Over 100
        explanation="Test",
        confidence_or_model_status="Test",
        data_source="Test"
    )
    
    assert signal.risk_score == 100


def test_risk_level_mapping():
    """Test risk level mapping"""
    engine = RiskEngine()
    
    # Low risk
    signal_low = engine.create_risk_signal(
        location_id="KHI-001",
        risk_type="flood",
        risk_score=25,
        explanation="Test",
        confidence_or_model_status="Test",
        data_source="Test"
    )
    assert signal_low.risk_level == "LOW"
    
    # Medium risk
    signal_med = engine.create_risk_signal(
        location_id="KHI-002",
        risk_type="flood",
        risk_score=55,
        explanation="Test",
        confidence_or_model_status="Test",
        data_source="Test"
    )
    assert signal_med.risk_level == "MEDIUM"
    
    # High risk
    signal_high = engine.create_risk_signal(
        location_id="KHI-003",
        risk_type="flood",
        risk_score=85,
        explanation="Test",
        confidence_or_model_status="Test",
        data_source="Test"
    )
    assert signal_high.risk_level == "HIGH"


def test_calculate_overall_risk():
    """Test overall risk calculation"""
    engine = RiskEngine()
    
    signal1 = engine.create_risk_signal(
        location_id="KHI-001",
        risk_type="flood",
        risk_score=80,
        explanation="Test",
        confidence_or_model_status="Test",
        data_source="Test"
    )
    
    signal2 = engine.create_risk_signal(
        location_id="KHI-001",
        risk_type="traffic",
        risk_score=60,
        explanation="Test",
        confidence_or_model_status="Test",
        data_source="Test"
    )
    
    overall = engine.calculate_overall_risk([signal1, signal2])
    
    assert "overall_score" in overall
    assert "overall_level" in overall
    assert "components" in overall
    assert overall["available_signals"] == 2
    assert overall["overall_score"] > 0


def test_overall_risk_empty():
    """Test overall risk with no signals"""
    engine = RiskEngine()
    
    overall = engine.calculate_overall_risk([])
    
    assert overall["overall_score"] == 0
    assert overall["overall_level"] == "LOW"
    assert overall["available_signals"] == 0


def test_overall_risk_weights():
    """Test that risk weights are applied"""
    engine = RiskEngine()
    
    # Flood has weight 0.45, traffic has 0.35
    signal_flood = engine.create_risk_signal(
        location_id="KHI-001",
        risk_type="flood",
        risk_score=100,
        explanation="Test",
        confidence_or_model_status="Test",
        data_source="Test"
    )
    
    signal_traffic = engine.create_risk_signal(
        location_id="KHI-001",
        risk_type="traffic",
        risk_score=50,
        explanation="Test",
        confidence_or_model_status="Test",
        data_source="Test"
    )
    
    overall = engine.calculate_overall_risk([signal_flood, signal_traffic])
    
    # Should be weighted average
    expected = (100 * 0.45 + 50 * 0.35) / (0.45 + 0.35)
    assert abs(overall["overall_score"] - expected) < 0.1


def test_risk_summary():
    """Test risk summary generation"""
    engine = RiskEngine()
    
    signal1 = engine.create_risk_signal(
        location_id="KHI-001",
        risk_type="flood",
        risk_score=80,
        explanation="High flood risk",
        confidence_or_model_status="Test",
        data_source="Test"
    )
    
    signal2 = engine.create_risk_signal(
        location_id="KHI-001",
        risk_type="traffic",
        risk_score=60,
        explanation="Medium traffic risk",
        confidence_or_model_status="Test",
        data_source="Test"
    )
    
    summary = engine.get_risk_summary([signal1, signal2])
    
    assert summary["total_signals"] == 2
    assert "flood" in summary["by_type"]
    assert "traffic" in summary["by_type"]
    assert summary["highest_risk"] == signal1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
