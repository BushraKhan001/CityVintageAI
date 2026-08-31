"""
Map Component - City Vantage AI
Dark-themed interactive Folium map for Karachi risk visualization
"""

import folium
from streamlit_folium import st_folium
import streamlit as st
from typing import List, Dict, Optional

from components.theme import COLORS, get_risk_color

KARACHI_CENTER = [24.8850, 67.0100]

# Dark map tile style
DARK_TILES = "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
DARK_ATTR = '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>'


def create_karachi_map(
    locations: List[Dict],
    risk_data: Optional[Dict] = None,
    height: int = 500,
    zoom_start: int = 11
) -> folium.Map:
    """Create interactive Karachi map with risk markers on dark basemap"""

    m = folium.Map(
        location=KARACHI_CENTER,
        zoom_start=zoom_start,
        tiles=None,
        height=height,
        width="100%",
    )

    folium.TileLayer(tiles=DARK_TILES, attr=DARK_ATTR, name="Dark").add_to(m)

    if risk_data is None:
        risk_data = {}

    for loc in locations:
        loc_id = loc.get("location_id", "")
        name = loc.get("name", "Unknown")
        lat = loc.get("latitude")
        lon = loc.get("longitude")

        if lat is None or lon is None:
            continue

        info = risk_data.get(loc_id, {})
        risk_level = info.get("risk_level", "LOW")
        risk_score = info.get("risk_score", 0)
        color = get_risk_color(risk_level)

        radius = max(10, min(24, risk_score / 4))

        popup_html = f"""
        <div style="
            min-width: 220px;
            font-family: 'Inter', -apple-system, sans-serif;
            background: {COLORS['bg_secondary']};
            color: {COLORS['text_primary']};
            padding: 16px;
            border-radius: 8px;
            border: 1px solid {COLORS['border_default']};
        ">
            <div style="font-size: 14px; font-weight: 600; margin-bottom: 8px;">{name}</div>
            <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 6px;">
                <div style="
                    width: 8px; height: 8px; border-radius: 50%;
                    background: {color}; box-shadow: 0 0 6px {color};
                "></div>
                <span style="font-size: 12px; color: {color}; font-weight: 600;">{risk_level}</span>
                <span style="font-size: 12px; color: {COLORS['text_secondary']};">| {risk_score:.0f}/100</span>
            </div>
            <div style="font-size: 11px; color: {COLORS['text_muted']};">{loc.get('area', '')}</div>
        </div>
        """

        # Outer glow ring
        folium.CircleMarker(
            location=[lat, lon],
            radius=radius + 4,
            color=color,
            fillColor=color,
            fillOpacity=0.15,
            weight=0,
        ).add_to(m)

        # Main marker
        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{name} — {risk_level} Risk ({risk_score:.0f})",
            color=color,
            fillColor=color,
            fillOpacity=0.6,
            weight=2,
        ).add_to(m)

    return m


def render_map(
    locations: List[Dict],
    risk_data: Optional[Dict] = None,
    height: int = 500,
):
    """Render the interactive map in Streamlit"""
    m = create_karachi_map(locations, risk_data, height=height)
    map_data = st_folium(m, width=None, height=height, returned_objects=["last_clicked"])
    return map_data
