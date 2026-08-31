"""
Design System & Theme - City Vantage AI
Command-center style dark theme inspired by smart city platforms
"""

# ── Color Palette ────────────────────────────────────────────────────
COLORS = {
    # Backgrounds
    "bg_primary": "#0A0E1A",
    "bg_secondary": "#151B2E",
    "bg_tertiary": "#1E2642",
    "bg_elevated": "#232B45",
    
    # Surfaces
    "surface_default": "#1A2238",
    "surface_hover": "#232B45",
    "surface_active": "#2A3556",
    
    # Borders
    "border_default": "#2A3556",
    "border_subtle": "#1E2642",
    "border_accent": "#00D4FF",
    
    # Text
    "text_primary": "#E4E7EF",
    "text_secondary": "#8B95B0",
    "text_muted": "#5A6478",
    "text_inverse": "#0A0E1A",
    
    # Accents
    "accent_primary": "#00D4FF",
    "accent_secondary": "#7C5CFF",
    "accent_success": "#00E676",
    "accent_warning": "#FFB020",
    
    # Risk Levels
    "risk_critical": "#FF3B5C",
    "risk_high": "#FF6B35",
    "risk_medium": "#FFB020",
    "risk_low": "#00E676",
    
    # Priority Levels
    "priority_urgent": "#FF3B5C",
    "priority_high": "#FF6B35",
    "priority_monitor": "#00D4FF",
    
    # Map
    "map_marker_critical": "#FF3B5C",
    "map_marker_high": "#FF6B35",
    "map_marker_medium": "#FFB020",
    "map_marker_low": "#00E676",
}

# ── Risk Level Helpers ───────────────────────────────────────────────
RISK_COLORS = {
    "CRITICAL": COLORS["risk_critical"],
    "HIGH": COLORS["risk_high"],
    "MEDIUM": COLORS["risk_medium"],
    "LOW": COLORS["risk_low"],
}

PRIORITY_COLORS = {
    "P1 - URGENT": COLORS["priority_urgent"],
    "P2 - HIGH": COLORS["priority_high"],
    "P3 - MONITOR": COLORS["priority_monitor"],
}

def get_risk_color(level: str) -> str:
    """Get color for risk level"""
    return RISK_COLORS.get(level, COLORS["text_muted"])

def get_priority_color(level: str) -> str:
    """Get color for priority level"""
    return PRIORITY_COLORS.get(level, COLORS["text_muted"])

# ── Global CSS ───────────────────────────────────────────────────────
GLOBAL_CSS = f"""
<style>
/* ── Base ──────────────────────────────────────────────────────── */
.stApp {{
    background-color: {COLORS["bg_primary"]};
}}

.main .block-container {{
    padding: 1rem 2rem 2rem 2rem;
    max-width: 100%;
}}

/* ── Sidebar ───────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {{
    background-color: {COLORS["bg_secondary"]};
    border-right: 1px solid {COLORS["border_subtle"]};
    padding: 0;
}}

section[data-testid="stSidebar"] > div {{
    padding: 1.5rem 1rem;
}}

section[data-testid="stSidebar"] .stMarkdown {{
    color: {COLORS["text_primary"]};
}}

section[data-testid="stSidebar"] .stRadio > label {{
    color: {COLORS["text_secondary"]};
    font-size: 0.85rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}}

section[data-testid="stSidebar"] .stRadio > div {{
    gap: 0.25rem;
}}

section[data-testid="stSidebar"] .stRadio > div > label {{
    background: transparent;
    border: none;
    border-radius: 6px;
    padding: 0.6rem 0.8rem;
    color: {COLORS["text_secondary"]};
    font-size: 0.9rem;
    transition: all 0.2s ease;
}}

section[data-testid="stSidebar"] .stRadio > div > label:hover {{
    background: {COLORS["surface_hover"]};
    color: {COLORS["text_primary"]};
}}

section[data-testid="stSidebar"] .stRadio > div > label[data-baseweb="radio"]:has(div[aria-checked="true"]) {{
    background: {COLORS["surface_active"]};
    color: {COLORS["accent_primary"]};
}}

section[data-testid="stSidebar"] .stRadio > div > label > div:first-child {{
    display: none;
}}

/* ── Typography ────────────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6 {{
    color: {COLORS["text_primary"]};
    font-weight: 600;
}}

h1 {{
    font-size: 1.75rem;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
}}

h2 {{
    font-size: 1.35rem;
    letter-spacing: -0.01em;
}}

h3 {{
    font-size: 1.1rem;
    color: {COLORS["text_secondary"]};
    font-weight: 500;
}}

p, span, div {{
    color: {COLORS["text_primary"]};
}}

/* ── Metrics ───────────────────────────────────────────────────── */
[data-testid="stMetric"] {{
    background: {COLORS["surface_default"]};
    border: 1px solid {COLORS["border_default"]};
    border-radius: 8px;
    padding: 1rem 1.25rem;
}}

[data-testid="stMetric"] label {{
    color: {COLORS["text_secondary"]};
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

[data-testid="stMetric"] [data-testid="stMetricValue"] {{
    color: {COLORS["text_primary"]};
    font-size: 1.75rem;
    font-weight: 700;
}}

[data-testid="stMetric"] [data-testid="stMetricDelta"] {{
    font-size: 0.8rem;
}}

/* ── Dataframes ────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {{
    border: 1px solid {COLORS["border_default"]};
    border-radius: 8px;
    overflow: hidden;
}}

/* ── Selectboxes & Inputs ──────────────────────────────────────── */
.stSelectbox > div > div {{
    background: {COLORS["surface_default"]};
    border: 1px solid {COLORS["border_default"]};
    border-radius: 6px;
    color: {COLORS["text_primary"]};
}}

.stSlider > div > div > div {{
    color: {COLORS["text_secondary"]};
}}

/* ── Buttons ───────────────────────────────────────────────────── */
.stButton > button {{
    background: {COLORS["accent_primary"]};
    color: {COLORS["text_inverse"]};
    border: none;
    border-radius: 6px;
    padding: 0.5rem 1.25rem;
    font-weight: 600;
    font-size: 0.875rem;
    transition: all 0.2s ease;
}}

.stButton > button:hover {{
    background: #33DDFF;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
}}

/* ── Alerts & Info ─────────────────────────────────────────────── */
.stAlert {{
    border-radius: 6px;
    border: 1px solid {COLORS["border_default"]};
}}

.stAlert[data-baseweb="notification"] {{
    background: {COLORS["surface_default"]};
}}

/* ── Expanders ─────────────────────────────────────────────────── */
.streamlit-expanderHeader {{
    background: {COLORS["surface_default"]};
    border: 1px solid {COLORS["border_default"]};
    border-radius: 6px;
    color: {COLORS["text_primary"]};
    padding: 0.75rem 1rem;
}}

.streamlit-expanderHeader:hover {{
    background: {COLORS["surface_hover"]};
}}

/* ── File Uploader ─────────────────────────────────────────────── */
[data-testid="stFileUploader"] {{
    background: {COLORS["surface_default"]};
    border: 2px dashed {COLORS["border_default"]};
    border-radius: 8px;
}}

/* ── Tabs ──────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 0.5rem;
    background: transparent;
}}

.stTabs [data-baseweb="tab"] {{
    background: {COLORS["surface_default"]};
    border: 1px solid {COLORS["border_default"]};
    border-radius: 6px;
    color: {COLORS["text_secondary"]};
    padding: 0.5rem 1rem;
}}

.stTabs [aria-selected="true"] {{
    background: {COLORS["accent_primary"]};
    color: {COLORS["text_inverse"]};
    border-color: {COLORS["accent_primary"]};
}}

/* ── Dividers ──────────────────────────────────────────────────── */
hr {{
    border-color: {COLORS["border_subtle"]};
    margin: 1.5rem 0;
}}

/* ── Scrollbar ─────────────────────────────────────────────────── */
::-webkit-scrollbar {{
    width: 8px;
    height: 8px;
}}

::-webkit-scrollbar-track {{
    background: {COLORS["bg_primary"]};
}}

::-webkit-scrollbar-thumb {{
    background: {COLORS["border_default"]};
    border-radius: 4px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: {COLORS["text_muted"]};
}}
</style>
"""

# ── Component CSS Templates ──────────────────────────────────────────

def risk_card_css(title: str, score: float, level: str) -> str:
    """Generate CSS for a risk status card"""
    color = get_risk_color(level)
    return f"""
    <div style="
        background: {COLORS['surface_default']};
        border: 1px solid {COLORS['border_default']};
        border-left: 3px solid {color};
        border-radius: 8px;
        padding: 1.25rem;
        transition: all 0.2s ease;
    ">
        <div style="
            font-size: 0.75rem;
            color: {COLORS['text_secondary']};
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.5rem;
        ">{title}</div>
        <div style="
            font-size: 2.25rem;
            font-weight: 700;
            color: {color};
            line-height: 1;
            margin-bottom: 0.25rem;
        ">{score:.0f}</div>
        <div style="
            display: inline-block;
            font-size: 0.7rem;
            font-weight: 600;
            color: {color};
            background: {color}15;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        ">{level}</div>
    </div>
    """

def priority_badge_css(level: str, score: float) -> str:
    """Generate CSS for a priority badge"""
    color = get_priority_color(level)
    return f"""
    <div style="
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: {color}20;
        border: 1px solid {color}40;
        border-radius: 20px;
        padding: 0.4rem 1rem;
    ">
        <div style="
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: {color};
            box-shadow: 0 0 8px {color};
        "></div>
        <span style="
            font-size: 0.8rem;
            font-weight: 600;
            color: {color};
            text-transform: uppercase;
            letter-spacing: 0.05em;
        ">{level}</span>
        <span style="
            font-size: 0.75rem;
            color: {COLORS['text_secondary']};
        ">({score:.1f})</span>
    </div>
    """

def kpi_card_css(label: str, value: str, delta: str = None, delta_positive: bool = True) -> str:
    """Generate CSS for a KPI card"""
    delta_color = COLORS["accent_success"] if delta_positive else COLORS["risk_high"]
    delta_html = f'<div style="font-size: 0.75rem; color: {delta_color}; margin-top: 0.25rem;">{delta}</div>' if delta else ""
    
    return f"""
    <div style="
        background: {COLORS['surface_default']};
        border: 1px solid {COLORS['border_default']};
        border-radius: 8px;
        padding: 1.25rem;
    ">
        <div style="
            font-size: 0.7rem;
            color: {COLORS['text_secondary']};
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.5rem;
        ">{label}</div>
        <div style="
            font-size: 2rem;
            font-weight: 700;
            color: {COLORS['text_primary']};
            line-height: 1;
        ">{value}</div>
        {delta_html}
    </div>
    """

def info_banner_css(message: str, variant: str = "info") -> str:
    """Generate CSS for an info banner"""
    colors = {
        "info": (COLORS["accent_primary"], COLORS["accent_primary"] + "15"),
        "warning": (COLORS["accent_warning"], COLORS["accent_warning"] + "15"),
        "danger": (COLORS["risk_critical"], COLORS["risk_critical"] + "15"),
    }
    border_color, bg_color = colors.get(variant, colors["info"])
    
    return f"""
    <div style="
        background: {bg_color};
        border: 1px solid {border_color}30;
        border-left: 3px solid {border_color};
        border-radius: 6px;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
    ">
        <div style="
            font-size: 0.85rem;
            color: {COLORS['text_primary']};
            line-height: 1.5;
        ">{message}</div>
    </div>
    """

def provenance_banner_css(source: str, model_status: str) -> str:
    """Generate CSS for data provenance banner"""
    return f"""
    <div style="
        background: {COLORS['accent_warning']}10;
        border: 1px solid {COLORS['accent_warning']}30;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        margin: 1rem 0;
    ">
        <div style="
            font-size: 0.7rem;
            color: {COLORS['accent_warning']};
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.4rem;
            font-weight: 600;
        ">DATA & MODEL INFORMATION</div>
        <div style="font-size: 0.8rem; color: {COLORS['text_secondary']}; line-height: 1.6;">
            <strong>Source:</strong> {source}<br>
            <strong>Model:</strong> {model_status}
        </div>
    </div>
    """

def section_header_css(title: str, subtitle: str = None) -> str:
    """Generate CSS for a section header"""
    subtitle_html = f'<div style="font-size: 0.85rem; color: {COLORS["text_secondary"]}; margin-top: 0.25rem;">{subtitle}</div>' if subtitle else ""
    return f"""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="
            font-size: 1.25rem;
            font-weight: 600;
            color: {COLORS['text_primary']};
            margin: 0;
            letter-spacing: -0.01em;
        ">{title}</h2>
        {subtitle_html}
    </div>
    """

def metric_row_css(label: str, value: str, subtitle: str = None) -> str:
    """Generate CSS for a metric row"""
    subtitle_html = f'<div style="font-size: 0.75rem; color: {COLORS["text_muted"]};">{subtitle}</div>' if subtitle else ""
    return f"""
    <div style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0;
        border-bottom: 1px solid {COLORS['border_subtle']};
    ">
        <div style="font-size: 0.85rem; color: {COLORS['text_secondary']};">{label}</div>
        <div style="text-align: right;">
            <div style="font-size: 0.9rem; font-weight: 600; color: {COLORS['text_primary']};">{value}</div>
            {subtitle_html}
        </div>
    </div>
    """
