from .base import BaseAgent

class PulmonologistAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role_prompt="You are an expert Pulmonologist. You specialize in diseases of the respiratory tract. Evaluate the symptoms focusing on lung and respiratory conditions.",
            weight=0.4
        )
