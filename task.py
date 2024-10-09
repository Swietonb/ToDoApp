class Task:
    def __init__(self, title, priority, category, due_date=None, due_time=None):
        self.title = title
        self.priority = priority
        self.category = category
        self.due_date = due_date
        self.due_time = due_time
        self.is_deleted = False
        self.is_completed = False

    def toggle_completed(self):
        """Przełącz status ukończenia zadania"""
        self.is_completed = not self.is_completed
