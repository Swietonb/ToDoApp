import customtkinter as ctk
from confirm_delete_dialog import ConfirmDeleteDialog


class DeletedTasksDialog(ctk.CTkToplevel):
    def __init__(self, parent, deleted_tasks):
        super().__init__(parent)
        self.title("Kosz - Usunięte zadania")
        self.geometry("800x600")

        self.deleted_tasks = deleted_tasks
        self.restored_task = None
        self.parent = parent  # Dodajemy referencję do TaskManagerApp

        # Główna ramka dialogowa
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Przewijalna ramka na usunięte zadania
        self.scroll_frame = ctk.CTkScrollableFrame(self.frame, height=500)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_deleted_tasks()

    def update_deleted_tasks(self):
        """Odświeżenie listy usuniętych zadań"""
        # Czyścimy ramkę przewijalną
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Wyświetlamy usunięte zadania
        for task in self.deleted_tasks:
            task_frame = ctk.CTkFrame(self.scroll_frame, corner_radius=10)
            task_frame.pack(fill="x", padx=10, pady=5, ipady=10)

            task_title = ctk.CTkLabel(task_frame, text=task.title, font=("Arial", 16))
            task_title.pack(side="left", padx=10)

            # Przycisk "Usuń na stałe" (zamieniamy kolejnością z przyciskiem "Przywróć")
            delete_button = ctk.CTkButton(task_frame, text="🗑", font=("Arial", 16), width=80, height=40,
                                          fg_color="red", command=lambda t=task: self.confirm_delete_task(t))
            delete_button.pack(side="right", padx=10)

            # Przycisk "Przywróć zadanie"
            restore_button = ctk.CTkButton(task_frame, text="⤾", font=("Arial", 16), width=80, height=40,
                                           command=lambda t=task: self.restore_task(t))
            restore_button.pack(side="right", padx=10)

    def restore_task(self, task):
        """Przywracamy zadanie i odświeżamy listę usuniętych zadań"""
        self.restored_task = task
        self.parent.task_manager.restore_task(task)  # Przywracamy zadanie w task_manager

        # Usuwamy zadanie z listy usuniętych na podstawie jego id
        self.deleted_tasks = [t for t in self.deleted_tasks if t.id != task.id]

        self.update_deleted_tasks()  # Odświeżamy widok po przywróceniu zadania

    def confirm_delete_task(self, task):
        """Wywołanie dialogu potwierdzenia usunięcia zadania"""
        ConfirmDeleteDialog(self, task, lambda: self.delete_task_permanently(task))

    def delete_task_permanently(self, task):
        """Trwale usuwamy zadanie z bazy danych i z listy"""
        self.deleted_tasks.remove(task)
        query = "DELETE FROM Tasks WHERE id = ?"
        self.parent.task_manager.conn.execute(query, (task.id,))
        self.parent.task_manager.conn.commit()
        self.update_deleted_tasks()  # Odświeżamy listę po usunięciu zadania