"""
Risk Engine - City Vantage AI
Unified risk processing and scoring system
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from utils.helpers import normalize_score, risk_level_from_score


@dataclass
class RiskSignal:
    """Standardized risk signal structure"""
    location_id: str
    risk_type: str
    risk_score: float
    risk_level: str
    confidence_or_model_status: str
    explanation: str
    data_source: str
    details: Optional[Dict] = None


class RiskEngine:
    """Unified risk processing engine"""
    
    def __init__(self):
        self.risk_weights = {
            "flood": 0.45,
            "traffic": 0.35,
            "road": 0.20
        }
    
    def create_risk_signal(
        self,
        location_id: str,
        risk_type: str,
        risk_score: float,
        explanation: str,
        confidence_or_model_status: str,
        data_source: str,
        details: Optional[Dict] = None
    ) -> RiskSignal:
        """Create a standardized risk signal"""
        
        normalized_score = normalize_score(risk_score, 0, 100)
        risk_level = risk_level_from_score(normalized_score)
        
        return RiskSignal(
            location_id=location_id,
            risk_type=risk_type,
            risk_score=normalized_score,
            risk_level=risk_level,
            confidence_or_model_status=confidence_or_model_status,
            explanation=explanation,
            data_source=data_source,
            details=details
        )
    
    def calculate_overall_risk(self, risk_signals: List[RiskSignal]) -> Dict:
        """
        Calculate overall risk from multiple risk signals
        
        Uses weighted average based on configured weights
        """
        if not risk_signals:
            return {
                "overall_score": 0,
                "overall_level": "LOW",
                "components": [],
                "available_signals": 0
            }
        
        available_signals = [s for s in risk_signals if s.risk_score is not None]
        
        if not available_signals:
            return {
                "overall_score": 0,
                "overall_level": "LOW",
                "components": [],
                "available_signals": 0
            }
        
        total_weight = sum(self.risk_weights.get(s.risk_type, 0.2) for s in available_signals)
        if total_weight == 0:
            total_weight = 1
        
        weighted_sum = sum(
            s.risk_score * self.risk_weights.get(s.risk_type, 0.2)
            for s in available_signals
        )
        
        overall_score = weighted_sum / total_weight
        overall_level = risk_level_from_score(overall_score)
        
        components = [
            {
                "type": s.risk_type,
                "score": s.risk_score,
                "level": s.risk_level,
                "weight": self.risk_weights.get(s.risk_type, 0.2)
            }
            for s in available_signals
        ]
        
        return {
            "overall_score": float(overall_score),
            "overall_level": overall_level,
            "components": components,
            "available_signals": len(available_signals),
            "weights": self.risk_weights
        }
    
    def get_risk_summary(self, risk_signals: List[RiskSignal]) -> Dict:
        """Get summary of all risk signals for a location"""
        
        summary = {
            "total_signals": len(risk_signals),
            "by_type": {},
            "highest_risk": None,
            "all_explanations": []
        }
        
        for signal in risk_signals:
            summary["by_type"][signal.risk_type] = {
                "score": signal.risk_score,
                "level": signal.risk_level,
                "explanation": signal.explanation
            }
            summary["all_explanations"].append(f"{signal.risk_type}: {signal.explanation}")
        
        if risk_signals:
            summary["highest_risk"] = max(risk_signals, key=lambda s: s.risk_score)
        
        return summary
