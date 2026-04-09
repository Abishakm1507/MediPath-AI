from .base import BaseAgent

class InfectiousSpecialistAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role_prompt="You are an expert Infectious Disease Specialist. Evaluate the symptoms focusing on viral, bacterial, fungal, or parasitic infections and systemic responses.",
            weight=0.3
        )
