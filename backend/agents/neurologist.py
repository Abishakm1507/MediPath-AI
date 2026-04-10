from .base import BaseAgent

class NeurologistAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role_prompt="You are an expert Neurologist. Evaluate the symptoms with a focus on the nervous system, brain, and spinal cord.",
            weight=0.3
        )
