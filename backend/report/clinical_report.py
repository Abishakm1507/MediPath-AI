from typing import Dict, List, Any
from datetime import datetime

class ClinicalReportGenerator:
    def __init__(self):
        pass

    def generate_report(self,
                       patient_data: Dict[str, Any],
                       symptoms: str,
                       diagnosis_results: Dict[str, Any],
                       doctor_opinions: List[Dict[str, Any]],
                       confidence_score: float,
                       risk_level: str,
                       recommended_tests: List[str],
                       ai_explanation: str) -> str:
        """
        Generate a comprehensive clinical report.
        """
        report_lines = []

        # Header
        report_lines.append("MEDIPATH AI CLINICAL REPORT")
        report_lines.append("=" * 50)
        report_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")

        # Patient Summary
        report_lines.append("PATIENT SUMMARY")
        report_lines.append("-" * 20)
        age = patient_data.get('age', 'Not specified')
        gender = patient_data.get('gender', 'Not specified')
        duration = patient_data.get('duration', 'Not specified')
        severity = patient_data.get('severity', 'Not specified')

        report_lines.append(f"Age: {age}")
        report_lines.append(f"Gender: {gender}")
        report_lines.append(f"Symptom Duration: {duration}")
        report_lines.append(f"Severity: {severity}")
        report_lines.append("")

        # Symptoms
        report_lines.append("SYMPTOMS")
        report_lines.append("-" * 10)
        report_lines.append(symptoms)
        report_lines.append("")

        # Possible Diagnoses
        report_lines.append("POSSIBLE DIAGNOSES")
        report_lines.append("-" * 20)
        diagnoses = diagnosis_results.get('diagnoses', [])
        if diagnoses:
            for i, diagnosis in enumerate(diagnoses[:5], 1):  # Top 5
                report_lines.append(f"{i}. {diagnosis}")
        else:
            report_lines.append("No specific diagnoses identified")
        report_lines.append("")

        # Confidence Score
        report_lines.append("CONFIDENCE SCORE")
        report_lines.append("-" * 17)
        report_lines.append(f"{confidence_score:.1f}%")
        report_lines.append("")

        # Risk Level
        report_lines.append("RISK LEVEL")
        report_lines.append("-" * 12)
        report_lines.append(risk_level.upper())
        report_lines.append("")

        # Recommended Tests
        report_lines.append("RECOMMENDED TESTS")
        report_lines.append("-" * 19)
        if recommended_tests:
            for i, test in enumerate(recommended_tests, 1):
                report_lines.append(f"{i}. {test}")
        else:
            report_lines.append("No specific tests recommended")
        report_lines.append("")

        # Doctor Opinions
        report_lines.append("DOCTOR OPINIONS")
        report_lines.append("-" * 16)
        if doctor_opinions:
            for opinion in doctor_opinions:
                doctor = opinion.get('doctor', 'Unknown')
                diagnosis = opinion.get('diagnosis', 'N/A')
                confidence = opinion.get('confidence', 'N/A')
                report_lines.append(f"Dr. {doctor}: {diagnosis} (Confidence: {confidence})")
        else:
            report_lines.append("No doctor opinions available")
        report_lines.append("")

        # AI Explanation
        report_lines.append("AI EXPLANATION")
        report_lines.append("-" * 15)
        report_lines.append(ai_explanation)
        report_lines.append("")

        # Safety Disclaimer
        report_lines.append("SAFETY DISCLAIMER")
        report_lines.append("-" * 17)
        report_lines.append("This AI provides decision support only and is not a substitute for professional medical advice.")
        report_lines.append("Please consult with a qualified healthcare provider for diagnosis and treatment.")
        report_lines.append("In case of emergency, seek immediate medical attention.")

        return "\n".join(report_lines)

    def generate_pdf_content(self, text_report: str) -> str:
        """
        Convert text report to basic HTML for PDF generation.
        In a real implementation, this would use a PDF library.
        """
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MediPath AI Clinical Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2563eb; }}
                h2 {{ color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 5px; }}
                .disclaimer {{ background-color: #fef3c7; padding: 15px; border-left: 4px solid #f59e0b; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <pre>{text_report}</pre>
        </body>
        </html>
        """
        return html_content