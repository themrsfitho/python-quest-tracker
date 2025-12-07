# ai_engine.py
"""
LLM simulation / prompt-engineering engine.
This mimics a real LLM pipeline but is fully deterministic and free.
It reads prompt templates from prompts/, fills them, and returns structured JSON-like output.
"""

import json
import random
import re
from typing import List, Dict, Any

PROMPT_DIR = "prompts"

class LLMConfig:
    def __init__(self, model_name: str = "sim-model-v1", temperature: float = 0.3, max_tokens: int = 300):
        self.model_name = model_name
        self.temperature = float(temperature)
        self.max_tokens = int(max_tokens)

class LLMEngine:
    def __init__(self, config: LLMConfig = None):
        self.config = config or LLMConfig()
        # load templates and schema
        self.base_prompt = self._load_template("base_prompt.txt")
        self.quest_prompt = self._load_template("quest_gen_prompt.txt")
        self.schema = self._load_json("schema.json")

    def _load_template(self, filename: str) -> str:
        path = f"{PROMPT_DIR}/{filename}"
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def _load_json(self, filename: str) -> Dict[str, Any]:
        path = f"{PROMPT_DIR}/{filename}"
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _seed_rng(self, seed_text: str) -> random.Random:
        # deterministic behavior so the same goal+config returns same output
        seed = sum(ord(c) for c in (seed_text + self.config.model_name))
        return random.Random(seed)

    def generate_quests(self, goal: str, n: int = 5) -> List[Dict[str, Any]]:
        """
        Simulate LLM generation. Returns a list of quest dicts following schema.
        This function intentionally prioritizes determinism and structure.
        """
        rng = self._seed_rng(goal)
        # Use schema defaults if present
        name_tpls = self.schema.get("name_templates", [])
        desc_tpls = self.schema.get("description_templates", [])
        points_range = self.schema.get("points_range", [8, 15])

        results: List[Dict[str, Any]] = []
        for i in range(n):
            name = self._render_name(goal, name_tpls, rng, idx=i)
            description = self._render_description(goal, desc_tpls, rng)
            points = int(rng.randint(points_range[0], points_range[1]))
            difficulty = self._estimate_difficulty(points, points_range)
            results.append({
                "name": name,
                "description": description,
                "points": points,
                "difficulty": difficulty
            })
        return results

    def _render_name(self, goal: str, templates: List[str], rng: random.Random, idx: int) -> str:
        if templates:
            tpl = templates[idx % len(templates)]
            short_goal = self._short_goal(goal)
            name = tpl.replace("{goal_short}", short_goal).strip()
            return self._clean_whitespace(name)
        short_goal = self._short_goal(goal)
        return f"{short_goal.title()} Step {idx+1}"

    def _render_description(self, goal: str, templates: List[str], rng: random.Random) -> str:
        if templates:
            tpl = rng.choice(templates)
            desc = tpl.replace("{goal}", goal)
            if rng.random() > 0.85:
                desc = desc + " Try to push slightly harder today."
            return self._clean_whitespace(desc)
        return f"A small action to support: {goal}"

    def _short_goal(self, goal: str, limit: int = 20) -> str:
        words = re.findall(r"[A-Za-z]+", goal)
        short = " ".join(words[:3])
        return short or goal[:limit]

    def _estimate_difficulty(self, points: int, points_range: List[int]) -> str:
        low, high = points_range[0], points_range[1]
        span = max(1, high - low)
        norm = (points - low) / span
        if norm < 0.33:
            return "easy"
        if norm < 0.66:
            return "medium"
        return "hard"

    def _clean_whitespace(self, s: str) -> str:
        return re.sub(r"\s+", " ", s).strip()

        