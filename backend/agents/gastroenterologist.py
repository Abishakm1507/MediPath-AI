from .base import BaseAgent

class GastroenterologistAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role_prompt="You are an expert Gastroenterologist. Evaluate the symptoms with a focus on the digestive system and its disorders.",
            weight=0.3
        )
