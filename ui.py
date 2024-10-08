import customtkinter as ctk
from task_manager import TaskManager
from add_task_dialog import AddTaskDialog
from deleted_tasks_dialog import DeletedTasksDialog


class TaskManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager")
        self.geometry("1200x800")

        # Inicjalizacja TaskManager
        self.task_manager = TaskManager()

        # Ładujemy zadania z bazy danych
        self.task_manager.load_tasks_from_db()

        self.category_var = ctk.StringVar(value="All")
        self.create_widgets()

        # Ustawienie proporcjonalnego skalowania
        self.grid_rowconfigure(1, weight=10)
        self.grid_columnconfigure(0, weight=1)

        # Wywołanie update_task_list, aby odświeżyć listę zadań po załadowaniu z bazy
        self.update_task_list()

    def create_widgets(self):
        # Główna ramka
        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Ustawienie proporcji dla kolumn i wierszy ramki
        frame.grid_rowconfigure(1, weight=10)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # Kategoria filtrów
        ctk.CTkLabel(frame, text="Kategoria").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.category_menu = ctk.CTkComboBox(frame, values=["All", "Work", "Personal", "Others"],
                                             variable=self.category_var, command=self.update_task_list)
        self.category_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Przewijalna ramka na zadania
        self.task_scroll_frame = ctk.CTkScrollableFrame(frame, height=600)
        self.task_scroll_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Przycisk dodawania zadań
        add_task_btn = ctk.CTkButton(frame, text="+", font=("Arial", 24), width=50, height=50, command=self.open_add_task_dialog)
        add_task_btn.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # Przycisk Kosz
        delete_btn = ctk.CTkButton(frame, text="🗑", font=("Arial", 24), width=50, height=50, command=self.open_deleted_tasks_dialog)
        delete_btn.grid(row=2, column=0, padx=5, pady=5, sticky="sw")

    def open_add_task_dialog(self):
        # Otwieramy dialog do dodawania zadań
        dialog = AddTaskDialog(self)
        dialog.lift()
        dialog.grab_set()
        self.wait_window(dialog)

        if dialog.task:  # Jeśli dodano zadanie
            self.task_manager.add_task(dialog.task)  # Dodajemy zadanie przez TaskManager
            self.update_task_list()

    def open_deleted_tasks_dialog(self):
        # Otwieramy dialog do usuniętych zadań
        dialog = DeletedTasksDialog(self, self.task_manager.get_deleted_tasks())
        dialog.lift()
        dialog.grab_set()
        self.wait_window(dialog)

        if dialog.restored_task:
            self.update_task_list()  # Aktualizujemy listę zadań po przywróceniu

    def update_task_list(self):
        # Czyścimy stare zadania
        for widget in self.task_scroll_frame.winfo_children():
            widget.destroy()

        # Pobieramy zadania według kategorii
        tasks = self.task_manager.get_tasks_by_category(self.category_var.get())

        # Oddzielamy zadania ukończone od nieukończonych
        not_completed_tasks = [task for task in tasks if not task.is_completed]
        completed_tasks = [task for task in tasks if task.is_completed]

        # Wyświetlamy niewykonane zadania
        for task in not_completed_tasks:
            task_frame = ctk.CTkFrame(self.task_scroll_frame, corner_radius=10)
            task_frame.pack(fill="x", padx=10, pady=5, ipady=10)

            task_title = ctk.CTkLabel(task_frame, text=task.title, font=("Arial", 16))
            task_title.pack(side="left", padx=10)

            # Najpierw przycisk usunięcia zadania
            delete_button = ctk.CTkButton(task_frame, text="🗑", font=("Arial", 16), width=40, height=40,
                                          fg_color="red", command=lambda t=task: self.delete_task(t))
            delete_button.pack(side="right", padx=10)

            # Potem przycisk ukończenia zadania (⬛ -> ✔), z kolorem #262624
            complete_button = ctk.CTkButton(task_frame, text="⬛", font=("Arial", 16), width=40, height=40,
                                            fg_color="#262624",  # Kolor przycisku ukończenia
                                            command=lambda t=task: self.toggle_task_completed(t))
            complete_button.pack(side="right", padx=10)

        # Dodajemy estetyczne oddzielenie ukończonych zadań
        if completed_tasks:
            separator = ctk.CTkLabel(self.task_scroll_frame, text="--- Ukończone zadania ---", font=("Arial", 12))
            separator.pack(pady=10)

        # Wyświetlamy ukończone zadania (z kolorem #30302f)
        for task in completed_tasks:
            task_frame = ctk.CTkFrame(self.task_scroll_frame, corner_radius=10,
                                      fg_color="#30302f")  # Kolor ukończonego zadania
            task_frame.pack(fill="x", padx=10, pady=5, ipady=10)

            task_title = ctk.CTkLabel(task_frame, text=task.title, font=("Arial", 16), text_color="gray")
            task_title.pack(side="left", padx=10)

            # Najpierw przycisk usunięcia zadania
            delete_button = ctk.CTkButton(task_frame, text="🗑", font=("Arial", 16), width=40, height=40,
                                          fg_color="red", command=lambda t=task: self.delete_task(t))
            delete_button.pack(side="right", padx=10)

            # Potem przycisk ukończenia zadania (✔), z kolorem #262624
            complete_button = ctk.CTkButton(task_frame, text="✔", font=("Arial", 16), width=40, height=40,
                                            fg_color="#262624", command=lambda t=task: self.toggle_task_completed(t))
            complete_button.pack(side="right", padx=10)

    def toggle_task_completed(self, task):
        """Przełącz status ukończenia zadania"""
        self.task_manager.mark_task_completed(task)
        self.update_task_list()  # Odświeżamy listę zadań

    def delete_task(self, task):
        # Przenosimy zadanie do usuniętych
        self.task_manager.remove_task(task)
        self.update_task_list()
