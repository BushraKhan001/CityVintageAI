"""
Charts Component - City Vantage AI
Dark-themed visualization components
"""

import streamlit as st
import pandas as pd
from typing import Dict, List
from components.theme import COLORS, get_risk_color


def render_priority_table(priority_results: List, title: str = "Priority Queue"):
    """Render priority queue in a responsive dark-native layout"""
    if not priority_results:
        st.info("No priority data available.")
        return

    st.subheader(title)
    header = st.columns([0.5, 2.1, 1.4, 0.8, 1.3, 3.2])
    for column, label in zip(header, ["Rank", "Location", "Priority", "Score", "Top Risk", "Reason"]):
        column.caption(label.upper())

    for index, priority in enumerate(priority_results, 1):
        top_signal = max(priority.risk_signals, key=lambda signal: signal["score"]) if priority.risk_signals else None
        row = st.columns([0.5, 2.1, 1.4, 0.8, 1.3, 3.2])
        row[0].markdown(f"**{index}**")
        row[1].markdown(f"**{priority.location_name}**")
        row[2].markdown(f"**{priority.priority_level}**")
        row[3].markdown(f"**{priority.priority_score:.1f}**")
        row[4].write(top_signal["type"].capitalize() if top_signal else "N/A")
        row[5].write(priority.reasons[0] if priority.reasons else "N/A")
        st.divider()


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
