from ai_engine import LLMEngine, LLMConfig
import json

eng = LLMEngine(LLMConfig(model_name="sim-model-v1", temperature=0.3))
items = eng.generate_quests("improve morning routine", n=3)
print(json.dumps(items, indent=2))
