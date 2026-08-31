"""
Data loader for City Vantage AI
Loads and validates all datasets
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional

DATA_DIR = Path(__file__).parent.parent / "data"


def load_locations() -> pd.DataFrame:
    """Load monitored locations dataset"""
    path = DATA_DIR / "locations.csv"
    if not path.exists():
        raise FileNotFoundError(f"Locations data not found at {path}")
    
    df = pd.read_csv(path)
    required = ["location_id", "name", "latitude", "longitude", "area", "exposure", "historical_vulnerability"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in locations: {missing}")
    
    return df


def load_flood_data() -> pd.DataFrame:
    """Load flood risk dataset"""
    path = DATA_DIR / "flood.csv"
    if not path.exists():
        raise FileNotFoundError(f"Flood data not found at {path}")
    
    df = pd.read_csv(path)
    required = ["location_id", "rainfall_1h", "rainfall_3h", "rainfall_24h", 
                "previous_rainfall", "historical_flood"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in flood data: {missing}")
    
    return df


def load_traffic_data() -> pd.DataFrame:
    """Load traffic dataset"""
    path = DATA_DIR / "traffic.csv"
    if not path.exists():
        raise FileNotFoundError(f"Traffic data not found at {path}")
    
    df = pd.read_csv(path)
    required = ["location_id", "hour", "day_of_week", "traffic_volume", "congestion"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in traffic data: {missing}")
    
    return df


def get_location_by_id(location_id: str, locations_df: Optional[pd.DataFrame] = None) -> dict:
    """Get location details by ID"""
    if locations_df is None:
        locations_df = load_locations()
    
    loc = locations_df[locations_df["location_id"] == location_id]
    if loc.empty:
        raise ValueError(f"Location {location_id} not found")
    
    return loc.iloc[0].to_dict()


def get_current_conditions(location_id: str) -> dict:
    """Get current conditions for a location (latest data point)"""
    try:
        flood_df = load_flood_data()
        flood_current = flood_df[flood_df["location_id"] == location_id].iloc[-1].to_dict()
    except:
        flood_current = None
    
    try:
        traffic_df = load_traffic_data()
        traffic_current = traffic_df[traffic_df["location_id"] == location_id].iloc[-1].to_dict()
    except:
        traffic_current = None
    
    return {
        "flood": flood_current,
        "traffic": traffic_current
    }
