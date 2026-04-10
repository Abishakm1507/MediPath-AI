import re
from typing import Dict, List, Any, Optional

class MissingDataDetector:
    def __init__(self):
        self.required_fields = ['age', 'gender', 'duration', 'severity']

    def detect_missing_data(self, symptoms: str, additional_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Detect missing patient data from symptoms text and additional data.
        Returns dict with 'missing_fields': list, 'follow_up_questions': list
        """
        if additional_data is None:
            additional_data = {}

        missing_fields = []
        follow_up_questions = []

        # Extract data from symptoms text
        extracted_data = self._extract_from_text(symptoms)

        # Check each required field
        for field in self.required_fields:
            if field not in additional_data and field not in extracted_data:
                missing_fields.append(field)
                question = self._get_follow_up_question(field)
                if question:
                    follow_up_questions.append(question)

        return {
            'missing_fields': missing_fields,
            'follow_up_questions': follow_up_questions,
            'extracted_data': extracted_data
        }

    def _extract_from_text(self, text: str) -> Dict[str, Any]:
        """Extract patient data from symptoms text using regex patterns."""
        extracted = {}

        # Age patterns
        age_patterns = [
            r'(\d{1,3})\s*(?:year|yr)s?\s*old',
            r'age\s*(\d{1,3})',
            r'(\d{1,3})\s*(?:year|yr)s?\s*old',
        ]
        for pattern in age_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    age = int(match.group(1))
                    if 0 < age < 150:
                        extracted['age'] = age
                        break
                except ValueError:
                    pass

        # Gender patterns
        if re.search(r'\b(?:male|man|boy|he|his|him)\b', text, re.IGNORECASE):
            extracted['gender'] = 'male'
        elif re.search(r'\b(?:female|woman|girl|she|her|hers)\b', text, re.IGNORECASE):
            extracted['gender'] = 'female'

        # Duration patterns
        duration_patterns = [
            r'for\s+(?:the\s+)?(?:past\s+)?(\d+)\s*(day|week|month|year)s?',
            r'(\d+)\s*(day|week|month|year)s?\s+(ago|now)',
            r'since\s+(\d+)\s*(day|week|month|year)s?\s+ago',
        ]
        for pattern in duration_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    num = int(match.group(1))
                    unit = match.group(2).lower()
                    extracted['duration'] = f"{num} {unit}{'s' if num != 1 else ''}"
                    break
                except (ValueError, IndexError):
                    pass

        # Severity patterns
        if re.search(r'\b(?:severe|extreme|critical|intense|unbearable)\b', text, re.IGNORECASE):
            extracted['severity'] = 'severe'
        elif re.search(r'\b(?:moderate|mild|slight|minor)\b', text, re.IGNORECASE):
            extracted['severity'] = 'mild'
        elif re.search(r'\b(?:mild|slight|minor)\b', text, re.IGNORECASE):
            extracted['severity'] = 'mild'

        return extracted

    def _get_follow_up_question(self, field: str) -> Optional[str]:
        """Get appropriate follow-up question for missing field."""
        questions = {
            'age': 'What is the patient\'s age?',
            'gender': 'What is the patient\'s gender?',
            'duration': 'How long have these symptoms been present?',
            'severity': 'How would you rate the severity of the symptoms (mild, moderate, severe)?'
        }
        return questions.get(field)