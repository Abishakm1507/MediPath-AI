def calculate_agreement(doctor_outputs: dict, final_diagnosis: str) -> float:
    if not doctor_outputs or not final_diagnosis:
        return 0.0
    
    agreeing_doctors = 0
    total_doctors = len(doctor_outputs)
    
    for doc, result in doctor_outputs.items():
        diseases = result.get("diseases", [])
        if diseases and isinstance(diseases, list):
            # Check if top predicted disease matches final diagnosis (fuzzy match)
            top_dx = str(diseases[0]).lower()
            fin_dx = str(final_diagnosis).lower()
            if fin_dx in top_dx or top_dx in fin_dx:
                agreeing_doctors += 1
                
    return (agreeing_doctors / total_doctors) * 100 if total_doctors > 0 else 0.0


def calculate_confidence(doctor_outputs: dict, final_diagnosis: str, symptom_severity: float = 0.5) -> dict:
    agreement_score = calculate_agreement(doctor_outputs, final_diagnosis)
    
    # Calculate average confidence
    total_conf = 0.0
    count = 0
    
    # contributions dictionary for bonus
    contributions = {}
    
    for doc, result in doctor_outputs.items():
        conf_list = result.get("confidence", [])
        doc_conf = 0.0
        if conf_list and isinstance(conf_list, list) and len(conf_list) > 0:
            doc_conf = float(conf_list[0])
            
        total_conf += doc_conf
        count += 1
        
        # assign contribution based on raw base weight logic
        # For simplicity, base it roughly on the doctor's confidence in top prediction
        contributions[doc] = doc_conf * 100
    
    avg_confidence = (total_conf / count * 100) if count > 0 else 0.0
    
    # Combine: 0.4 * agreement + 0.4 * average_confidence + 0.2 * symptom_severity_normalized
    confidence_value = (0.4 * agreement_score) + (0.4 * avg_confidence) + (0.2 * (symptom_severity * 100))
    
    # Normalize contributions nicely to sum to 100
    total_cont = sum(contributions.values())
    if total_cont > 0:
        for k in contributions:
            contributions[k] = round((contributions[k] / total_cont) * 100)
            
    return {
        "confidence": round(confidence_value, 1),
        "agreement_score": round(agreement_score, 1),
        "contributions": contributions
    }
