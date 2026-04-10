RISK_LEVEL = {
    "Heart Attack": "High",
    "Stroke": "High",
    "Pulmonary Embolism": "High",
    "Tuberculosis": "High",
    "Pneumonia": "Medium",
    "Asthma": "Medium",
    "Flu": "Low",
    "Anxiety": "Low",
    "Acid Reflux": "Low",
    "Viral Infection": "Low"
}

def calculate_risk(diagnosis: str) -> str:
    if not diagnosis:
        return "Unknown"
        
    for key, level in RISK_LEVEL.items():
        if key.lower() in diagnosis.lower() or diagnosis.lower() in key.lower():
            return level
            
    return "Medium"  # Default fallback
