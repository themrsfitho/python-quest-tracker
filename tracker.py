# tracker.py
import json
from user import User
from quest import Quest

class QuestTracker: 
    def __init__(self, data_file="data/users.json"):
        self.users = {}
        self.data_file = data_file
        self.load_users()
        
    def add_user(self, username):
        if username not in self.users:
            self.users[username] = User(username)
            return True
        return False
    
    def get_user(self, username):
        return self.users.get(username)
        
    def save_users(self):
        data = {}
        for uname, user in self.users.items():
            data[uname] = {
                "points": user.points,
                "streak": user.streak,
                "quests": [
                    {"name": q.name, "description": q.description, "points": q.points, "completed": q.completed}
                    for q in user.quests
                ]
            }
        #ensure folder exists 
        import os
        os.makedirs("data", exist_ok=True)
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2)
            
    def load_users(self):
        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
            for uname, udata in data.items():
                user = user(uname)
                user.points = udata.get("points", 0)
                user.streak = udata.get("streak", 0)
                for qd in udata.get("quests", []):
                    q = Quest(qd["name"], qd.get("description", ""), qd.get("points", 10))
                    q.completed = qd.get("completed", False) 
                    user.add_quest(q)
                self.users[uname] = user 
        except FileNotFoundError:
            return 