import re
from typing import Dict, Any

class InputValidator:
    def __init__(self):
        # Medical keywords to check for medical relevance
        self.medical_keywords = {

# Pain Types (Very Important for Diagnosis)
'sharp pain','dull pain','burning pain','stabbing pain','shooting pain',
'throbbing pain','cramping pain','aching pain','radiating pain',
'localized pain','diffuse pain','constant pain','intermittent pain',
'worsening pain','sudden pain','chronic pain','acute pain',

# Severity Descriptors
'mild','moderate','severe','intense','extreme','unbearable',
'manageable','persistent','progressive','worsening','improving',

# Duration Related
'sudden','gradual','constant','intermittent','comes and goes',
'recurring','chronic','acute','recent','long term','short term',

# Constitutional Symptoms
'fatigue','tired','weakness','malaise','lethargy','low energy',
'weight loss','weight gain','loss appetite','increased appetite',
'night sweats','chills','fever','temperature','dehydration',

# Respiratory Extended
'short breath','breathlessness','difficulty breathing','wheezing',
'coughing','dry cough','wet cough','productive cough',
'blood cough','hemoptysis','chest tightness','congestion',
'runny nose','blocked nose','nasal congestion','sneezing',
'sore throat','hoarse voice','voice change',

# Cardiovascular Extended
'chest discomfort','chest pressure','tight chest',
'palpitations','rapid heartbeat','slow heartbeat',
'irregular heartbeat','heart racing','skipped beats',
'leg swelling','ankle swelling','edema',
'fainting','near fainting','cold extremities',

# Neurological Extended
'headache','migraine','dizziness','vertigo','lightheaded',
'fainting','seizure','convulsion','tremor',
'numbness','tingling','pins and needles',
'weakness','paralysis','confusion','memory loss',
'difficulty concentrating','speech difficulty',
'slurred speech','vision changes','double vision',

# Gastrointestinal Extended
'abdominal pain','stomach pain','bloating','gas',
'nausea','vomiting','diarrhea','constipation',
'loose stool','hard stool','blood stool',
'black stool','acid reflux','heartburn',
'indigestion','burping','belching','flatulence',
'cramps','abdominal swelling',

# Urinary Extended
'frequent urination','pain urination','burning urination',
'urgency urination','blood urine','dark urine',
'cloudy urine','urinary retention','incontinence',
'kidney pain','flank pain',

# Skin Extended
'rash','itching','redness','swelling','blister',
'wound','cut','bruise','bleeding','dry skin',
'peeling skin','discoloration','lump','bump',
'skin infection','abscess','ulcer',

# Musculoskeletal Extended
'joint pain','muscle pain','back pain','neck pain',
'stiffness','swelling joint','limited movement',
'cramps','spasm','muscle weakness',
'sprain','strain','fracture','bone pain',

# Eye Extended
'blurred vision','double vision','eye pain',
'red eye','dry eyes','watering eyes',
'light sensitivity','vision loss',
'eye discharge','floaters',

# Ear Extended
'ear pain','hearing loss','ringing ears',
'tinnitus','ear discharge','blocked ear',
'dizziness','vertigo ear',

# Mental Health Extended
'anxiety','stress','depression','panic attack',
'mood swings','irritability','insomnia',
'sleep problem','restlessness','fear',
'hallucination','delusion','confusion',

# Infection Related
'infection','viral','bacterial','fungal',
'pus','abscess','inflammation','redness',
'swelling','warmth','fever infection',

# Metabolic
'excess thirst','frequent hunger','weight change',
'fatigue','sweating','cold intolerance',
'heat intolerance',

# Endocrine
'thyroid','hormone','diabetes','high sugar',
'low sugar','cholesterol','metabolic',

# Blood Related
'bleeding','clotting','anemia','low hemoglobin',
'pale skin','bruising','platelet',

# Pediatric Symptoms
'crying','irritability','poor feeding',
'vomiting child','fever child','rash child',

# Geriatric
'confusion elderly','fall','weakness elderly',
'memory problem','mobility issue',

# Emergency Keywords (Very Important)
'severe chest pain','difficulty breathing',
'unconscious','seizure','stroke symptoms',
'paralysis','heavy bleeding','severe pain',
'bluish lips','sudden weakness',

# Common Layman Words (Important for NLP)
'not feeling well','feeling sick','unwell',
'body pain','body ache','not okay',
'feeling weak','feeling tired','low energy',
'heavy head','tight chest','upset stomach',

# COVID / Viral
'covid','corona','loss smell','loss taste',
'body ache','viral fever',

# Women's Health
'irregular periods','missed period','heavy bleeding',
'pelvic pain','discharge','pregnancy',
'cramps','menstrual pain',

# Men's Health
'erectile dysfunction','testicular pain',
'prostate','urinary problem male'

}

        # Emergency keywords
        self.emergency_keywords = {
            'chest pain', 'severe bleeding', 'stroke', 'difficulty breathing',
            'unconscious', 'seizure', 'heart attack', 'choking', 'severe injury'
        }

    def validate_input(self, symptoms: str) -> Dict[str, Any]:
        """
        Validate input symptoms text.
        Returns dict with 'valid': bool, 'message': str, 'emergency': bool
        """
        if not symptoms or not symptoms.strip():
            return {
                'valid': False,
                'message': 'Please describe your symptoms in detail.',
                'emergency': False
            }

        symptoms_lower = symptoms.lower().strip()

        # Check for malicious input
        if self._is_malicious(symptoms):
            return {
                'valid': False,
                'message': 'Invalid input detected. Please provide medical symptoms only.',
                'emergency': False
            }

        # Check if it's medical-related
        if not self._is_medical_related(symptoms_lower):
            return {
                'valid': False,
                'message': 'Please describe medical symptoms. This appears to be non-medical content.',
                'emergency': False
            }

        # Check for emergency
        if self._is_emergency(symptoms_lower):
            return {
                'valid': True,
                'message': 'EMERGENCY DETECTED: Please seek immediate medical attention! Call emergency services.',
                'emergency': True
            }

        return {
            'valid': True,
            'message': 'Input validated successfully.',
            'emergency': False
        }

    def _is_malicious(self, text: str) -> bool:
        """Check for potentially malicious input patterns."""
        malicious_patterns = [
            r'<script[^>]*>.*?</script>',  # Script tags
            r'javascript:',  # JavaScript URLs
            r'on\w+\s*=',  # Event handlers
            r';\s*DROP\s+TABLE',  # SQL injection
            r';\s*DELETE\s+FROM',  # SQL injection
            r'union\s+select',  # SQL injection
            r'--',  # SQL comments
            r'/\*.*?\*/',  # SQL comments
        ]

        for pattern in malicious_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def _is_medical_related(self, text: str) -> bool:
        """Check if text contains medical keywords."""
        words = set(re.findall(r'\b\w+\b', text))
        medical_words = words.intersection(self.medical_keywords)
        return len(medical_words) >= 1  # Require at least 1 medical keyword

    def _is_emergency(self, text: str) -> bool:
        """Check for emergency symptoms."""
        for keyword in self.emergency_keywords:
            if keyword in text:
                return True
        return False