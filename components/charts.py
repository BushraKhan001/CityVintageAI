"""
Charts Component - City Vantage AI
Dark-themed visualization components
"""

import streamlit as st
import pandas as pd
from typing import Dict, List
from components.theme import COLORS, get_risk_color, get_priority_color


def render_priority_table(priority_results: List, title: str = "Priority Queue"):
    """Render priority queue table with dark theme"""
    if not priority_results:
        st.info("No priority data available.")
        return

    st.markdown(f"""
    <div style="font-size: 1.1rem; font-weight: 600; color: {COLORS['text_primary']};
                margin-bottom: 1rem;">{title}</div>
    """, unsafe_allow_html=True)

    rows = []
    for i, pr in enumerate(priority_results, 1):
        top_signal = max(pr.risk_signals, key=lambda x: x["score"]) if pr.risk_signals else None
        rows.append({
            "Rank": i,
            "Location": pr.location_name,
            "Priority": pr.priority_level,
            "Score": f"{pr.priority_score:.1f}",
            "Top Risk": top_signal["type"].capitalize() if top_signal else "N/A",
            "Reason": pr.reasons[0] if pr.reasons else "N/A"
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_risk_comparison(risk_signals: List[Dict], title: str = "Risk Comparison"):
    """Render risk comparison bar chart with dark theme"""
    if not risk_signals:
        st.info("No risk data available.")
        return

    st.markdown(f"""
    <div style="font-size: 1.1rem; font-weight: 600; color: {COLORS['text_primary']};
                margin-bottom: 1rem;">{title}</div>
    """, unsafe_allow_html=True)

    data = {
        "Risk Type": [s.get("risk_type", "Unknown").capitalize() for s in risk_signals],
        "Risk Score": [s.get("risk_score", 0) for s in risk_signals]
    }
    chart_df = pd.DataFrame(data)
    st.bar_chart(chart_df.set_index("Risk Type"))


def render_model_metrics(metrics: Dict, title: str = "Model Performance"):
    """Render model evaluation metrics with dark theme"""
    if not metrics:
        st.info("No model metrics available.")
        return

    st.markdown(f"""
    <div style="font-size: 1.1rem; font-weight: 600; color: {COLORS['text_primary']};
                margin-bottom: 1rem;">{title}</div>
    """, unsafe_allow_html=True)

    cols = st.columns(min(len(metrics), 4))
    for i, (key, value) in enumerate(metrics.items()):
        with cols[i % len(cols)]:
            st.metric(
                key.replace("_", " ").title(),
                f"{value:.3f}" if isinstance(value, float) else value
            )


def render_feature_importance(importance: Dict, title: str = "Feature Importance"):
    """Render feature importance chart with dark theme"""
    if not importance:
        st.info("No feature importance data available.")
        return

    st.markdown(f"""
    <div style="font-size: 1.1rem; font-weight: 600; color: {COLORS['text_primary']};
                margin-bottom: 1rem;">{title}</div>
    """, unsafe_allow_html=True)

    df = pd.DataFrame({
        "Feature": list(importance.keys()),
        "Importance": list(importance.values())
    })
    st.bar_chart(df.set_index("Feature"))
