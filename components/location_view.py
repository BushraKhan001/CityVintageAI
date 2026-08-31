"""
Location View Component - City Vantage AI
Detailed location intelligence panel with dark theme
"""

import streamlit as st
from typing import Dict, List
from components.theme import COLORS, get_risk_color
from components.dashboard import (
    render_risk_status_card, render_metric_row, render_priority_badge,
    render_recommendation_list, render_explanation_block, render_data_provenance,
    render_section_header
)


def render_location_header(location: Dict):
    """Render location header with dark theme"""
    exposure_color = {
        "High": COLORS["risk_high"],
        "Medium": COLORS["risk_medium"],
        "Low": COLORS["risk_low"],
    }.get(location.get("exposure", ""), COLORS["text_muted"])

    st.markdown(f"""
    <div style="padding: 1rem 0; margin-bottom: 1.5rem;">
        <h2 style="margin: 0; font-size: 1.35rem; font-weight: 600;
            color: {COLORS['text_primary']};">{location.get('name', 'Unknown')}</h2>
        <div style="display: flex; gap: 1.5rem; margin-top: 0.5rem; font-size: 0.8rem;">
            <span style="color: {COLORS['text_muted']};">{location.get('area', '')}</span>
            <span>Exposure: <span style="color: {exposure_color}; font-weight: 600;">{location.get('exposure', 'N/A')}</span></span>
            <span>Vulnerability: <span style="color: {COLORS['text_primary']}; font-weight: 600;">{location.get('historical_vulnerability', 0):.2f}</span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_risk_cards(risk_signals: List[Dict]):
    """Render risk status cards for all risk types"""
    if not risk_signals:
        st.info("No risk signals available for this location.")
        return

    cols = st.columns(len(risk_signals))
    for i, signal in enumerate(risk_signals):
        with cols[i]:
            render_risk_status_card(
                title=f"{signal.get('risk_type', 'Risk').capitalize()} Risk",
                score=signal.get("risk_score", 0),
                level=signal.get("risk_level", "LOW")
            )


def render_flood_detail(flood_result: Dict):
    """Render detailed flood risk information with dark theme"""
    render_section_header("Flood Intelligence")

    col1, col2 = st.columns(2)

    with col1:
        render_metric_row("Risk Score", f"{flood_result.get('risk_score', 0):.1f}/100")
        render_metric_row("Risk Level", flood_result.get("risk_level", "N/A"))
        render_metric_row("Probability", f"{flood_result.get('probability', 0):.3f}")

    with col2:
        metrics = flood_result.get("metrics", {})
        if metrics:
            render_metric_row("Model Accuracy", f"{metrics.get('accuracy', 0):.2%}")
            render_metric_row("F1 Score", f"{metrics.get('f1_score', 0):.2f}")
            render_metric_row("Test Samples", str(metrics.get("test_samples", 0)))

    st.markdown(f"""
    <div style="background: {COLORS['surface_default']}; border: 1px solid {COLORS['border_default']};
                border-radius: 6px; padding: 1rem; margin: 1rem 0;">
        <div style="font-size: 0.7rem; color: {COLORS['accent_primary']};
                    text-transform: uppercase; letter-spacing: 0.08em;
                    margin-bottom: 0.5rem; font-weight: 600;">EXPLANATION</div>
        <div style="font-size: 0.85rem; color: {COLORS['text_primary']};
                    line-height: 1.6;">{flood_result.get("explanation", "No explanation available")}</div>
    </div>
    """, unsafe_allow_html=True)

    render_data_provenance(
        "Demonstration dataset with simulated historical patterns",
        flood_result.get("model_status", "Random Forest Classifier")
    )


def render_traffic_detail(traffic_result: Dict):
    """Render detailed traffic risk information with dark theme"""
    render_section_header("Traffic Intelligence")

    col1, col2 = st.columns(2)

    with col1:
        render_metric_row("Congestion Level", traffic_result.get("congestion_level", "N/A"))
        render_metric_row("Risk Score", f"{traffic_result.get('risk_score', 0):.1f}/100")
        render_metric_row("Risk Level", traffic_result.get("risk_level", "N/A"))

    with col2:
        metrics = traffic_result.get("metrics", {})
        if metrics:
            render_metric_row("MAE", f"{metrics.get('mae', 0):.2f}")
            render_metric_row("R² Score", f"{metrics.get('r2', 0):.2f}")

    st.markdown(f"""
    <div style="background: {COLORS['surface_default']}; border: 1px solid {COLORS['border_default']};
                border-radius: 6px; padding: 1rem; margin: 1rem 0;">
        <div style="font-size: 0.7rem; color: {COLORS['accent_primary']};
                    text-transform: uppercase; letter-spacing: 0.08em;
                    margin-bottom: 0.5rem; font-weight: 600;">EXPLANATION</div>
        <div style="font-size: 0.85rem; color: {COLORS['text_primary']};
                    line-height: 1.6;">{traffic_result.get("explanation", "No explanation available")}</div>
    </div>
    """, unsafe_allow_html=True)

    render_data_provenance(
        traffic_result.get("data_provenance", "Demonstration data — not live Karachi traffic"),
        traffic_result.get("model_status", "Random Forest Regressor")
    )


def render_overall_risk(overall_risk: Dict):
    """Render overall risk assessment with dark theme"""
    render_section_header("Overall Risk Assessment")

    score = overall_risk.get("overall_score", 0)
    level = overall_risk.get("overall_level", "LOW")
    render_risk_status_card("OVERALL RISK", score, level)

    components = overall_risk.get("components", [])
    if components:
        for comp in components:
            color = get_risk_color(comp.get("level", "LOW"))
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center;
                        padding: 0.5rem 0; border-bottom: 1px solid {COLORS['border_subtle']};">
                <span style="font-size: 0.85rem; color: {COLORS['text_secondary']};">
                    {comp.get('type', '').capitalize()}</span>
                <span>
                    <span style="color: {color}; font-weight: 600; font-size: 0.9rem;">
                        {comp.get('score', 0):.1f}</span>
                    <span style="color: {COLORS['text_muted']}; font-size: 0.75rem; margin-left: 0.5rem;">
                        (w: {comp.get('weight', 0):.2f})</span>
                </span>
            </div>
            """, unsafe_allow_html=True)


def render_priority_detail(priority_result):
    """Render priority information with dark theme"""
    render_section_header("Priority Assessment")

    render_priority_badge(priority_result.priority_level, priority_result.priority_score)

    st.markdown(f"""
    <div style="margin-top: 0.75rem; font-size: 0.85rem; color: {COLORS['text_secondary']};">
        Priority Score: <span style="color: {COLORS['text_primary']}; font-weight: 600;">
        {priority_result.priority_score:.1f}/100</span>
    </div>
    """, unsafe_allow_html=True)

    if priority_result.reasons:
        st.markdown(f"""
        <div style="font-size: 0.75rem; color: {COLORS['text_muted']};
                    text-transform: uppercase; letter-spacing: 0.05em;
                    margin: 1rem 0 0.5rem; font-weight: 600;">
            Why this priority?
        </div>
        """, unsafe_allow_html=True)
        for reason in priority_result.reasons:
            st.markdown(
                f'<div style="padding: 0.25rem 0; font-size: 0.85rem; color: {COLORS["text_secondary"]};">'
                f'<span style="color: {COLORS["accent_primary"]};">›</span> {reason}</div>',
                unsafe_allow_html=True
            )


def render_recommendations(recommendations: Dict):
    """Render recommendations section with dark theme"""
    render_section_header("Recommended Actions")

    overall = recommendations.get("overall", {})
    overall_recs = overall.get("recommendations", [])
    if overall_recs:
        render_recommendation_list(overall_recs, "Overall Recommendations")

    by_type = recommendations.get("by_type", {})
    if by_type:
        for risk_type, data in by_type.items():
            recs = data.get("recommendations", [])
            if recs:
                with st.expander(f"{risk_type.capitalize()} Actions"):
                    render_recommendation_list(recs, f"{risk_type.capitalize()} Recommendations")
