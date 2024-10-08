class Task:
    def __init__(self, title, priority, category):
        self.title = title
        self.priority = priority
        self.category = category
        self.is_deleted = False
        self.is_completed = False  # Domyślnie zadanie nie jest ukończone

    def toggle_completed(self):
        """Przełącz status ukończenia zadania"""
        self.is_completed = not self.is_completed

    def mark_completed(self):
        self.completed = True
