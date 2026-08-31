"""
City Vantage AI — Urban Intelligence & Decision-Support Platform for Karachi
Bano Qabil × Alibaba.com × Alkhidmat Hackathon
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.data_loader import load_locations, load_flood_data, load_traffic_data
from models.flood_model import get_flood_model
from models.traffic_model import get_traffic_model
from models.pothole_model import get_pothole_model
from services.risk_engine import RiskEngine
from services.priority_engine import PriorityEngine
from services.explanation_engine import ExplanationEngine
from services.recommendation_engine import RecommendationEngine
from components.theme import COLORS, GLOBAL_CSS, get_risk_color
from components.map import render_map
from components.dashboard import (
    render_risk_status_card, render_metric_row, render_priority_badge,
    render_recommendation_list, render_explanation_block, render_data_provenance,
    render_section_header, render_kpi_row
)
from components.location_view import (
    render_location_header, render_risk_cards, render_flood_detail,
    render_traffic_detail, render_overall_risk, render_priority_detail,
    render_recommendations
)
from components.charts import (
    render_priority_table, render_model_metrics, render_feature_importance,
    render_risk_comparison
)

st.set_page_config(
    page_title="City Vantage AI",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject dark theme CSS
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Initialize Engines ──────────────────────────────────────────────
@st.cache_resource
def init_models():
    flood_model = get_flood_model()
    traffic_model = get_traffic_model()
    pothole_model = get_pothole_model()
    return flood_model, traffic_model, pothole_model


risk_engine = RiskEngine()
priority_engine = PriorityEngine()
explanation_engine = ExplanationEngine()
recommendation_engine = RecommendationEngine()


# ── Compute all location intelligence ───────────────────────────────
@st.cache_data(ttl=300)
def compute_all_intelligence():
    """Pre-compute risk, priority, and recommendations for all locations"""
    try:
        locations_df = load_locations()
    except Exception as e:
        return None

    flood_model, traffic_model, pothole_model = init_models()
    results = {}

    for _, loc in locations_df.iterrows():
        loc_id = loc["location_id"]
        risk_signals = []

        # Flood risk
        flood_result = None
        try:
            flood_df = load_flood_data()
            loc_flood = flood_df[flood_df["location_id"] == loc_id]
            if not loc_flood.empty:
                current = loc_flood.iloc[-1]
                features = {
                    "rainfall_1h": current["rainfall_1h"],
                    "rainfall_3h": current["rainfall_3h"],
                    "rainfall_24h": current["rainfall_24h"],
                    "previous_rainfall": current["previous_rainfall"],
                    "historical_flood": current["historical_flood"],
                    "drainage_capacity": current["drainage_capacity"],
                    "soil_saturation": current["soil_saturation"]
                }
                flood_result = flood_model.predict(features)
                if flood_result:
                    signal = risk_engine.create_risk_signal(
                        location_id=loc_id,
                        risk_type="flood",
                        risk_score=flood_result["risk_score"],
                        explanation=flood_result["explanation"],
                        confidence_or_model_status=flood_result["model_status"],
                        data_source="Demonstration dataset with simulated historical patterns",
                        details=flood_result
                    )
                    risk_signals.append(signal)
        except Exception:
            pass

        # Traffic risk
        traffic_result = None
        try:
            traffic_df = load_traffic_data()
            loc_traffic = traffic_df[traffic_df["location_id"] == loc_id]
            if not loc_traffic.empty:
                current = loc_traffic.iloc[-1]
                features = {
                    "hour": int(current["hour"]),
                    "day_of_week": int(current["day_of_week"]),
                    "is_rush_hour": int(current["is_rush_hour"]),
                    "road_work": int(current["road_work"])
                }
                traffic_result = traffic_model.predict(features)
                if traffic_result:
                    signal = risk_engine.create_risk_signal(
                        location_id=loc_id,
                        risk_type="traffic",
                        risk_score=traffic_result["risk_score"],
                        explanation=traffic_result["explanation"],
                        confidence_or_model_status=traffic_result["model_status"],
                        data_source="Demonstration data — not live Karachi traffic",
                        details=traffic_result
                    )
                    risk_signals.append(signal)
        except Exception:
            pass

        # Overall risk
        overall_risk = risk_engine.calculate_overall_risk(risk_signals)

        # Priority
        priority_result = priority_engine.calculate_priority(
            location_id=loc_id,
            location_name=loc["name"],
            risk_signals=risk_signals,
            exposure=loc["exposure"],
            historical_vulnerability=loc["historical_vulnerability"],
            overall_risk_score=overall_risk["overall_score"]
        )

        # Explanation
        explanation = explanation_engine.generate_location_explanation(
            risk_signals=risk_signals,
            overall_risk=overall_risk,
            priority_result={
                "priority_level": priority_result.priority_level,
                "reasons": priority_result.reasons
            }
        )

        # Recommendations
        recommendations = recommendation_engine.generate_recommendations(
            risk_signals=risk_signals,
            overall_risk=overall_risk
        )

        results[loc_id] = {
            "location": loc.to_dict(),
            "risk_signals": risk_signals,
            "flood_result": flood_result,
            "traffic_result": traffic_result,
            "overall_risk": overall_risk,
            "priority_result": priority_result,
            "explanation": explanation,
            "recommendations": recommendations
        }

    return results


# ── Sidebar ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 0.5rem 0 1.5rem 0;">
        <div style="font-size: 1.1rem; font-weight: 700; color: {COLORS['text_primary']};
                    letter-spacing: -0.02em;">CITY VANTAGE</div>
        <div style="font-size: 0.65rem; color: {COLORS['accent_primary']};
                    text-transform: uppercase; letter-spacing: 0.15em;
                    font-weight: 600; margin-top: 0.15rem;">AI Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Live Map",
            "Flood Intelligence",
            "Traffic Intelligence",
            "Road Intelligence",
            "Priority Queue",
            "Data & Models",
        ],
        label_visibility="collapsed"
    )

    st.markdown(f"""
    <div style="position: absolute; bottom: 1.5rem; left: 1rem; right: 1rem;">
        <div style="font-size: 0.65rem; color: {COLORS['text_muted']}; line-height: 1.5;">
            Bano Qabil × Alibaba.com × Alkhidmat<br>
            Decision-support tool — not automated decision-making
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Load intelligence ──────────────────────────────────────────────
intelligence = compute_all_intelligence()

if intelligence is None:
    st.error("Failed to initialize the system. Please check data files.")
    st.stop()

# ── Top bar ─────────────────────────────────────────────────────────
high_risk_count = sum(
    1 for r in intelligence.values()
    if r["overall_risk"]["overall_level"] == "HIGH"
)
urgent_count = sum(
    1 for r in intelligence.values()
    if r["priority_result"].priority_level == "P1 - URGENT"
)

st.markdown(f"""
<div style="
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.75rem 0 1rem 0;
    border-bottom: 1px solid {COLORS['border_subtle']};
    margin-bottom: 1.5rem;
">
    <div>
        <h1 style="margin: 0; font-size: 1.5rem; font-weight: 700;
            color: {COLORS['text_primary']}; letter-spacing: -0.02em;">{page}</h1>
        <div style="font-size: 0.8rem; color: {COLORS['text_muted']}; margin-top: 0.15rem;">
            Urban Intelligence & Decision-Support Platform — Karachi
        </div>
    </div>
    <div style="display: flex; gap: 1.5rem; align-items: center;">
        <div style="text-align: right;">
            <div style="font-size: 0.65rem; color: {COLORS['text_muted']};
                        text-transform: uppercase; letter-spacing: 0.08em;">High Risk</div>
            <div style="font-size: 1.25rem; font-weight: 700;
                        color: {COLORS['risk_high']};">{high_risk_count}</div>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 0.65rem; color: {COLORS['text_muted']};
                        text-transform: uppercase; letter-spacing: 0.08em;">Urgent</div>
            <div style="font-size: 1.25rem; font-weight: 700;
                        color: {COLORS['priority_urgent']};">{urgent_count}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Session state ───────────────────────────────────────────────────
if "selected_location" not in st.session_state:
    st.session_state.selected_location = None

location_names = [f"{r['location']['name']} ({r['location']['location_id']})" for r in intelligence.values()]


def get_loc_id_from_selection(selected: str) -> str:
    """Extract location ID from selection string"""
    return selected.split("(")[-1].rstrip(")")


# ── Pages ──────────────────────────────────────────────────────────

# ── OVERVIEW ───────────────────────────────────────────────────────
if page == "Overview":
    medium_risk_count = sum(
        1 for r in intelligence.values()
        if r["overall_risk"]["overall_level"] == "MEDIUM"
    )
    total_locations = len(intelligence)

    render_kpi_row([
        {"label": "Monitored Locations", "value": total_locations},
        {"label": "High Risk", "value": high_risk_count, "delta": f"{high_risk_count} locations", "delta_positive": False},
        {"label": "Medium Risk", "value": medium_risk_count},
        {"label": "Urgent Priority", "value": urgent_count, "delta": f"{urgent_count} need attention", "delta_positive": False},
    ])

    st.markdown("---")

    # Map + Priority side by side
    col_map, col_priority = st.columns([3, 2])

    with col_map:
        render_section_header("City Risk Map", "Click markers to view location intelligence")
        risk_data = {
            loc_id: {
                "risk_score": r["overall_risk"]["overall_score"],
                "risk_level": r["overall_risk"]["overall_level"]
            }
            for loc_id, r in intelligence.items()
        }
        locations_list = [r["location"] for r in intelligence.values()]
        render_map(locations_list, risk_data, height=450)

    with col_priority:
        render_section_header("Priority Queue", "What needs attention first")
        priority_list = priority_engine.rank_locations(
            [r["priority_result"] for r in intelligence.values()]
        )
        for i, pr in enumerate(priority_list[:6], 1):
            color = get_risk_color("HIGH" if pr.priority_score >= 70 else "MEDIUM" if pr.priority_score >= 40 else "LOW")
            st.markdown(f"""
            <div style="
                display: flex; align-items: center; gap: 0.75rem;
                padding: 0.75rem; margin-bottom: 0.5rem;
                background: {COLORS['surface_default']};
                border: 1px solid {COLORS['border_default']};
                border-radius: 6px;
                border-left: 3px solid {color};
            ">
                <div style="
                    font-size: 0.75rem; font-weight: 700;
                    color: {COLORS['text_muted']};
                    min-width: 1.5rem;
                ">#{i}</div>
                <div style="flex: 1;">
                    <div style="font-size: 0.85rem; font-weight: 600;
                                color: {COLORS['text_primary']};">{pr.location_name}</div>
                    <div style="font-size: 0.7rem; color: {COLORS['text_secondary']};">
                        {pr.reasons[0] if pr.reasons else ''}</div>
                </div>
                <div style="
                    font-size: 1.1rem; font-weight: 700;
                    color: {color};
                ">{pr.priority_score:.0f}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size: 0.75rem; color: {COLORS['text_muted']}; padding: 0.5rem 0;">
        ⚠️ <strong>Data Limitation:</strong> This platform uses demonstration datasets.
        Flood data contains simulated historical patterns. Traffic data is simulated.
        Results should not be used for actual emergency decisions.
    </div>
    """, unsafe_allow_html=True)


# ── LIVE MAP ───────────────────────────────────────────────────────
elif page == "Live Map":
    render_section_header("Risk Map", "Where is the risk? Click on any location marker to view intelligence.")

    risk_data = {
        loc_id: {
            "risk_score": r["overall_risk"]["overall_score"],
            "risk_level": r["overall_risk"]["overall_level"]
        }
        for loc_id, r in intelligence.items()
    }
    locations_list = [r["location"] for r in intelligence.values()]
    map_data = render_map(locations_list, risk_data, height=550)

    st.markdown("---")
    render_section_header("Location Detail", "Select a location to view intelligence")

    selected = st.selectbox("Choose location:", location_names, key="map_loc")
    if selected:
        loc_id = get_loc_id_from_selection(selected)
        loc_data = intelligence.get(loc_id)
        if loc_data:
            render_location_header(loc_data["location"])

            signals_dict = [
                {"risk_type": s.risk_type, "risk_score": s.risk_score, "risk_level": s.risk_level}
                for s in loc_data["risk_signals"]
            ]
            render_risk_cards(signals_dict)
            render_overall_risk(loc_data["overall_risk"])
            render_priority_detail(loc_data["priority_result"])

            # Explanation (now wired!)
            if loc_data["explanation"]:
                render_explanation_block(loc_data["explanation"])

            top_recs = recommendation_engine.get_top_recommendations(loc_data["recommendations"])
            render_recommendation_list(top_recs)


# ── FLOOD INTELLIGENCE ─────────────────────────────────────────────
elif page == "Flood Intelligence":
    render_section_header("Flood Intelligence", "AI-powered flood risk assessment using Random Forest classification")

    selected = st.selectbox("Select Location:", location_names, key="flood_loc")
    if selected:
        loc_id = get_loc_id_from_selection(selected)
        loc_data = intelligence.get(loc_id)

        if loc_data and loc_data["flood_result"]:
            render_flood_detail(loc_data["flood_result"])

            flood_model, _, _ = init_models()
            importance = flood_model.get_feature_importance()
            if importance:
                render_feature_importance(importance)
        else:
            st.warning("No flood data available for this location.")

    st.markdown("---")
    render_section_header("Model Overview")
    flood_model, _, _ = init_models()
    if flood_model.metrics:
        render_model_metrics(flood_model.metrics, "Flood Model Evaluation")

    st.markdown(f"""
    <div style="font-size: 0.8rem; color: {COLORS['accent_warning']}; padding: 1rem 0;">
        ⚠️ <strong>Prototype Model:</strong> This flood prediction model is trained on demonstration data.
        It should not be used for actual flood emergency decisions.
    </div>
    """, unsafe_allow_html=True)


# ── TRAFFIC INTELLIGENCE ───────────────────────────────────────────
elif page == "Traffic Intelligence":
    render_section_header("Traffic Intelligence", "Traffic congestion prediction and analysis")

    selected = st.selectbox("Select Location:", location_names, key="traffic_loc")
    if selected:
        loc_id = get_loc_id_from_selection(selected)
        loc_data = intelligence.get(loc_id)

        if loc_data and loc_data["traffic_result"]:
            render_traffic_detail(loc_data["traffic_result"])
        else:
            st.warning("No traffic data available for this location.")

    st.markdown("---")
    render_section_header("Predict Traffic for Custom Time")

    col1, col2 = st.columns(2)
    with col1:
        custom_hour = st.slider("Hour of Day:", 0, 23, 12)
    with col2:
        custom_day = st.selectbox("Day of Week:", list(range(7)), format_func=lambda x: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][x])

    if st.button("Predict Traffic"):
        _, traffic_model, _ = init_models()
        features = {
            "hour": custom_hour,
            "day_of_week": custom_day,
            "is_rush_hour": 1 if (7 <= custom_hour <= 9 or 17 <= custom_hour <= 19) else 0,
            "road_work": 0
        }
        result = traffic_model.predict(features)
        if result:
            st.success(f"Predicted Congestion: **{result['congestion_level']}** (Risk Score: {result['risk_score']:.1f}/100)")
            st.info(result["explanation"])

    st.markdown(f"""
    <div style="font-size: 0.8rem; color: {COLORS['accent_warning']}; padding: 1rem 0;">
        ⚠️ <strong>Demonstration Data:</strong> Traffic predictions are based on simulated data.
        This is NOT live Karachi traffic data.
    </div>
    """, unsafe_allow_html=True)


# ── ROAD INTELLIGENCE ──────────────────────────────────────────────
elif page == "Road Intelligence":
    render_section_header("Road Intelligence", "Computer vision-based road surface analysis")

    _, _, pothole_model = init_models()

    if not pothole_model.is_available:
        st.markdown(f"""
        <div style="
            background: {COLORS['accent_warning']}15;
            border: 1px solid {COLORS['accent_warning']}40;
            border-radius: 6px;
            padding: 1.25rem;
            margin: 1rem 0;
        ">
            <div style="font-size: 0.9rem; font-weight: 600; color: {COLORS['accent_warning']}; margin-bottom: 0.5rem;">
                Capability Limitation
            </div>
            <div style="font-size: 0.85rem; color: {COLORS['text_secondary']}; line-height: 1.6;">
                Computer vision libraries (OpenCV) are not available in this environment.
                Road surface analysis is limited. This does not affect the core flood risk and traffic intelligence pipeline.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Upload Road Image")
    uploaded_file = st.file_uploader(
        "Upload an image of a road surface:",
        type=["jpg", "jpeg", "png"],
    )

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Road Image", use_container_width=True)

        if st.button("Analyze Road Surface"):
            if pothole_model.is_available:
                import tempfile
                import os

                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name

                result = pothole_model.analyze_image(tmp_path)
                os.unlink(tmp_path)

                if result and "error" not in result:
                    st.markdown("### Analysis Results")
                    st.metric("Detections", result.get("detection_count", 0))
                    st.metric("Confidence", f"{result.get('confidence', 0):.2f}")
                    st.metric("Risk Score", f"{result.get('risk_score', 0):.1f}/100")
                    st.info(result.get("explanation", ""))
                    st.warning("⚠️ **Prototype:** This uses basic edge detection, not a trained deep learning model.")
                else:
                    st.error(result.get("error", "Analysis failed"))
            else:
                st.warning("Computer vision analysis is not available.")


# ── PRIORITY QUEUE ─────────────────────────────────────────────────
elif page == "Priority Queue":
    render_section_header("Priority Queue", "Locations ranked by priority for human decision-makers")

    priority_list = priority_engine.rank_locations(
        [r["priority_result"] for r in intelligence.values()]
    )
    render_priority_table(priority_list)

    st.markdown("---")
    render_section_header("Detailed Priority Breakdown")

    for i, pr in enumerate(priority_list, 1):
        with st.expander(f"#{i} — {pr.location_name} ({pr.priority_level})"):
            st.markdown(f"**Priority Score:** {pr.priority_score:.1f}/100")

            if pr.reasons:
                st.markdown("**Why this priority?**")
                for reason in pr.reasons:
                    st.markdown(f"- {reason}")

            if pr.risk_signals:
                st.markdown("**Risk Signals:**")
                for rs in pr.risk_signals:
                    st.markdown(f"- {rs['type'].capitalize()}: {rs['score']:.1f}/100 ({rs['level']})")

            loc_data = intelligence.get(pr.location_id)
            if loc_data:
                top_recs = recommendation_engine.get_top_recommendations(loc_data["recommendations"])
                if top_recs:
                    st.markdown("**Recommended Actions:**")
                    for rec in top_recs:
                        st.markdown(f"- {rec}")

    st.markdown("---")
    render_section_header("Priority Configuration")
    for factor, weight in priority_engine.weights.items():
        st.markdown(f"- {factor.replace('_', ' ').title()}: {weight:.0%}")


# ── DATA & MODELS ──────────────────────────────────────────────────
elif page == "Data & Models":
    render_section_header("Data & Models", "Technical details, data provenance, and model information")

    st.markdown("### Data Sources")
    st.markdown("""
    | Dataset | Type | Source | Status |
    |---------|------|--------|--------|
    | Locations | Demonstration | 10 Karachi areas selected for monitoring | Not official government data |
    | Flood | Demonstration/Simulated | Simulated historical patterns | Prototype |
    | Traffic | Simulated | Simulated congestion patterns | NOT live traffic data |
    """)

    st.markdown("---")
    st.markdown("### Models")

    flood_model, traffic_model, pothole_model = init_models()

    st.markdown("#### Flood Risk Model")
    st.markdown(f"- **Type:** Random Forest Classifier")
    st.markdown(f"- **Status:** {'✅ Trained' if flood_model.is_trained else '❌ Not trained'}")
    st.markdown(f"- **Features:** {', '.join(flood_model.feature_names)}")
    if flood_model.metrics:
        render_model_metrics(flood_model.metrics)

    st.markdown("#### Traffic Prediction Model")
    st.markdown(f"- **Type:** Random Forest Regressor")
    st.markdown(f"- **Status:** {'✅ Trained' if traffic_model.is_trained else '❌ Not trained'}")
    st.markdown(f"- **Features:** {', '.join(traffic_model.feature_names)}")
    if traffic_model.metrics:
        render_model_metrics(traffic_model.metrics)

    st.markdown("#### Road Surface Analysis")
    st.markdown(f"- **Type:** Basic Computer Vision (Edge Detection)")
    st.markdown(f"- **Status:** {'✅ Available' if pothole_model.is_available else '⚠️ Limited'}")
    st.markdown(f"- **Limitation:** Uses basic edge detection, not a trained deep learning model")

    st.markdown("---")
    render_section_header("Risk Engine Configuration")

    st.markdown("**Risk Weights (Overall Risk Calculation):**")
    for risk_type, weight in risk_engine.risk_weights.items():
        st.markdown(f"- {risk_type.capitalize()}: {weight:.0%}")

    st.markdown("**Priority Weights:**")
    for factor, weight in priority_engine.weights.items():
        st.markdown(f"- {factor.replace('_', ' ').title()}: {weight:.0%}")

    st.markdown("**Risk Level Thresholds:**")
    st.markdown("- 0–39: LOW")
    st.markdown("- 40–69: MEDIUM")
    st.markdown("- 70–100: HIGH")

    st.markdown("---")
    render_section_header("Known Limitations")
    st.markdown("""
    1. **Demonstration Data:** All datasets are simulated for demonstration purposes
    2. **No Live Data:** The system does not connect to live weather, traffic, or government data feeds
    3. **Prototype Models:** ML models are trained on limited demonstration data
    4. **Basic CV:** Road surface analysis uses basic edge detection, not deep learning
    5. **Limited Scope:** Only 10 locations in Karachi are monitored
    6. **Not for Emergency Use:** This system should NOT be used for actual emergency response
    """)

    render_section_header("Architecture")
    st.markdown("""
    ```
    DATA LAYER (CSV datasets)
        ↓
    AI / ML MODELS (Random Forest)
        ↓
    RISK ENGINE (Unified risk scoring)
        ↓
    EXPLANATION ENGINE (Feature-based explanations)
        ↓
    PRIORITY ENGINE (Weighted ranking)
        ↓
    RECOMMENDATION ENGINE (Deterministic rules)
        ↓
    CITY INTELLIGENCE UI (Streamlit)
        ↓
    HUMAN DECISION
    ```
    """)
