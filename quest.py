# quest.py
class Quest:
    def __init__(self, name, description="", points=10):
        self.name = name
        self.description = description
        self.points = points
        self.completed = False

    def mark_complete(self):
        self.completed = True

    def reset(self):
        self.completed = False

        
        