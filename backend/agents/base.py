import os
import json
from groq import AsyncGroq

class BaseAgent:
    def __init__(self, role_prompt, weight):
        api_key = os.environ.get("GROQ_API_KEY")
        self.client = AsyncGroq(api_key=api_key) if api_key else None
        self.role_prompt = role_prompt
        self.weight = weight

    async def analyze(self, symptoms: str):
        if not self.client:
            return {
                "disease_predictions": {},
                "confidence_scores": {},
                "recommended_tests": [],
                "reasoning": "Error: GROQ_API_KEY not configured. Cannot generate analysis."
            }
            
        prompt = f"""
        {self.role_prompt}
        
        Analyze the following symptoms: {symptoms}
        
        Provide your analysis in JSON format with the following keys:
        - "disease_predictions": A dictionary mapping disease names to probability floats (0.0 to 1.0). Limit to top 3.
        - "confidence_scores": A dictionary mapping disease names to confidence scores floats (0.0 to 1.0).
        - "recommended_tests": A list of diagnostic tests you recommend (e.g., ["Blood Test", "X-ray"]).
        - "reasoning": A brief paragraph explaining your reasoning.
        
        Ensure the output is ONLY valid JSON.
        """
        try:
            response = await self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful, extremely precise medical AI assistant that only outputs valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile", # Groq model
                response_format={"type": "json_object"},
                temperature=0.2
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"Error in agent: {e}")
            return {
                "disease_predictions": {},
                "confidence_scores": {},
                "recommended_tests": [],
                "reasoning": f"Error during analysis: {str(e)}"
            }
