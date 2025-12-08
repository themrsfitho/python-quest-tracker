"""
QuestTracker handles users, quests, and persistence.
"""

import json
from quest import Quest

class User:
    """Represents a user with quests."""
    def __init__(self, username: str):
        self.username = username
        self.quests = []
        self.points = 0

    def add_quest(self, quest: Quest):
        """Add a quest to the user's list."""
        self.quests.append(quest)

    def complete_quest(self, quest_name: str):
        """Complete a quest by name and add points."""
        for q in self.quests:
            if q.name == quest_name and not q.completed:
                q.complete()
                self.points += q.points
                break

class QuestTracker:
    """Manages multiple users and saves/loads data."""
    def __init__(self, data_file: str = "data/users.json"):
        self.users = {}
        self.data_file = data_file
        self.load_users()

    def add_user(self, username: str):
        """Add a new user or switch to existing user."""
        if username not in self.users:
            self.users[username] = User(username)
            return True
        return False

    def get_user(self, username: str):
        """Retrieve a user by username."""
        return self.users.get(username)

    def save_users(self):
        """Save all users and quests to JSON."""
        data = {}
        for uname, user in self.users.items():
            data[uname] = {
                "points": user.points,
                "quests": [
                    {
                        "name": q.name,
                        "description": q.description,
                        "points": q.points,
                        "completed": q.completed
                    } for q in user.quests
                ]
            }
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2)

    def load_users(self):
        """Load users and quests from JSON."""
        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
            for uname, udata in data.items():
                user = User(uname)
                user.points = udata.get("points", 0)
                for qd in udata.get("quests", []):
                    q = Quest(qd["name"], qd["description"], qd["points"])
                    if qd.get("completed", False):
                        q.complete()
                    user.add_quest(q)
                self.users[uname] = user
        except FileNotFoundError:
            # File not created yet
            pass
        except json.JSONDecodeError:
            # Empty file or invalid JSON
            pass
