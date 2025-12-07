# user.py
from quest import Quest

class User:
    def __init__(self, username):
        self.username = username 
        self.quests = []
        self.points = 0
        self.streak - 0
        
    def add_quest(self, quest: Quest):
        self.quests.append(quest)
        
    def complete_quest(self, quest_name: str):
        for q in self.quests:
            if q.name == quest_name:
                if not q.completed:
                    q.mark_complete()
                    self.points += q.points
                return True
            return False
        
    def reset_quests(self):
        for q in self.quests:
            q.reset()