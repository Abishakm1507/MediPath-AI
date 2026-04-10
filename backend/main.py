import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

from router.symptom_analyzer import extract_symptoms
from router.specialty_router import route_doctors
from hospitals.hospital_router import run_hospitals
from hospitals.hospital_aggregator import aggregate_hospital_opinions
from aggregator.belief_aggregator import aggregate_beliefs
from optimizer.cost_optimizer import optimize_tests
from reasoning.final_reasoning import generate_final_reasoning
from reasoning.confidence_engine import calculate_confidence
from reasoning.risk_engine import calculate_risk
from reasoning.explainable_ai import generate_explanation
from reasoning.detailed_analysis import generate_detailed_analysis
from visualization.visualization_engine import generate_all_visualizations
from safety.input_validator import InputValidator
from safety.missing_data_detector import MissingDataDetector
from report.clinical_report import ClinicalReportGenerator
from agents.followup_question_agent import FollowUpQuestionAgent
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

# Initialize safety and report components
input_validator = InputValidator()
missing_data_detector = MissingDataDetector()
report_generator = ClinicalReportGenerator()

# Initialize followup agent (will raise error if GROQ_API_KEY not set)
try:
    followup_agent = FollowUpQuestionAgent()
except ValueError as e:
    print(f"Warning: FollowUpQuestionAgent not initialized: {e}")
    followup_agent = None

from models.request_models import AnalyzeRequest, FollowUpRequest, ReportRequest, RefineDiagnosisRequest
@app.post("/analyze")
async def analyze_symptoms(request: AnalyzeRequest):
    # Step 1: Input Validation
    validation = input_validator.validate_input(request.symptoms)
    if not validation['valid']:
        return {
            "status": "error",
            "message": validation['message'],
            "emergency": validation['emergency']
        }

    if validation['emergency']:
        return {
            "status": "emergency",
            "message": validation['message'],
            "emergency": True
        }

    # Step 2: Missing Data Detection
    patient_data = {
        'age': request.age,
        'gender': request.gender,
        'duration': request.duration,
        'severity': request.severity
    }

    missing_data = missing_data_detector.detect_missing_data(request.symptoms, patient_data)

    if missing_data['missing_fields']:
        return {
            "status": "follow_up",
            "message": "Please provide additional information.",
            "follow_up_questions": missing_data['follow_up_questions'],
            "missing_fields": missing_data['missing_fields']
        }

    # Step 3: Proceed with analysis (Phase 7 logic)
    hospital_results = await run_hospitals(request.symptoms)

    # Aggregate and Compute Consensus
    aggregated_data = aggregate_hospital_opinions(hospital_results)

    # Re-optimize tests from the broad multi-hospital pool for UI cost consistency
    total_tests = aggregated_data.get("recommended_tests", [])
    cost_optimization_result = optimize_tests(total_tests, budget=request.budget)

    # Derive top risk level from leading consensus hospital
    ops = aggregated_data.get("hospital_opinions", [])
    top_risk = ops[0]["risk"] if ops else "Medium"
    top_conf = aggregated_data.get("confidence", 0)

    # Generate final reasoning and explanation
    final_reasoning = await generate_final_reasoning(request.symptoms, aggregated_data.get("hospital_opinions", []), aggregated_data, cost_optimization_result.get("optimized_tests", []))
    
    # Convert hospital_opinions list to dict for generate_explanation
    doctor_outputs = {op["hospital_name"]: op for op in aggregated_data.get("hospital_opinions", [])}
    
    explanation = generate_explanation(
        request.symptoms,
        doctor_outputs,
        final_reasoning.get("final_diagnosis", ""),
        top_conf,
        85.0,  # placeholder agreement score
        top_risk
    )

    # Step 4: Generate Clinical Report
    patient_summary = patient_data
    patient_summary.update(missing_data['extracted_data'])

    report = report_generator.generate_report(
        patient_data=patient_summary,
        symptoms=request.symptoms,
        diagnosis_results=final_reasoning,
        doctor_opinions=ops,
        confidence_score=top_conf,
        risk_level=top_risk,
        recommended_tests=cost_optimization_result.get("optimized_tests", []),
        ai_explanation=explanation
    )

    # Step 5: Generate follow-up questions if requested
    followup_questions = None
    if request.generate_followup and followup_agent:
        try:
            followup_questions = await followup_agent.generate_followup_questions(
                initial_symptoms=request.symptoms,
                initial_diagnosis=final_reasoning.get("final_diagnosis", ""),
                doctor_opinions=ops,
                confidence_score=top_conf,
                risk_level=top_risk
            )
        except Exception as e:
            print(f"Error generating follow-up questions: {e}")
            followup_questions = None

    # Generate detailed analysis
    try:
        detailed_analysis = generate_detailed_analysis(
            symptoms=request.symptoms,
            doctor_opinions=ops,
            confidence_score=top_conf
        )
    except Exception as e:
        print(f"Error generating detailed analysis: {e}")
        detailed_analysis = {}

    # Generate visualizations
    try:
        visualizations = generate_all_visualizations(
            conditions=detailed_analysis.get('conditions', []),
            confidences=detailed_analysis.get('confidence_scores', []),
            risk_levels=detailed_analysis.get('risk_levels', []),
            doctor_opinions=ops,
            symptom_importance=detailed_analysis.get('symptom_importance', {}),
            overall_risk=top_risk
        )
    except Exception as e:
        print(f"Error generating visualizations: {e}")
        visualizations = {}

    return {
        "status": "success",
        "patient_report": report,
        "risk": top_risk,
        "diagnosis": final_reasoning.get("final_diagnosis", ""),
        "tests": cost_optimization_result.get("optimized_tests", []),
        "estimated_cost": cost_optimization_result.get("estimated_cost", 0),
        "confidence": top_conf,
        "explanation": final_reasoning.get("reasoning", ""),
        "doctor_opinions": ops,
        "followup_questions": followup_questions,
        "detailed_analysis": detailed_analysis,
        "visualizations": visualizations
    }

@app.post("/followup")
async def handle_followup(request: FollowUpRequest):
    # This endpoint would process follow-up responses and continue analysis
    # For now, return a placeholder
    return {
        "status": "processing",
        "message": "Follow-up responses received. Proceeding with analysis."
    }

@app.post("/refine-diagnosis")
async def refine_diagnosis(request: RefineDiagnosisRequest):
    if not followup_agent:
        return {
            "status": "error",
            "message": "Follow-up question agent not available"
        }
    
    try:
        # This is a simplified implementation
        # In a real system, you'd store the initial analysis and retrieve it
        refined = await followup_agent.refine_diagnosis_with_responses(
            initial_symptoms="",  # Would need to retrieve from stored analysis
            initial_diagnosis="",  # Would need to retrieve from stored analysis
            followup_responses=request.followup_responses,
            doctor_opinions=[]  # Would need to retrieve from stored analysis
        )
        
        return {
            "status": "success",
            "refined_diagnosis": refined.get("refined_diagnosis", "Refined diagnosis"),
            "confidence_score": refined.get("confidence_score", 80),
            "key_factors": refined.get("key_factors", "Based on follow-up responses"),
            "risk_assessment": refined.get("risk_assessment", "Medium")
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Refinement failed: {str(e)}"
        }

@app.get("/report/{analysis_id}")
async def get_report(analysis_id: str):
    # This would retrieve a stored report
    # For now, return placeholder
    return {
        "status": "error",
        "message": "Report retrieval not implemented yet"
    }

    return {
        # Phase 7 core outputs
        "hospitals": aggregated_data.get("hospitals", []),
        "hospital_opinions": aggregated_data.get("hospital_opinions", []),
        "consensus_diagnosis": aggregated_data.get("consensus_diagnosis", "Unknown"),
        "agreement": aggregated_data.get("agreement", "0%"),
        "debate_explanation": aggregated_data.get("debate_explanation", ""),
        
        # UI format bridge mapping
        "selected_doctors": aggregated_data.get("hospitals", []),  # repurpose the label
        "final_diagnosis": aggregated_data.get("consensus_diagnosis", "Unknown"),
        "confidence": top_conf,
        "risk_level": top_risk,
        "optimized_tests": cost_optimization_result["recommended_tests"],
        "estimated_cost": cost_optimization_result["estimated_cost"],
        "explanation": aggregated_data.get("debate_explanation", ""),
        "doctor_contributions": { h: round(100/len(aggregated_data["hospitals"]), 1) for h in aggregated_data.get("hospitals", []) }

    }
