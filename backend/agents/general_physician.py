from .base import BaseAgent

class GeneralPhysicianAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role_prompt="You are an expert General Physician. You have a broad understanding of various medical domains. Evaluate the symptoms from a primary care perspective.",
            weight=0.3
        )
