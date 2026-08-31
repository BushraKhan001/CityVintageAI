"""
Recommendation Engine - City Vantage AI
Generates actionable recommendations based on risk assessment
"""

from typing import Dict, List
from services.risk_engine import RiskSignal


class RecommendationEngine:
    """Generates recommendations for risk mitigation"""
    
    def __init__(self):
        self.recommendation_templates = {
            "flood": {
                "HIGH": [
                    "Inspect and clear drainage systems immediately",
                    "Deploy water pumps to vulnerable areas",
                    "Issue public advisory for flood preparedness",
                    "Monitor rainfall continuously",
                    "Prepare emergency response resources"
                ],
                "MEDIUM": [
                    "Check drainage capacity",
                    "Monitor rainfall forecasts",
                    "Prepare sandbags in vulnerable areas",
                    "Alert maintenance teams"
                ],
                "LOW": [
                    "Continue routine monitoring",
                    "Schedule regular drainage inspection"
                ]
            },
            "traffic": {
                "HIGH": [
                    "Deploy traffic management personnel",
                    "Activate alternative route suggestions",
                    "Investigate bottleneck causes",
                    "Consider traffic signal optimization",
                    "Issue congestion alerts"
                ],
                "MEDIUM": [
                    "Monitor traffic flow",
                    "Check for incidents or road work",
                    "Prepare traffic management plan"
                ],
                "LOW": [
                    "Continue routine monitoring",
                    "No immediate action required"
                ]
            },
            "road": {
                "HIGH": [
                    "Inspect road surface immediately",
                    "Deploy repair crew for pothole patching",
                    "Install temporary warning signs",
                    "Schedule comprehensive road assessment"
                ],
                "MEDIUM": [
                    "Schedule road inspection",
                    "Monitor road condition",
                    "Plan maintenance activity"
                ],
                "LOW": [
                    "Continue routine monitoring",
                    "No immediate action required"
                ]
            }
        }
    
    def generate_recommendations(
        self,
        risk_signals: List[RiskSignal],
        overall_risk: Dict
    ) -> Dict:
        """
        Generate recommendations based on risk signals
        
        Returns dict with recommendations organized by risk type and overall
        """
        
        recommendations_by_type = {}
        all_recommendations = []
        
        # Generate recommendations for each risk signal
        for signal in risk_signals:
            risk_type = signal.risk_type
            risk_level = signal.risk_level
            
            type_recommendations = self.recommendation_templates.get(risk_type, {}).get(risk_level, [])
            
            recommendations_by_type[risk_type] = {
                "level": risk_level,
                "score": signal.risk_score,
                "recommendations": type_recommendations
            }
            
            all_recommendations.extend(type_recommendations)
        
        # Generate overall recommendations based on overall risk
        overall_level = overall_risk.get("overall_level", "LOW")
        overall_score = overall_risk.get("overall_score", 0)
        
        overall_recommendations = []
        
        if overall_level == "HIGH":
            overall_recommendations = [
                "Coordinate multi-department response",
                "Prioritize this location for immediate attention",
                "Allocate additional resources",
                "Establish monitoring protocol"
            ]
        elif overall_level == "MEDIUM":
            overall_recommendations = [
                "Monitor closely",
                "Prepare contingency plans",
                "Coordinate with relevant departments"
            ]
        else:
            overall_recommendations = [
                "Continue routine monitoring"
            ]
        
        return {
            "by_type": recommendations_by_type,
            "overall": {
                "level": overall_level,
                "score": overall_score,
                "recommendations": overall_recommendations
            },
            "all_recommendations": all_recommendations
        }
    
    def get_top_recommendations(self, recommendations: Dict, top_n: int = 3) -> List[str]:
        """Get top N recommendations across all types"""
        
        all_recs = recommendations.get("all_recommendations", [])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_recs = []
        for rec in all_recs:
            if rec not in seen:
                seen.add(rec)
                unique_recs.append(rec)
        
        return unique_recs[:top_n]
