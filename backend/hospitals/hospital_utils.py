import asyncio
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

async def run_hospital_pipeline(symptoms_text: str, hospital_name: str, specialization: str):
    # Route dynamically
    extracted_symptoms = extract_symptoms(symptoms_text)
    selected_doctors = route_doctors(extracted_symptoms)

    # Force specialization
    if "Cardiac" in specialization and "cardiologist" not in selected_doctors:
        selected_doctors.append("cardiologist")
    if "Emergency" in specialization and "neurologist" not in selected_doctors:
        selected_doctors.append("neurologist")

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

    results = await asyncio.gather(*tasks)

    doctor_opinions = {}
    for name, result in zip(task_names, results):
        doctor_opinions[name] = result

    aggregated_diagnosis = aggregate_beliefs(doctor_opinions)

    test_recommendations = []
    for doc, result in doctor_opinions.items():
        test_recommendations.extend(result.get("tests", []))
    
    cost_optimization_result = optimize_tests(test_recommendations)
    cost_optimized_plan = cost_optimization_result["detailed_plan"]

    # Incorporate specialization bias into reasoning prompt if needed (handled simply as a context wrapper)
    modified_symptoms = f"[{hospital_name} - {specialization} Perspective]: {symptoms_text}"

    final_reasoning = await generate_final_reasoning(
        modified_symptoms, 
        doctor_opinions, 
        aggregated_diagnosis, 
        cost_optimized_plan
    )

    final_diagnosis_str = final_reasoning.get("final_diagnosis", "Unknown")
    symptom_severity = min(0.9, len(extracted_symptoms) * 0.15 + 0.3)
    confidence_data = calculate_confidence(doctor_opinions, final_diagnosis_str, symptom_severity)
    risk_level = calculate_risk(final_diagnosis_str)

    return {
        "hospital_name": hospital_name,
        "specialization": specialization,
        "diagnosis": final_diagnosis_str,
        "confidence": confidence_data["confidence"],
        "risk": risk_level,
        "tests": cost_optimization_result["recommended_tests"],
        "raw_doctor_opinions": doctor_opinions,
        "raw_aggregated_diagnosis": aggregated_diagnosis,
        "raw_reasoning": final_reasoning.get("reasoning", "")
    }
