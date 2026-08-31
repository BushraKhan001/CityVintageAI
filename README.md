# City Vantage AI

**AI-Powered Urban Intelligence & Decision-Support Platform for Karachi**

Built for **Bano Qabil × Alibaba.com × Alkhidmat Hackathon**

---

## Problem

Urban authorities in Karachi face challenges in:
- Identifying emerging risks across multiple domains (flood, traffic, infrastructure)
- Understanding why certain areas are high-risk
- Prioritizing limited resources effectively
- Making data-informed decisions quickly

## Solution

City Vantage AI provides a unified intelligence platform that:

1. **Collects** urban data from multiple sources
2. **Analyzes** risks using AI/ML models
3. **Detects** and predicts risk levels
4. **Explains** why risks are high
5. **Prioritizes** locations for attention
6. **Recommends** actions for human decision-makers

This is a **decision-support tool** — it supports human authorities, not replaces them.

---

## Architecture

```
DATA LAYER (CSV datasets)
    ↓
AI / ML MODELS (Random Forest classifiers/regressors)
    ↓
RISK ENGINE (Unified risk scoring 0-100)
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

---

## MVP Features

### Core (P0)
- ✅ Professional Streamlit UI with 7 pages
- ✅ Interactive Karachi map with 10 monitored locations
- ✅ Flood risk prediction using Random Forest classifier
- ✅ Traffic congestion prediction using Random Forest regressor
- ✅ Unified risk scoring (0-100 with Low/Medium/High levels)
- ✅ Feature-based risk explanations
- ✅ Priority engine with transparent ranking
- ✅ Deterministic recommendation engine
- ✅ Data provenance and limitation labels
- ✅ Complete end-to-end demo flow

### Additional (P1)
- ✅ Multiple risk signals per location
- ✅ Model evaluation metrics
- ✅ Feature importance visualization
- ✅ Custom time predictions

### Road Intelligence (Limited)
- ⚠️ Basic CV edge detection (not deep learning)
- ⚠️ Requires OpenCV (may not be available in all environments)

---

## Data Sources & Limitations

| Dataset | Type | Source | Status |
|---------|------|--------|--------|
| Locations | Demonstration | 10 Karachi areas | Not official government data |
| Flood | Simulated | Historical patterns | Prototype |
| Traffic | Simulated | Congestion patterns | NOT live traffic |

**Important:** All datasets are simulated for demonstration. This system should NOT be used for actual emergency response.

---

## Models

### Flood Risk Model
- **Type:** Random Forest Classifier
- **Features:** rainfall_1h, rainfall_3h, rainfall_24h, previous_rainfall, historical_flood, drainage_capacity, soil_saturation
- **Output:** Probability → Risk Score (0-100) → Risk Level (Low/Medium/High)
- **Evaluation:** Accuracy, Precision, Recall, F1 Score

### Traffic Prediction Model
- **Type:** Random Forest Regressor
- **Features:** hour, day_of_week, is_rush_hour, road_work
- **Output:** Congestion Level → Risk Score → Risk Level
- **Evaluation:** MAE, RMSE, R² Score

### Road Surface Analysis
- **Type:** Basic Computer Vision (Edge Detection)
- **Status:** Prototype — uses basic CV, not trained deep learning model
- **Limitation:** Not suitable for production use

---

## Installation

### Requirements
```bash
pip install -r requirements.txt
```

### Dependencies
- Python 3.8+
- Streamlit
- Pandas, NumPy
- Scikit-learn
- Folium, streamlit-folium
- Pillow (optional, for road image analysis)

---

## Running the Application

```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

---

## Testing

Run all tests:
```bash
pytest tests/ -v
```

Run specific test suite:
```bash
pytest tests/test_flood.py -v
pytest tests/test_risk.py -v
pytest tests/test_priority.py -v
```

---

## Demo Flow (3-5 minutes)

1. **Overview** — "What is happening?"
   - See city-wide risk summary
   - View high-risk location count

2. **Risk Map** — "Where is the risk?"
   - Interactive Karachi map
   - Click locations to see risk levels

3. **Location Selection** — "What is happening here?"
   - View all risk signals for a location
   - See overall risk assessment

4. **Flood Intelligence** — "Why is the risk high?"
   - See model predictions
   - Read feature-based explanations
   - View model performance metrics

5. **Priority Queue** — "Which location comes first?"
   - Ranked locations by priority
   - Transparent reasons for ranking

6. **Recommendations** — "What should be investigated?"
   - Actionable recommendations
   - Organized by risk type

7. **Human Decision** — "The system supports the authority"
   - Clear data limitations
   - Not automated decision-making

---

## Known Limitations

1. **Demonstration Data:** All datasets are simulated
2. **No Live Data:** No connection to live weather, traffic, or government feeds
3. **Prototype Models:** Trained on limited demonstration data
4. **Basic CV:** Road analysis uses edge detection, not deep learning
5. **Limited Scope:** Only 10 locations monitored
6. **Not for Emergency Use:** Should NOT be used for actual emergency response

---

## Future Extensions

- Integration with live weather APIs
- Real-time traffic data feeds
- Deep learning models for road surface analysis
- Expanded location coverage
- Mobile-responsive bottom navigation
- Multi-language support (Urdu/English)
- Citizen complaint integration
- Historical trend analysis
- Predictive scenario modeling
- Government API integration

---

## Project Structure

```
city-vantage-ai/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # This file
│
├── data/
│   ├── locations.csv        # Monitored locations
│   ├── flood.csv           # Flood risk data
│   └── traffic.csv         # Traffic data
│
├── models/
│   ├── flood_model.py      # Flood ML model
│   ├── traffic_model.py    # Traffic ML model
│   └── pothole_model.py    # Road CV model
│
├── services/
│   ├── risk_engine.py          # Unified risk scoring
│   ├── priority_engine.py      # Priority ranking
│   ├── explanation_engine.py   # Risk explanations
│   └── recommendation_engine.py # Recommendations
│
├── components/
│   ├── map.py              # Interactive map
│   ├── dashboard.py        # Dashboard widgets
│   ├── location_view.py    # Location details
│   └── charts.py           # Visualizations
│
├── utils/
│   ├── data_loader.py      # Data loading
│   └── helpers.py          # Utilities
│
└── tests/
    ├── test_flood.py       # Flood model tests
    ├── test_risk.py        # Risk engine tests
    └── test_priority.py    # Priority engine tests
```

---

## License

Built for hackathon demonstration purposes.

---

## Team

Built with ❤️ for urban intelligence and better decision-making.

**City Vantage AI** — Supporting human authorities with AI-powered insights.
