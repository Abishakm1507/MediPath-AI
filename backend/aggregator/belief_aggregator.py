def aggregate_beliefs(doctor_opinions: dict) -> dict:
    weights = {
        "General Physician": 0.3,
        "Pulmonologist": 0.4,
        "Infectious Disease Specialist": 0.3
    }

    aggregated_probs = {}

    for doc_name, result in doctor_opinions.items():
        doc_weight = weights.get(doc_name, 0.0)
        diseases = result.get("diseases", [])
        confidences = result.get("confidence", [])
        
        for i in range(min(len(diseases), len(confidences))):
            disease = diseases[i]
            prob = confidences[i]
            
            # Standardize disease name roughly
            disease_key = str(disease).title().strip()
            
            if disease_key not in aggregated_probs:
                aggregated_probs[disease_key] = 0.0
            
            try:
                aggregated_probs[disease_key] += doc_weight * float(prob)
            except (ValueError, TypeError):
                pass
            
    # Sort diseases by final aggregate probability descending
    sorted_diseases = dict(sorted(aggregated_probs.items(), key=lambda item: item[1], reverse=True))

    return {
        "ranked_diseases": list(sorted_diseases.keys()),
        "probability_distribution": sorted_diseases
    }
