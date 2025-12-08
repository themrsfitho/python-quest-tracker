"""
Quest object representing a single task with points and optional completion status.
"""

class Quest:
    """A single quest/task."""
    def __init__(self, name: str, description: str = "", points: int = 10):
        self.name = name
        self.description = description
        self.points = points
        self.completed = False

    def complete(self):
        """Mark this quest as completed."""
        self.completed = True
