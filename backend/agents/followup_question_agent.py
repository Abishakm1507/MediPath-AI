import os
import json
from groq import AsyncGroq
from typing import List, Dict, Any

class FollowUpQuestionAgent:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        self.client = AsyncGroq(api_key=self.api_key)

    async def generate_followup_questions(
        self,
        initial_symptoms: str,
        initial_diagnosis: str,
        doctor_opinions: List[Dict[str, Any]],
        confidence_score: float,
        risk_level: str
    ) -> List[str]:
        """
        Generate adaptive follow-up questions based on initial diagnosis and doctor opinions.

        Args:
            initial_symptoms: The patient's reported symptoms
            initial_diagnosis: The primary diagnosis from initial analysis
            doctor_opinions: List of doctor opinions with diagnoses
            confidence_score: Confidence score of the diagnosis
            risk_level: Risk level assessment

        Returns:
            List of follow-up questions to ask the patient
        """

        # Extract unique diagnoses from doctor opinions
        diagnoses = set()
        for opinion in doctor_opinions:
            if opinion.get('diagnosis'):
                diagnoses.add(opinion['diagnosis'].lower())

        diagnoses = list(diagnoses)

        # If confidence is low or multiple diagnoses, generate more questions
        question_count = 3 if confidence_score < 70 else 2
        if len(diagnoses) > 1:
            question_count += 1

        prompt = f"""
        You are a medical follow-up question specialist. Based on the patient's symptoms and initial AI diagnosis,
        generate {question_count} targeted follow-up questions to refine the diagnosis.

        Patient Symptoms: {initial_symptoms}
        Initial Diagnosis: {initial_diagnosis}
        Confidence Score: {confidence_score}%
        Risk Level: {risk_level}
        Alternative Diagnoses Considered: {', '.join(diagnoses)}

        Generate questions that will help differentiate between possible diagnoses and gather more clinical information.
        Focus on:
        - Duration and progression of symptoms
        - Associated symptoms
        - Risk factors
        - Severity and impact on daily life
        - Previous medical history relevant to the condition

        Return exactly {question_count} questions as a JSON array of strings.
        Make questions clear, professional, and medically relevant.
        """

        try:
            response = await self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a medical AI that generates follow-up questions. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.1-8b-instant",
                response_format={"type": "json_object"},
                temperature=0.3
            )

            content = response.choices[0].message.content
            result = json.loads(content)

            # Extract questions from the response
            if isinstance(result, dict) and 'questions' in result:
                questions = result['questions']
            elif isinstance(result, list):
                questions = result
            else:
                # Fallback: try to extract from text
                questions = [f"How long have you had {initial_symptoms}?",
                           f"Have you noticed any other symptoms besides {initial_symptoms}?",
                           f"On a scale of 1-10, how severe are your symptoms?"]

            return questions[:question_count]  # Ensure we don't exceed requested count

        except Exception as e:
            print(f"Error generating follow-up questions: {e}")
            # Return fallback questions
            return [
                f"How long have you been experiencing {initial_symptoms}?",
                f"Have you noticed any other symptoms or changes?",
                f"Are there any factors that make your symptoms better or worse?"
            ]

    async def refine_diagnosis_with_responses(
        self,
        initial_symptoms: str,
        initial_diagnosis: str,
        followup_responses: Dict[str, str],
        doctor_opinions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Refine the diagnosis based on follow-up question responses.

        Args:
            initial_symptoms: Original symptoms
            initial_diagnosis: Initial diagnosis
            followup_responses: Dict of question -> answer
            doctor_opinions: Original doctor opinions

        Returns:
            Refined diagnosis information
        """

        responses_text = "\n".join([f"Q: {q}\nA: {a}" for q, a in followup_responses.items()])

        prompt = f"""
        You are a medical diagnosis refinement specialist. Review the initial diagnosis and incorporate
        the patient's responses to follow-up questions to refine or confirm the diagnosis.

        Initial Symptoms: {initial_symptoms}
        Initial Diagnosis: {initial_diagnosis}

        Follow-up Responses:
        {responses_text}

        Doctor Opinions:
        {json.dumps(doctor_opinions, indent=2)}

        Provide a refined diagnosis analysis including:
        - Refined primary diagnosis
        - Updated confidence score (percentage)
        - Key factors from follow-up responses
        - Any changes to risk assessment

        Return as JSON with keys: refined_diagnosis, confidence_score, key_factors, risk_assessment
        """

        try:
            response = await self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a medical AI that refines diagnoses. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"},
                temperature=0.3
            )

            content = response.choices[0].message.content
            return json.loads(content)

        except Exception as e:
            print(f"Error refining diagnosis: {e}")
            return {
                "refined_diagnosis": initial_diagnosis,
                "confidence_score": 75,
                "key_factors": "Unable to process responses",
                "risk_assessment": "Medium"
            }