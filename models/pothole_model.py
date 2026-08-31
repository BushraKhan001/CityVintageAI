"""
Pothole Detection Model - City Vantage AI
Computer vision model for road surface analysis
"""

from typing import Dict, Optional


class PotholeModel:
    """Pothole detection using computer vision"""

    def __init__(self):
        self.is_available = False
        self.model = None
        self._check_availability()

    def _check_availability(self):
        """Check if pothole detection is available"""
        try:
            import cv2
            from PIL import Image
            self.is_available = True
        except ImportError:
            self.is_available = False

    def analyze_image(self, image_path: str) -> Optional[Dict]:
        """Analyze road image for potholes"""
        if not self.is_available:
            return None

        try:
            import cv2

            img = cv2.imread(image_path)
            if img is None:
                return {"error": "Could not load image"}

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            potential_potholes = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if 100 < area < 5000:
                    x, y, w, h = cv2.boundingRect(contour)
                    potential_potholes.append({
                        "x": int(x),
                        "y": int(y),
                        "width": int(w),
                        "height": int(h),
                        "area": int(area)
                    })

            detection_count = len(potential_potholes)

            if detection_count > 0:
                confidence = min(0.85, 0.5 + (detection_count * 0.1))
                risk_score = min(100, detection_count * 25)
            else:
                confidence = 0.75
                risk_score = 15

            from utils.helpers import risk_level_from_score
            risk_level = risk_level_from_score(risk_score)

            return {
                "detections": potential_potholes,
                "detection_count": detection_count,
                "confidence": float(confidence),
                "risk_score": float(risk_score),
                "risk_level": risk_level,
                "model_status": "Basic CV edge detection (prototype)",
                "explanation": f"Detected {detection_count} potential road surface anomalies using edge detection"
            }

        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}


_model_instance = None


def get_pothole_model() -> PotholeModel:
    """Get or create pothole model instance"""
    global _model_instance
    if _model_instance is None:
        _model_instance = PotholeModel()
    return _model_instance
