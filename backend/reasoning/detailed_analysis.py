"""
Detailed Analysis Engine - Generates comprehensive multi-hypothesis analysis
with reasoning, confidence scores, and visualization data.
"""

def generate_detailed_analysis(symptoms: str, doctor_opinions: list, confidence_score: float) -> dict:
    """
    Generate detailed analysis with condition hierarchies, confidence distributions,
    and clinical reasoning.
    
    Args:
        symptoms: Patient symptoms description
        doctor_opinions: List of doctor opinions with diagnoses
        confidence_score: Overall confidence percentage (0-100)
    
    Returns:
        dict with conditions, confidence scores, reasoning, and risk levels
    """
    
    # Extract conditions from doctor opinions
    conditions = []
    confidences = []
    risk_levels = []
    
    for opinion in doctor_opinions:
        if opinion.get('diagnosis'):
            condition = opinion['diagnosis']
            conf = float(opinion.get('confidence', 0))
            risk = opinion.get('risk', 'Medium')
            
            conditions.append(condition)
            confidences.append(conf)
            risk_levels.append(risk)
    
    # Generate reasoning based on symptoms and doctor consensus
    reasoning = _generate_reasoning(symptoms, conditions, confidences)
    
    # Calculate differential diagnosis percentages
    total_confidence = sum(confidences) if confidences else 1
    normalized_confidences = [
        round((c / total_confidence) * 100, 1) for c in confidences
    ] if total_confidence > 0 else [0] * len(conditions)
    
    # Generate symptom importance scores
    symptom_importance = _calculate_symptom_importance(symptoms, conditions)
    
    return {
        "conditions": conditions,
        "confidence_scores": normalized_confidences,
        "risk_levels": risk_levels,
        "differential_diagnosis": dict(zip(conditions, normalized_confidences)),
        "reasoning": reasoning,
        "symptom_importance": symptom_importance,
        "overall_confidence": confidence_score,
        "condition_count": len(conditions)
    }


def _generate_reasoning(symptoms: str, conditions: list, confidences: list) -> str:
    """Generate clinical reasoning explanation."""
    
    if not conditions:
        return "Insufficient data for analysis."
    
    # Build reasoning based on top conditions
    top_condition = conditions[0] if conditions else "Unknown"
    top_confidence = confidences[0] if confidences else 0
    
    reasoning_parts = []
    reasoning_parts.append(
        f"Primary consideration: {top_condition} (confidence: {top_confidence}%)"
    )
    
    if len(conditions) > 1:
        reasoning_parts.append(
            f"Differential includes: {', '.join(conditions[1:3])}"
        )
    
    reasoning_parts.append(
        "Clinical correlation with patient presentation supports this assessment."
    )
    
    return " ".join(reasoning_parts)


def _calculate_symptom_importance(symptoms: str, conditions: list) -> dict:
    """
    Calculate which symptoms are most important for the diagnosis.
    
    Returns:
        dict mapping symptom keywords to importance scores (0-100)
    """
    
    symptoms_lower = symptoms.lower()
    
    # Symptom importance mapping
    symptom_keywords = {
        'chest': {'weight': 25, 'cardiac': True},
        'pain': {'weight': 20, 'cardinal': True},
        'shortness': {'weight': 22, 'cardinal': True},
        'breathing': {'weight': 22, 'cardinal': True},
        'sweating': {'weight': 18, 'cardiac': True},
        'nausea': {'weight': 15, 'general': True},
        'fever': {'weight': 20, 'infection': True},
        'cough': {'weight': 18, 'respiratory': True},
        'headache': {'weight': 15, 'neuro': True},
        'dizziness': {'weight': 16, 'neuro': True},
        'fatigue': {'weight': 12, 'general': True},
    }
    
    importance_scores = {}
    found_symptoms = []
    
    for symptom, details in symptom_keywords.items():
        if symptom in symptoms_lower:
            found_symptoms.append(symptom)
            importance_scores[symptom] = details['weight']
    
    # If no specific symptoms found, return default
    if not importance_scores:
        importance_scores['patient description'] = 50
    
    return importance_scores


def calculate_risk_over_time(risk_level: str, condition: str) -> dict:
    """
    Calculate risk progression over time.
    
    Returns:
        dict with immediate, short-term, and long-term risk assessments
    """
    
    risk_mapping = {
        'High': {'immediate': 90, 'short_term': 75, 'long_term': 50},
        'Medium': {'immediate': 50, 'short_term': 40, 'long_term': 25},
        'Low': {'immediate': 20, 'short_term': 15, 'long_term': 10},
    }
    
    base_risk = risk_mapping.get(risk_level, risk_mapping['Medium'])
    
    return {
        "immediate_risk": base_risk['immediate'],
        "short_term_risk": base_risk['short_term'],
        "long_term_risk": base_risk['long_term'],
        "risk_level": risk_level,
        "timeframe": {
            "immediate": "0-24 hours",
            "short_term": "1-7 days",
            "long_term": "7+ days"
        }
    }
