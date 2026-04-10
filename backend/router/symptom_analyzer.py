import re

def extract_symptoms(text: str) -> list[str]:
    """
    Extracts symptoms from a given text.
    For this basic implementation, it uses keyword matching and splitting.
    Can be expanded to use complex NLP or LLM extraction.
    """
    # Create a basic list of common symptom keywords from the router
    common_symptoms = [
        "chest pain", 
        "shortness of breath", 
        "fever", 
        "headache", 
        "abdominal pain", 
        "fatigue"
    ]
    
    extracted = []
    text_lower = text.lower()
    
    for symptom in common_symptoms:
        if symptom in text_lower:
            extracted.append(symptom)
            
    # As a fallback, if no predefined symptom matched, we split by "and" or commas
    if not extracted:
        # Simplistic split
        parts = re.split(r",|\band\b", text_lower)
        extracted = [p.strip() for p in parts if len(p.strip()) > 3]
        
    return extracted
