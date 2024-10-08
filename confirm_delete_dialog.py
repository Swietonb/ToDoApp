from simple_dialog import SimpleDialog

class ConfirmDeleteDialog(SimpleDialog):
    def __init__(self, parent, task, confirm_callback):
        message = f"Czy na pewno chcesz usunąć zadanie '{task.title}' na stałe?"
        super().__init__(parent, message, confirm_callback)
        self.task = task
