"""
Simulated AI engine for generating quests with random variation.
"""

from typing import List, Dict
import random

class LLMConfig:
    """Configuration for the AI engine."""
    def __init__(self, model_name: str = "sim-model-v1", temperature: float = 0.3):
        self.model_name = model_name
        self.temperature = temperature

class LLMEngine:
    """Simulated AI engine for quest generation."""
    def __init__(self, config: LLMConfig):
        self.config = config

    def generate_quests(self, goal: str, n: int = 5, mode: str = "ai_sim") -> List[Dict]:
        """
        Generate quests with random names, descriptions, points, and difficulty.

        Args:
            goal (str): The user’s goal.
            n (int): Number of quests.
            mode (str): Mode, for compatibility ("ai_sim").

        Returns:
            List[Dict]: List of generated quests.
        """
        suffixes = ["Quick Win", "Mini Habit", "Boost", "Momentum", "Push Forward", "Step Forward", "Micro Task"]
        used_names = set()
        quests = []

        for i in range(n):
            available = [s for s in suffixes if s not in used_names]
            if not available:
                available = suffixes
            suffix = random.choice(available)
            used_names.add(suffix)

            points = random.randint(5, 15)
            difficulty = random.choice(["easy", "medium", "hard"])
            descriptions = [
                f"Do a short action to help with the goal: {goal}. Keep it manageable.",
                f"Perform a small step toward: {goal}. Make it achievable today.",
                f"Take a tiny action to progress with: {goal}. Keep it consistent.",
                f"Small activity to support {goal}. Stay focused and repeatable.",
                f"Quick task to advance {goal}. Keep it light and achievable."
            ]
            description = random.choice(descriptions)

            quests.append({
                "name": f"{goal} - {suffix}",
                "description": description,
                "points": points,
                "difficulty": difficulty
            })

        return quests
