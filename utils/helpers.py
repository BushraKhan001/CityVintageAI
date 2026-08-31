"""
Helper utilities for City Vantage AI
Centralized risk thresholds and utility functions
"""

from typing import List, Dict

# ── Risk Thresholds (single source of truth) ─────────────────────────
RISK_THRESHOLDS = {
    "low_max": 40,
    "medium_max": 70,
}

PRIORITY_THRESHOLDS = {
    "urgent_min": 75,
    "high_min": 50,
}

RISK_LEVELS = ["LOW", "MEDIUM", "HIGH"]
PRIORITY_LEVELS = ["P1 - URGENT", "P2 - HIGH", "P3 - MONITOR"]


def normalize_score(value: float, min_val: float = 0, max_val: float = 100) -> float:
    """Normalize a value to 0-100 range"""
    if max_val == min_val:
        return 0
    normalized = ((value - min_val) / (max_val - min_val)) * 100
    return max(0, min(100, normalized))


def risk_level_from_score(score: float) -> str:
    """Convert risk score to risk level using centralized thresholds"""
    if score < RISK_THRESHOLDS["low_max"]:
        return "LOW"
    elif score < RISK_THRESHOLDS["medium_max"]:
        return "MEDIUM"
    else:
        return "HIGH"


def priority_level_from_score(score: float) -> str:
    """Convert priority score to priority level using centralized thresholds"""
    if score >= PRIORITY_THRESHOLDS["urgent_min"]:
        return "P1 - URGENT"
    elif score >= PRIORITY_THRESHOLDS["high_min"]:
        return "P2 - HIGH"
    else:
        return "P3 - MONITOR"


def format_percentage(value: float) -> str:
    """Format a value as percentage"""
    return f"{value:.1f}%"


def calculate_weighted_average(components: List[Dict], weights: Dict[str, float]) -> float:
    """Calculate weighted average from risk components"""
    available = [c for c in components if c.get("available", True)]
    if not available:
        return 0

    total_weight = sum(weights.get(c["type"], 1.0) for c in available)
    if total_weight == 0:
        return 0

    weighted_sum = sum(c["score"] * weights.get(c["type"], 1.0) for c in available)
    return weighted_sum / total_weight
