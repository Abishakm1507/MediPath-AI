"""
Visualization Engine - Generates chart-ready data for frontend visualization
Supports: Bar charts, Pie charts, Line charts, Risk meters
"""

from typing import List, Dict, Any


def generate_confidence_chart(conditions: List[str], confidences: List[float]) -> dict:
    """
    Generate bar chart data for confidence distribution.
    
    Returns:
        Chart.js compatible format
    """
    # Normalize confidences to percentages
    total = sum(confidences) if confidences else 1
    normalized = [(c / total * 100) for c in confidences] if total > 0 else confidences
    
    return {
        "type": "bar",
        "title": "Diagnostic Confidence Distribution",
        "data": {
            "labels": conditions[:5],  # Top 5 conditions
            "datasets": [
                {
                    "label": "Confidence Score (%)",
                    "data": normalized[:5],
                    "backgroundColor": [
                        "rgba(59, 130, 246, 0.8)",   # Blue
                        "rgba(139, 92, 246, 0.8)",   # Purple
                        "rgba(34, 197, 94, 0.8)",    # Green
                        "rgba(249, 115, 22, 0.8)",   # Orange
                        "rgba(239, 68, 68, 0.8)"     # Red
                    ],
                    "borderColor": [
                        "rgb(59, 130, 246)",
                        "rgb(139, 92, 246)",
                        "rgb(34, 197, 94)",
                        "rgb(249, 115, 22)",
                        "rgb(239, 68, 68)"
                    ],
                    "borderWidth": 1,
                    "borderRadius": 4
                }
            ]
        }
    }


def generate_doctor_chart(doctor_opinions: List[Dict[str, Any]]) -> dict:
    """
    Generate pie chart data for doctor opinion distribution.
    
    Returns:
        Chart.js compatible pie chart format
    """
    
    doctor_names = []
    contributions = []
    
    for opinion in doctor_opinions:
        doctor_name = opinion.get('hospital_name', 'Unknown')
        confidence = float(opinion.get('confidence', 0))
        
        doctor_names.append(doctor_name)
        contributions.append(confidence)
    
    # Normalize contributions
    total = sum(contributions) if contributions else 1
    normalized = [(c / total * 100) for c in contributions] if total > 0 else contributions
    
    return {
        "type": "pie",
        "title": "Doctor Opinion Distribution",
        "data": {
            "labels": doctor_names,
            "datasets": [
                {
                    "label": "Contribution to Consensus",
                    "data": normalized,
                    "backgroundColor": [
                        "rgba(59, 130, 246, 0.8)",   # Blue
                        "rgba(139, 92, 246, 0.8)",   # Purple
                        "rgba(34, 197, 94, 0.8)",    # Green
                        "rgba(249, 115, 22, 0.8)",   # Orange
                        "rgba(239, 68, 68, 0.8)"     # Red
                    ],
                    "borderColor": [
                        "rgb(59, 130, 246)",
                        "rgb(139, 92, 246)",
                        "rgb(34, 197, 94)",
                        "rgb(249, 115, 22)",
                        "rgb(239, 68, 68)"
                    ],
                    "borderWidth": 2
                }
            ]
        }
    }


def generate_risk_chart(conditions: List[str], risk_levels: List[str]) -> dict:
    """
    Generate risk level visualization.
    
    Returns:
        Risk assessment data with colors
    """
    
    risk_colors = {
        'High': '#ef4444',      # Red
        'Medium': '#f59e0b',    # Orange
        'Low': '#10b981'        # Green
    }
    
    risk_data = []
    for condition, risk in zip(conditions, risk_levels):
        risk_data.append({
            "condition": condition,
            "risk_level": risk,
            "color": risk_colors.get(risk, '#6b7280'),
            "numeric_value": {'High': 3, 'Medium': 2, 'Low': 1}.get(risk, 2)
        })
    
    return {
        "type": "risk_meter",
        "title": "Risk Assessment by Condition",
        "data": risk_data,
        "summary": {
            "high_risk_count": len([r for r in risk_levels if r == 'High']),
            "medium_risk_count": len([r for r in risk_levels if r == 'Medium']),
            "low_risk_count": len([r for r in risk_levels if r == 'Low'])
        }
    }


def generate_symptom_impact(symptom_importance: Dict[str, int]) -> dict:
    """
    Generate symptom importance visualization.
    
    Returns:
        Symptom impact chart data
    """
    
    # Sort by importance
    sorted_symptoms = sorted(
        symptom_importance.items(),
        key=lambda x: x[1],
        reverse=True
    )[:8]  # Top 8 symptoms
    
    return {
        "type": "horizontal_bar",
        "title": "Symptom Importance in Diagnosis",
        "data": {
            "labels": [s[0].title() for s in sorted_symptoms],
            "datasets": [
                {
                    "label": "Importance Score",
                    "data": [s[1] for s in sorted_symptoms],
                    "backgroundColor": [
                        f"rgba(59, 130, 246, {0.9 - (i * 0.08)})"
                        for i in range(len(sorted_symptoms))
                    ],
                    "borderRadius": 4
                }
            ]
        }
    }


def generate_timeline_risk(risk_level: str) -> dict:
    """
    Generate risk over time visualization.
    
    Returns:
        Timeline chart data
    """
    
    # Risk progression based on severity
    risk_profiles = {
        'High': [90, 80, 70, 60, 50, 40, 35],
        'Medium': [60, 55, 45, 35, 25, 20, 15],
        'Low': [30, 25, 20, 15, 12, 10, 8]
    }
    
    risk_values = risk_profiles.get(risk_level, risk_profiles['Medium'])
    
    return {
        "type": "line",
        "title": "Risk Level Progression Over Time",
        "data": {
            "labels": ["Immediate", "6 hrs", "12 hrs", "24 hrs", "2 days", "5 days", "7+ days"],
            "datasets": [
                {
                    "label": f"{risk_level} Risk Timeline",
                    "data": risk_values,
                    "borderColor": {
                        'High': 'rgb(239, 68, 68)',
                        'Medium': 'rgb(249, 115, 22)',
                        'Low': 'rgb(34, 197, 94)'
                    }.get(risk_level, 'rgb(107, 114, 128)'),
                    "backgroundColor": {
                        'High': 'rgba(239, 68, 68, 0.1)',
                        'Medium': 'rgba(249, 115, 22, 0.1)',
                        'Low': 'rgba(34, 197, 94, 0.1)'
                    }.get(risk_level, 'rgba(107, 114, 128, 0.1)'),
                    "borderWidth": 3,
                    "tension": 0.4,
                    "fill": True,
                    "pointRadius": 5,
                    "pointBackgroundColor": {
                        'High': 'rgb(239, 68, 68)',
                        'Medium': 'rgb(249, 115, 22)',
                        'Low': 'rgb(34, 197, 94)'
                    }.get(risk_level, 'rgb(107, 114, 128)')
                }
            ]
        }
    }


def generate_all_visualizations(
    conditions: List[str],
    confidences: List[float],
    risk_levels: List[str],
    doctor_opinions: List[Dict[str, Any]],
    symptom_importance: Dict[str, int],
    overall_risk: str
) -> dict:
    """
    Generate all visualization data at once.
    
    Returns:
        Comprehensive visualization package
    """
    
    return {
        "confidence_chart": generate_confidence_chart(conditions, confidences),
        "doctor_chart": generate_doctor_chart(doctor_opinions),
        "risk_chart": generate_risk_chart(conditions, risk_levels),
        "symptom_impact": generate_symptom_impact(symptom_importance),
        "timeline_risk": generate_timeline_risk(overall_risk),
        "generated_at": "timestamp",
        "visualization_count": 5
    }
