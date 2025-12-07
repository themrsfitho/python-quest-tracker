#utils.py
import random 

DEFAULT_QUEST_TEMPLATES = [
    ("Drink 100-128 ounces of water throughout the day.", 10),
    ("Do recovery every single day before bed.", 12),
    ("Get your 30 minutes of HIIT cardio in every day.", 8),
    ("Walk 5k steps", "Try to walk after every meal to aid digestion.", 9),
    ("Eat breakfast within an hour of waking up.", 11),
    ("Eat every 2-3 hours for steady energy throughout the day", 10),
]

from ai_engine import LLMEngine, LLMConfig

def generate_quests_mock(goal: str, n: int = 5):
    rng = random.Random(goal)
    templates = DEFAULT_QUEST_TEMPLATES.copy()
    rng.shuffle(templates)
    results = []
    for i in range(min(n, len(templates))):
        name, desc, points = templates[i]
        desc_custom = f"{desc} (Goal: {goal})" if rng.random() < 0.6 else desc
        results.append({"name": name, "description": desc_custom, "points": points})
    return results

def generate_quests_ai_sim(goal: str, n: int = 5, model_name="sim-model-v1", temperature=0.3):
    cfg = LLMConfig(model_name=model_name, temperature=temperature)
    engine = LLMEngine(config=cfg)
    items = engine.generate_quests(goal, n=n)
    # map engine fields to the format used by the rest of the app
    mapped = []
    for it in items:
        mapped.append({
            "name": it.get("name"),
            "description": it.get("description"),
            "points": int(it.get("points", 10)),
            "difficulty": it.get("difficulty", "medium")
        })
    return mapped

def generate_quests(goal: str, n: int = 5, mode: str = "mock"):
    """
    mode: 'mock' (default), 'ai_sim' (realistic simulated LLM)
    """
    if mode == "mock":
        return generate_quests_mock(goal, n)
    elif mode == "ai_sim":
        return generate_quests_ai_sim(goal, n)
    else:
        raise ValueError("Unsupported mode: " + str(mode))