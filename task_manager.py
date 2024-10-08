class TaskManager:
    def __init__(self):
        self.tasks = []
        self.deleted_tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)
        self.deleted_tasks.append(task)

    def restore_task(self, task):
        self.deleted_tasks.remove(task)
        self.tasks.append(task)

    def get_tasks_by_category(self, category):
        if category == "All":
            return self.tasks
        return [task for task in self.tasks if task.category == category]

    def get_deleted_tasks(self):
        return self.deleted_tasks
