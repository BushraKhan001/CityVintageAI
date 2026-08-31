"""
Priority Engine - City Vantage AI
Location prioritization based on risk severity and impact
"""

from typing import Dict, List
from dataclasses import dataclass
from services.risk_engine import RiskSignal
from utils.helpers import priority_level_from_score


@dataclass
class PriorityResult:
    """Priority calculation result"""
    location_id: str
    location_name: str
    priority_score: float
    priority_level: str
    reasons: List[str]
    risk_signals: List[Dict]


class PriorityEngine:
    """Engine for calculating location priorities"""
    
    def __init__(self):
        self.weights = {
            "risk_severity": 0.40,
            "exposure": 0.25,
            "historical_vulnerability": 0.20,
            "model_confidence": 0.15
        }
    
    def calculate_priority(
        self,
        location_id: str,
        location_name: str,
        risk_signals: List[RiskSignal],
        exposure: str,
        historical_vulnerability: float,
        overall_risk_score: float
    ) -> PriorityResult:
        """
        Calculate priority for a location
        
        Factors:
        - Risk severity (overall risk score)
        - Exposure level
        - Historical vulnerability
        - Model confidence/availability
        """
        
        reasons = []
        
        # Risk severity component (0-100)
        risk_severity_score = overall_risk_score
        if risk_severity_score >= 70:
            reasons.append(f"High risk severity ({risk_severity_score:.1f}/100)")
        
        # Exposure component (0-100)
        exposure_map = {"Low": 33, "Medium": 66, "High": 100}
        exposure_score = exposure_map.get(exposure, 50)
        if exposure == "High":
            reasons.append(f"High exposure area")
        
        # Historical vulnerability (0-100)
        vulnerability_score = historical_vulnerability * 100
        if historical_vulnerability > 0.7:
            reasons.append(f"High historical vulnerability ({historical_vulnerability:.2f})")
        
        # Model confidence/availability (0-100)
        available_signals = len(risk_signals)
        confidence_score = (available_signals / 3.0) * 100  # Max 3 signals
        if available_signals >= 3:
            reasons.append("Multiple risk signals available")
        
        # Weighted priority score
        priority_score = (
            risk_severity_score * self.weights["risk_severity"] +
            exposure_score * self.weights["exposure"] +
            vulnerability_score * self.weights["historical_vulnerability"] +
            confidence_score * self.weights["model_confidence"]
        )
        
        priority_level = priority_level_from_score(priority_score)
        
        risk_signals_summary = [
            {
                "type": s.risk_type,
                "score": s.risk_score,
                "level": s.risk_level
            }
            for s in risk_signals
        ]
        
        if not reasons:
            reasons.append("Moderate risk factors present")
        
        return PriorityResult(
            location_id=location_id,
            location_name=location_name,
            priority_score=float(priority_score),
            priority_level=priority_level,
            reasons=reasons,
            risk_signals=risk_signals_summary
        )
    
    def rank_locations(self, priority_results: List[PriorityResult]) -> List[PriorityResult]:
        """Rank locations by priority score (highest first)"""
        return sorted(priority_results, key=lambda x: x.priority_score, reverse=True)
