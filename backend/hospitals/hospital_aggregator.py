from collections import Counter

def aggregate_hospital_opinions(hospital_results: list) -> dict:
    opinions = []
    diagnoses = []
    tests_pool = set()
    total_conf = 0.0
    unique_diagnoses_map = {}

    for res in hospital_results:
        diag = res["diagnosis"]
        diagnoses.append(diag)
        unique_diagnoses_map[res["hospital_name"]] = diag
        total_conf += res["confidence"]
        
        opinions.append({
            "hospital_name": res["hospital_name"],
            "specialization": res["specialization"],
            "diagnosis": diag,
            "confidence": res["confidence"],
            "risk": res["risk"],
            "tests": res["tests"]
        })
        
        for t in res["tests"]:
            tests_pool.add(t)

    if not hospital_results:
        return {}

    # Calculate Consensus
    # Normalizing comparison to lower case and skipping "unknown" matches if we have alternatives
    valid_diagnoses = [d for d in diagnoses if d.lower() != "unknown" and str(d).strip() != ""]
    target_diagnoses = valid_diagnoses if valid_diagnoses else diagnoses
    
    diag_counts = Counter([d.lower() for d in target_diagnoses])
    top_diag_lower, top_count = diag_counts.most_common(1)[0]
    
    consensus_diagnosis = next(d for d in target_diagnoses if d.lower() == top_diag_lower)
    
    avg_conf = round(total_conf / len(hospital_results), 1)
    agreement_score = round((top_count / len(hospital_results)) * 100, 1)

    # AI Debate Logic (Bonus Feature)
    debate_explanation = ""
    # Check if there's a difference in strict diagnostic findings
    unique_lower_diagnoses = set(d.lower() for d in valid_diagnoses)
    
    if len(unique_lower_diagnoses) > 1:
        disagreements = []
        for h, d in unique_diagnoses_map.items():
            if str(d).strip() != "" and str(d).lower() != "unknown":
                disagreements.append(f"{h} isolates '{d}'")
        debate_explanation = "Clinical Debate Identified: " + " whereas ".join(disagreements) + ". The consensus algorithm biases towards the most common convergence."
    else:
        debate_explanation = f"Network Consensus Reached: All remote hospitals perfectly concur on tracking '{consensus_diagnosis}' based on the symptomatic profile."

    return {
        "hospitals": [res["hospital_name"] for res in hospital_results],
        "hospital_opinions": opinions,
        "consensus_diagnosis": consensus_diagnosis,
        "confidence": avg_conf,
        "agreement": f"{agreement_score}%",
        "recommended_tests": list(tests_pool),
        "debate_explanation": debate_explanation,
        "explanation": debate_explanation # for backwards UI compat
    }
