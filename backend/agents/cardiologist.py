from .base import BaseAgent

class CardiologistAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role_prompt="You are an expert Cardiologist. Evaluate the symptoms with a focus on cardiovascular systems.",
            weight=0.0  # Weight not specified in the aggregation engine
        )
