import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

from agents.general_physician import GeneralPhysicianAgent
from agents.pulmonologist import PulmonologistAgent
from agents.infectious_specialist import InfectiousSpecialistAgent
from aggregator.belief_aggregator import aggregate_beliefs
from optimizer.cost_optimizer import optimize_tests
from reasoning.final_reasoning import generate_final_reasoning
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

class AnalyzeRequest(BaseModel):
    symptoms: str

@app.post("/analyze")
async def analyze_symptoms(request: AnalyzeRequest):
    symptoms = request.symptoms

    # 1. Initialize Agents
    gp = GeneralPhysicianAgent()
    pulmo = PulmonologistAgent()
    infectious = InfectiousSpecialistAgent()

    # 2. Run Agents in Parallel
    gp_task = gp.analyze(symptoms)
    pulmo_task = pulmo.analyze(symptoms)
    infectious_task = infectious.analyze(symptoms)

    results = await asyncio.gather(gp_task, pulmo_task, infectious_task)
    
    doctor_opinions = {
        "General Physician": results[0],
        "Pulmonologist": results[1],
        "Infectious Disease Specialist": results[2]
    }

    # 3. Aggregate Beliefs
    aggregated_diagnosis = aggregate_beliefs(doctor_opinions)

    # 4. Cost Optimization
    test_recommendations = []
    for doc, result in doctor_opinions.items():
        test_recommendations.extend(result.get("recommended_tests", []))
    
    cost_optimized_plan = optimize_tests(test_recommendations)

    # 5. Final Reasoning
    final_reasoning = await generate_final_reasoning(
        symptoms, 
        doctor_opinions, 
        aggregated_diagnosis, 
        cost_optimized_plan
    )

    return {
        "doctor_opinions": doctor_opinions,
        "aggregated_diagnosis": aggregated_diagnosis,
        "cost_optimized_plan": cost_optimized_plan,
        "final_diagnosis": final_reasoning.get("final_diagnosis", ""),
        "confidence": final_reasoning.get("confidence", ""),
        "reasoning": final_reasoning.get("reasoning", ""),
        "recommended_next_steps": final_reasoning.get("recommended_next_steps", [])
    }
