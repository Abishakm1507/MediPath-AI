def generate_explanation(symptoms: str, doctor_outputs: dict, final_diagnosis: str, confidence_score: float, agreement_score: float, risk_level: str) -> str:
    involved_doctors = list(doctor_outputs.keys())
    docs_string = ", ".join(involved_doctors) if involved_doctors else "the clinical pipeline"
    
    docs_count = len(involved_doctors)
    agreeing_count = round((agreement_score / 100) * docs_count)
    
    explain_text = (f"Based on the reported symptoms ('{symptoms}'), virtual agents ({docs_string}) "
                    f"were consulted. {agreeing_count} out of {docs_count} doctors formed consensus on {final_diagnosis}. "
                    f"The final probability is established at {confidence_score}%, and the risk marker is designated as '{risk_level}'.")
                    
    return explain_text
