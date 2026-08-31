"""
Explanation Engine - City Vantage AI
Generates human-readable explanations for risk assessments
"""

from typing import Dict, List
from services.risk_engine import RiskSignal
from utils.helpers import RISK_THRESHOLDS, risk_level_from_score


class ExplanationEngine:
    """Generates explanations for risk assessments"""

    def generate_location_explanation(
        self,
        risk_signals: List[RiskSignal],
        overall_risk: Dict,
        priority_result: Dict
    ) -> Dict:
        """Generate comprehensive explanation for a location"""

        explanations = []
        main_reasons = []

        for signal in risk_signals:
            level = risk_level_from_score(signal.risk_score)
            if level in ("HIGH", "MEDIUM"):
                main_reasons.append(f"{signal.risk_type.capitalize()} risk is {level}")
            explanations.append({
                "type": signal.risk_type,
                "level": level,
                "reason": signal.explanation,
                "score": signal.risk_score
            })

        overall_score = overall_risk.get("overall_score", 0)

        if overall_score >= RISK_THRESHOLDS["medium_max"]:
            overall_summary = "This location requires immediate attention. Multiple risk factors are elevated."
        elif overall_score >= RISK_THRESHOLDS["low_max"]:
            overall_summary = "This location shows moderate risk levels. Monitoring recommended."
        else:
            overall_summary = "This location is currently within normal risk parameters."

        priority_level = priority_result.get("priority_level", "P3 - MONITOR")
        priority_reasons = priority_result.get("reasons", [])

        return {
            "overall_summary": overall_summary,
            "main_reasons": main_reasons,
            "detailed_explanations": explanations,
            "priority_explanation": {
                "level": priority_level,
                "reasons": priority_reasons
            },
            "data_sources": [s.data_source for s in risk_signals]
        }
