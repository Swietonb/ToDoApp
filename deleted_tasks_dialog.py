import customtkinter as ctk

class DeletedTasksDialog(ctk.CTkToplevel):
    def __init__(self, parent, deleted_tasks):
        super().__init__(parent)
        self.title("Kosz - Usunięte zadania")
        self.geometry("800x600")

        self.deleted_tasks = deleted_tasks
        self.restored_task = None

        # Główna ramka dialogowa
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Przewijalna ramka na usunięte zadania
        self.scroll_frame = ctk.CTkScrollableFrame(self.frame, height=500)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_deleted_tasks()

    def update_deleted_tasks(self):
        # Czyścimy ramkę przewijalną
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Wyświetlamy usunięte zadania
        for task in self.deleted_tasks:
            task_frame = ctk.CTkFrame(self.scroll_frame, corner_radius=10)
            task_frame.pack(fill="x", padx=10, pady=5, ipady=10)

            task_title = ctk.CTkLabel(task_frame, text=task.title, font=("Arial", 16))
            task_title.pack(side="left", padx=10)

            # Przycisk "Przywróć"
            restore_button = ctk.CTkButton(task_frame, text="Przywróć", font=("Arial", 16), width=80, height=40,
                                           command=lambda t=task: self.restore_task(t))
            restore_button.pack(side="right", padx=10)

    def restore_task(self, task):
        # Przywracamy zadanie
        self.deleted_tasks.remove(task)
        self.restored_task = task
        self.destroy()
