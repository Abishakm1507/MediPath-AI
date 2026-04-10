import json
import os

TEST_INFORMATION_GAIN = {
    "Blood Test": 0.6,
    "ECG": 0.9,
    "Chest X-ray": 0.7,
    "MRI": 0.95,
    "CT Scan": 0.9,
    "Troponin Test": 0.85,
    "Ultrasound": 0.75
}

def load_test_costs():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_costs.json')
    try:
        with open(data_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def optimize_tests(test_recommendations: list, budget: float = None) -> dict:
    test_costs = load_test_costs()
    
    # Remove duplicates
    unique_tests = list(set(test_recommendations))
    
    test_scores = []
    
    for test in unique_tests:
        # Match given test with our dataset
        matched_key = None
        for key in test_costs.keys():
            if test.lower() in key.lower() or key.lower() in test.lower():
                matched_key = key
                break
                
        if matched_key:
            cost = test_costs.get(matched_key, 2000)
            info_gain = TEST_INFORMATION_GAIN.get(matched_key, 0.5)
            score = info_gain / float(cost) if cost > 0 else 0
            
            # Prioritization Level
            priority = "Optional"
            if info_gain >= 0.9:
                priority = "Critical"
            elif info_gain >= 0.7:
                priority = "Recommended"
                
            test_scores.append({
                "test": matched_key,
                "cost": cost,
                "information_gain": info_gain,
                "score": score,
                "priority": priority
            })
            
    # Greedy Algorithm: highest score first
    test_scores.sort(key=lambda x: x["score"], reverse=True)
    
    selected_tests = []
    total_cost = 0.0
    detailed_plan = []
    
    for item in test_scores:
        if budget is not None:
            if total_cost + item["cost"] > budget:
                continue # Skip if it exceeds budget
                
        selected_tests.append(item["test"])
        total_cost += item["cost"]
        detailed_plan.append({
            "test": item["test"],
            "cost": item["cost"],
            "priority": item["priority"]
        })
        
    return {
        "recommended_tests": selected_tests,
        "estimated_cost": total_cost,
        "detailed_plan": detailed_plan
    }
