class Task:
    def __init__(self, title, priority, category):
        self.title = title
        self.priority = priority
        self.category = category
        self.completed = False

    def mark_completed(self):
        self.completed = True
