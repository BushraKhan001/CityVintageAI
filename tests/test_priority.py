"""
Tests for Priority Engine
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from services.priority_engine import PriorityEngine, PriorityResult
from services.risk_engine import RiskEngine, RiskSignal


def test_calculate_priority():
    """Test priority calculation"""
    engine = PriorityEngine()
    risk_engine = RiskEngine()
    
    signal = risk_engine.create_risk_signal(
        location_id="KHI-001",
        risk_type="flood",
        risk_score=80,
        explanation="Test",
        confidence_or_model_status="Test",
        data_source="Test"
    )
    
    result = engine.calculate_priority(
        location_id="KHI-001",
        location_name="Saddar",
        risk_signals=[signal],
        exposure="High",
        historical_vulnerability=0.75,
        overall_risk_score=80
    )
    
    assert result.location_id == "KHI-001"
    assert result.location_name == "Saddar"
    assert 0 <= result.priority_score <= 100
    assert result.priority_level in ["P1 - URGENT", "P2 - HIGH", "P3 - MONITOR"]
    assert len(result.reasons) > 0


def test_priority_levels():
    """Test priority level mapping"""
    engine = PriorityEngine()
    risk_engine = RiskEngine()
    
    signal = risk_engine.create_risk_signal(
        location_id="KHI-001",
        risk_type="flood",
        risk_score=50,
        explanation="Test",
        confidence_or_model_status="Test",
        data_source="Test"
    )
    
    # High priority
    result_high = engine.calculate_priority(
        location_id="KHI-001",
        location_name="Test High",
        risk_signals=[signal],
        exposure="High",
        historical_vulnerability=0.9,
        overall_risk_score=85
    )
    
    # Low priority
    result_low = engine.calculate_priority(
        location_id="KHI-002",
        location_name="Test Low",
        risk_signals=[signal],
        exposure="Low",
        historical_vulnerability=0.2,
        overall_risk_score=30
    )
    
    assert result_high.priority_score > result_low.priority_score


def test_rank_locations():
    """Test location ranking"""
    engine = PriorityEngine()
    
    results = [
        PriorityResult(
            location_id="KHI-001",
            location_name="Location A",
            priority_score=50,
            priority_level="P2 - HIGH",
            reasons=["Test"],
            risk_signals=[]
        ),
        PriorityResult(
            location_id="KHI-002",
            location_name="Location B",
            priority_score=90,
            priority_level="P1 - URGENT",
            reasons=["Test"],
            risk_signals=[]
        ),
        PriorityResult(
            location_id="KHI-003",
            location_name="Location C",
            priority_score=30,
            priority_level="P3 - MONITOR",
            reasons=["Test"],
            risk_signals=[]
        )
    ]
    
    ranked = engine.rank_locations(results)
    
    assert ranked[0].location_id == "KHI-002"  # Highest
    assert ranked[1].location_id == "KHI-001"  # Middle
    assert ranked[2].location_id == "KHI-003"  # Lowest


def test_priority_reasons_generated():
    """Test that reasons are generated"""
    engine = PriorityEngine()
    risk_engine = RiskEngine()
    
    signal = risk_engine.create_risk_signal(
        location_id="KHI-001",
        risk_type="flood",
        risk_score=85,
        explanation="Test",
        confidence_or_model_status="Test",
        data_source="Test"
    )
    
    result = engine.calculate_priority(
        location_id="KHI-001",
        location_name="Saddar",
        risk_signals=[signal],
        exposure="High",
        historical_vulnerability=0.8,
        overall_risk_score=85
    )
    
    assert len(result.reasons) > 0
    assert any("High" in reason for reason in result.reasons)


def test_priority_deterministic():
    """Test that priority calculation is deterministic"""
    engine = PriorityEngine()
    risk_engine = RiskEngine()
    
    signal = risk_engine.create_risk_signal(
        location_id="KHI-001",
        risk_type="flood",
        risk_score=75,
        explanation="Test",
        confidence_or_model_status="Test",
        data_source="Test"
    )
    
    result1 = engine.calculate_priority(
        location_id="KHI-001",
        location_name="Saddar",
        risk_signals=[signal],
        exposure="High",
        historical_vulnerability=0.75,
        overall_risk_score=75
    )
    
    result2 = engine.calculate_priority(
        location_id="KHI-001",
        location_name="Saddar",
        risk_signals=[signal],
        exposure="High",
        historical_vulnerability=0.75,
        overall_risk_score=75
    )
    
    assert result1.priority_score == result2.priority_score


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
