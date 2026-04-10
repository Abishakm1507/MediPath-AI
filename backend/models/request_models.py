from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class AnalyzeRequest(BaseModel):
    symptoms: str
    budget: Optional[float] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    duration: Optional[str] = None
    severity: Optional[str] = None
    step: Optional[int] = 1  # For interactive flow
    generate_followup: Optional[bool] = False  # Whether to generate follow-up questions

class FollowUpRequest(BaseModel):
    question_responses: Dict[str, Any]

class RefineDiagnosisRequest(BaseModel):
    initial_analysis_id: str
    followup_responses: Dict[str, str]

class ReportRequest(BaseModel):
    analysis_id: str
