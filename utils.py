"""
Utility functions for Python Quest Tracker.
"""

from quest import Quest
from ai_engine import LLMEngine, LLMConfig
import random

def generate_quests(goal: str, n: int = 5, mode: str = "mock"):
    """
    Generate quests either in mock mode or ai_sim mode.

    Args:
        goal (str): The goal for quest generation.
        n (int): Number of quests.
        mode (str): 'mock' or 'ai_sim'.

    Returns:
        List[Dict]: List of quest dictionaries.
    """
    if mode == "mock":
        return [
            {
                "name": f"{goal} Step {i+1}",
                "description": f"Do a short action to help with the goal: {goal}. Keep it under 100 characters.",
                "points": random.randint(5, 15),
                "difficulty": "medium"
            } for i in range(n)
        ]
    else:
        engine = LLMEngine(LLMConfig())
        return engine.generate_quests(goal, n=n, mode=mode)
