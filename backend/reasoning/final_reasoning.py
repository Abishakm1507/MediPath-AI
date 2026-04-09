import os
import json
from groq import AsyncGroq

async def generate_final_reasoning(symptoms: str, doctor_opinions: dict, aggregated_diagnosis: dict, cost_optimized_plan: list) -> dict:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return {
            "final_diagnosis": "Unknown",
            "confidence": "0%",
            "reasoning": "Error: GROQ_API_KEY not configured. Cannot generate final reasoning.",
            "recommended_next_steps": []
        }
        
    client = AsyncGroq(api_key=api_key)
    
    prompt = f"""
    You are the Chief Medical Officer AI. Review the case of a patient with these symptoms:
    {symptoms}
    
    Opinions from specialist agents:
    {json.dumps(doctor_opinions, indent=2)}
    
    Aggregated probabilistic diagnosis:
    {json.dumps(aggregated_diagnosis, indent=2)}
    
    Cost-optimized diagnostic test plan:
    {json.dumps(cost_optimized_plan, indent=2)}
    
    Output valid JSON with ONLY the following keys:
    - "final_diagnosis": The single most likely disease (string).
    - "confidence": Your final confidence percentage as a string (e.g., "85%").
    - "reasoning": A detailed explanation of why this diagnosis was chosen, synthesizing the agents' inputs (string).
    - "recommended_next_steps": A list of immediate actions or tests to confirm (list of strings).
    """

    try:
        response = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a chief medical officer AI. Output ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            temperature=0.3
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"Error in final reasoning: {e}")
        return {
            "final_diagnosis": "Unknown due to error",
            "confidence": "0%",
            "reasoning": f"Error: {str(e)}",
            "recommended_next_steps": []
        }
