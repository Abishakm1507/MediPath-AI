SYMPTOM_ROUTING = {
    "chest pain": ["cardiologist", "general"],
    "shortness of breath": ["pulmonologist", "cardiologist"],
    "fever": ["infectious_specialist", "general"],
    "headache": ["neurologist", "general"],
    "abdominal pain": ["gastroenterologist", "general"],
    "fatigue": ["general"]
}

def route_doctors(symptoms: list[str]) -> list[str]:
    selected_doctors = set()
    for symptom in symptoms:
        symptom_lower = symptom.lower()
        for key, doctors in SYMPTOM_ROUTING.items():
            if key in symptom_lower or symptom_lower in key:
                selected_doctors.update(doctors)
    
    # Always include general physician
    selected_doctors.add("general")
    
    return list(selected_doctors)
