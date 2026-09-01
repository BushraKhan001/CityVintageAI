"""
Dashboard Component - City Vantage AI
Dark-themed dashboard widgets and status cards
"""

import streamlit as st
from typing import List, Dict
from components.theme import (
    COLORS, risk_card_css, priority_badge_css, kpi_card_css,
    info_banner_css, provenance_banner_css, section_header_css,
    get_risk_color
)


def render_risk_status_card(title: str, score: float, level: str):
    """Render a risk status card with dark theme"""
    st.markdown(risk_card_css(title, score, level), unsafe_allow_html=True)


def render_metric_row(label: str, value: str, subtitle: str = ""):
    """Render a metric row with Streamlit's native metric widget"""
    st.metric(label, value, delta=subtitle or None)


def render_priority_badge(priority_level: str, priority_score: float):
    """Render priority badge with dark theme"""
    st.markdown(priority_badge_css(priority_level, priority_score), unsafe_allow_html=True)


def render_kpi_row(kpis: List[Dict]):
    """Render a row of KPI cards"""
    cols = st.columns(len(kpis))
    for i, kpi in enumerate(kpis):
        with cols[i]:
            st.markdown(
                kpi_card_css(
                    kpi.get("label", ""),
                    str(kpi.get("value", "")),
                    kpi.get("delta"),
                    kpi.get("delta_positive", True)
                ),
                unsafe_allow_html=True
            )


def render_section_header(title: str, subtitle: str = None):
    """Render section header"""
    st.markdown(section_header_css(title, subtitle), unsafe_allow_html=True)


def render_recommendation_list(recommendations: List[str], title: str = "Recommended Actions"):
    """Render a list of recommendations with dark theme"""
    if not recommendations:
        st.info("No specific recommendations at this time.")
        return

    st.markdown(f"**{title}**")
    for i, rec in enumerate(recommendations, 1):
        st.markdown(
            f'<div style="padding: 0.4rem 0; font-size: 0.85rem; color: {COLORS["text_secondary"]};">'
            f'<span style="color: {COLORS["accent_primary"]}; font-weight: 600;">{i}.</span> {rec}'
            f'</div>',
            unsafe_allow_html=True
        )


def render_explanation_block(explanation: Dict):
    """Render detailed explanation block with dark theme"""
    st.markdown(
        section_header_css("Why is this risk level assigned?"),
        unsafe_allow_html=True,
    )

    overall_summary = explanation.get("overall_summary", "")
    if overall_summary:
        st.markdown(info_banner_css(overall_summary, "info"), unsafe_allow_html=True)

    main_reasons = explanation.get("main_reasons", [])
    if main_reasons:
        st.markdown(
            f'<div style="font-size: 0.8rem; color: {COLORS["text_secondary"]}; '
            f'text-transform: uppercase; letter-spacing: 0.05em; margin: 1rem 0 0.5rem;">'
            f'Key Factors</div>',
            unsafe_allow_html=True
        )
        for reason in main_reasons:
            st.markdown(
                f'<div style="padding: 0.3rem 0; font-size: 0.85rem; color: {COLORS["text_primary"]};">'
                f'<span style="color: {COLORS["accent_primary"]};">›</span> {reason}</div>',
                unsafe_allow_html=True
            )

    detailed = explanation.get("detailed_explanations", [])
    if detailed:
        with st.expander("Detailed breakdown"):
            for exp in detailed:
                color = get_risk_color(exp.get("level", "LOW"))
                st.markdown(
                    f'<div style="padding: 0.75rem 0; border-bottom: 1px solid {COLORS["border_subtle"]};">'
                    f'<div style="font-size: 0.85rem; font-weight: 600; color: {COLORS["text_primary"]};">'
                    f'{exp.get("type", "").capitalize()} '
                    f'<span style="color: {color}; font-size: 0.75rem;">{exp.get("level", "")}</span> '
                    f'<span style="color: {COLORS["text_muted"]}; font-weight: 400;">({exp.get("score", 0):.1f}/100)</span>'
                    f'</div>'
                    f'<div style="font-size: 0.8rem; color: {COLORS["text_secondary"]}; margin-top: 0.25rem;">'
                    f'{exp.get("reason", "")}</div></div>',
                    unsafe_allow_html=True
                )


def render_data_provenance(data_source: str, model_status: str):
    """Render data provenance banner with dark theme"""
    st.markdown(provenance_banner_css(data_source, model_status), unsafe_allow_html=True)
