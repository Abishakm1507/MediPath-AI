import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

from agents.general_physician import GeneralPhysicianAgent
from agents.pulmonologist import PulmonologistAgent
from agents.infectious_specialist import InfectiousSpecialistAgent
from agents.cardiologist import CardiologistAgent
from agents.neurologist import NeurologistAgent
from agents.gastroenterologist import GastroenterologistAgent
from router.symptom_analyzer import extract_symptoms
from router.specialty_router import route_doctors
from aggregator.belief_aggregator import aggregate_beliefs
from optimizer.cost_optimizer import optimize_tests
from reasoning.final_reasoning import generate_final_reasoning
from reasoning.confidence_engine import calculate_confidence
from reasoning.risk_engine import calculate_risk
from reasoning.explainable_ai import generate_explanation
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="MediPath AI", description="Multi-Doctor AI Second Opinion + Cost-Optimized Diagnosis Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from models.request_models import AnalyzeRequest
@app.post("/analyze")
async def analyze_symptoms(request: AnalyzeRequest):
    symptoms_text = request.symptoms

    # Route dynamically based on extracted symptoms
    extracted_symptoms = extract_symptoms(symptoms_text)
    selected_doctors = route_doctors(extracted_symptoms)

    tasks = []
    task_names = []

    if "general" in selected_doctors:
        tasks.append(GeneralPhysicianAgent().analyze(symptoms_text))
        task_names.append("General Physician")
    if "cardiologist" in selected_doctors:
        tasks.append(CardiologistAgent().analyze(symptoms_text))
        task_names.append("Cardiologist")
    if "pulmonologist" in selected_doctors:
        tasks.append(PulmonologistAgent().analyze(symptoms_text))
        task_names.append("Pulmonologist")
    if "infectious_specialist" in selected_doctors:
        tasks.append(InfectiousSpecialistAgent().analyze(symptoms_text))
        task_names.append("Infectious Specialist")
    if "neurologist" in selected_doctors:
        tasks.append(NeurologistAgent().analyze(symptoms_text))
        task_names.append("Neurologist")
    if "gastroenterologist" in selected_doctors:
        tasks.append(GastroenterologistAgent().analyze(symptoms_text))
        task_names.append("Gastroenterologist")

    # Run Agents in Parallel
    results = await asyncio.gather(*tasks)
    
    doctor_opinions = {}
    for name, result in zip(task_names, results):
        doctor_opinions[name] = result

    # Aggregate Beliefs
    aggregated_diagnosis = aggregate_beliefs(doctor_opinions)

    # Cost Optimization
    test_recommendations = []
    for doc, result in doctor_opinions.items():
        test_recommendations.extend(result.get("tests", []))
    
    cost_optimization_result = optimize_tests(test_recommendations, budget=request.budget)
    cost_optimized_plan = cost_optimization_result["detailed_plan"]

    # Final Reasoning
    final_reasoning = await generate_final_reasoning(
        symptoms_text, 
        doctor_opinions, 
        aggregated_diagnosis, 
        cost_optimized_plan
    )
    
    final_diagnosis_str = final_reasoning.get("final_diagnosis", "Unknown")
    
    # Phase 5: Confidence, Risk and Explainability
    symptom_severity = min(0.9, len(extracted_symptoms) * 0.15 + 0.3)  # basic severity heuristic
    confidence_data = calculate_confidence(doctor_opinions, final_diagnosis_str, symptom_severity)
    risk_level = calculate_risk(final_diagnosis_str)
    
    explanation_text = generate_explanation(
        symptoms=symptoms_text,
        doctor_outputs=doctor_opinions,
        final_diagnosis=final_diagnosis_str,
        confidence_score=confidence_data["confidence"],
        agreement_score=confidence_data["agreement_score"],
        risk_level=risk_level
    )

    return {
        "selected_doctors": task_names,
        "doctor_opinions": doctor_opinions,
        "aggregated_diagnosis": aggregated_diagnosis,
        "optimized_tests": cost_optimization_result["recommended_tests"],
        "estimated_cost": cost_optimization_result["estimated_cost"],
        "final_diagnosis": final_diagnosis_str,
        "confidence": confidence_data["confidence"],
        "agreement_score": confidence_data["agreement_score"],
        "risk_level": risk_level,
        "explanation": explanation_text,
        "doctor_contributions": confidence_data.get("contributions", {})
    }
