import json
import os
from collections import Counter

def optimize_tests(test_recommendations: list) -> list:
    # 1. Load test costs
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tests.json')
    try:
        with open(data_path, 'r') as f:
            test_costs = json.load(f)
    except FileNotFoundError:
        test_costs = {
            "Blood Test": 800,
            "X-ray": 1500,
            "CT Scan": 6000,
            "MRI": 8000,
            "PCR": 1200,
            "Sputum Test": 1000
        }

    normalized_recs = []
    for test in test_recommendations:
        test_lower = str(test).lower()
        matched = False
        for k in test_costs.keys():
            if k.lower() in test_lower or test_lower in k.lower():
                normalized_recs.append(k)
                matched = True
                break
        if not matched:
            normalized_recs.append(str(test).title())

    # Count frequencies (information gain proxy)
    counts = Counter(normalized_recs)
    unique_tests = list(counts.keys())
    
    default_cost = 2000
    
    test_scores = []
    for test in unique_tests:
        cost = test_costs.get(test, default_cost)
        info_gain = counts[test] 
        score = info_gain / float(cost)
        test_scores.append({
            "test": test,
            "cost": cost,
            "information_gain": info_gain,
            "score": score
        })
        
    # Sort by score descending
    test_scores.sort(key=lambda x: x["score"], reverse=True)
    
    plan = []
    cumulative_confidence_proxy = 0.0
    for idx, item in enumerate(test_scores):
        cumulative_confidence_proxy += min(0.3, item["score"] * 3000) # Scaling for simulation
        plan.append({
            "step": idx + 1,
            "test": item["test"],
            "cost": item["cost"],
            "reason": f"High info-to-cost ratio (Score: {item['score']:.6f}). Recommended by {item['information_gain']} agent(s)."
        })
        if cumulative_confidence_proxy >= 0.8:
            break
            
    return plan
