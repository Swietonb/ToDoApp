import customtkinter as ctk
from task_manager import TaskManager
from add_task_dialog import AddTaskDialog
from deleted_tasks_dialog import DeletedTasksDialog
from datetime import datetime


class TaskManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ToDoApp")
        self.geometry("1200x800")

        # Inicjalizacja TaskManager
        self.task_manager = TaskManager()

        # Ładowanie zadań z bazy danych
        self.task_manager.load_tasks_from_db()

        self.category_var = ctk.StringVar(value="All")
        self.create_widgets()

        # Ustawienie proporcjonalnego skalowania
        self.grid_rowconfigure(1, weight=10)
        self.grid_columnconfigure(0, weight=1)

        # Wywołanie update_task_list, aby odświeżyć listę zadań po załadowaniu z bazy
        self.update_task_list()

        self.sort_tasks("Data (najbliższa)")

    def create_widgets(self):
        # Główna ramka
        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Ustawienie proporcji dla kolumn i wierszy ramki
        frame.grid_rowconfigure(1, weight=10)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # Filtrowanie po kategorii
        ctk.CTkLabel(frame, text="Kategoria").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.category_menu = ctk.CTkComboBox(
            frame,
            values=["All", "Work", "Personal", "Others"],
            variable=self.category_var,
            command=lambda category: self.update_task_list(category),
            width=200
        )

        self.category_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Dodanie etykiety dla sortowania
        ctk.CTkLabel(frame, text="Sortuj według:").grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # Dodanie opcji sortowania
        self.sort_var = ctk.StringVar(value="Data (najbliższa)")
        self.sort_menu = ctk.CTkComboBox(
            frame,
            values=["Data (najbliższa)", "Data (najdalsza)", "Priorytet (najwyższy)",
                    "Priorytet (najniższy)"],
            command=self.sort_tasks,
            width=200
        )
        self.sort_menu.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Domyślna opcja sortowania
        self.sort_menu.set("Data (najbliższa)")


        # Przewijalna ramka na zadania
        self.task_scroll_frame = ctk.CTkScrollableFrame(frame, height=600)
        self.task_scroll_frame.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

        # Przycisk dodawania zadań
        add_task_btn = ctk.CTkButton(frame, text="+", font=("Arial", 24), width=50, height=50, command=self.open_add_task_dialog)
        add_task_btn.grid(row=0, column=4, padx=5, pady=5, sticky="e")

        # Przycisk Kosz
        delete_btn = ctk.CTkButton(frame, text="🗑", font=("Arial", 24), width=50, height=50, command=self.open_deleted_tasks_dialog)
        delete_btn.grid(row=2, column=0, padx=5, pady=5, sticky="sw")

    def open_add_task_dialog(self):
        dialog = AddTaskDialog(self)
        dialog.lift()
        dialog.grab_set()
        self.wait_window(dialog)

        if dialog.task:
            self.task_manager.add_task(dialog.task)  # Dodajemy zadanie przez TaskManager
            self.update_task_list()
            current_sort_option = self.sort_menu.get()  # Pobieramy aktualną opcję sortowania
            self.sort_tasks(current_sort_option)  # Sortujemy zadania po dodaniu nowego

    def open_deleted_tasks_dialog(self):
        dialog = DeletedTasksDialog(self, self.task_manager.get_deleted_tasks())
        dialog.lift()
        dialog.grab_set()
        self.wait_window(dialog)

        if dialog.restored_task:
            self.update_task_list()  # Aktualizujemy listę zadań po przywróceniu

    def update_task_list(self, selected_category=None):
        """Aktualizuje listę zadań
        """
        # Jeśli przekazano kategorię, aktualizujemy zmienną self.category_var
        if selected_category:
            self.category_var.set(selected_category)

        # Czyszczenie starych zadań
        for widget in self.task_scroll_frame.winfo_children():
            widget.destroy()

        # Pobieranie zadań po kategorii
        tasks = self.task_manager.get_tasks_by_category(self.category_var.get())

        # Oddzielanie zadań ukończonych od nieukończonych
        not_completed_tasks = [task for task in tasks if not task.is_completed]
        completed_tasks = [task for task in tasks if task.is_completed]

        # Wyświetlanie niewykonanych zadań
        for task in not_completed_tasks:
            task_frame = ctk.CTkFrame(self.task_scroll_frame, corner_radius=10)
            task_frame.pack(fill="x", padx=10, pady=5, ipady=10)

            # Prostokąt z literą priorytetu
            priority_label = ctk.CTkLabel(task_frame, text=task.priority[0].upper(),
                                          font=("Arial", 16, "bold"),
                                          width=40, height=40, fg_color="#262624", corner_radius=5, anchor="center")
            priority_label.pack(side="left", padx=10)

            task_title = ctk.CTkLabel(task_frame, text=task.title, font=("Arial", 16))
            task_title.pack(side="left", padx=10)

            # Przycisk usunięcia zadania
            delete_button = ctk.CTkButton(task_frame, text="🗑", font=("Arial", 16), width=40, height=40,
                                          fg_color="red", command=lambda t=task: self.delete_task(t))
            delete_button.pack(side="right", padx=10)

            # Przycisk ukończenia zadania (⬛ -> ✔)
            complete_button = ctk.CTkButton(task_frame, text="⬛", font=("Arial", 16), width=40, height=40,
                                            fg_color="#262624", command=lambda t=task: self.toggle_task_completed(t))
            complete_button.pack(side="right", padx=10)

            # Wyświetlanie daty
            if task.due_date and task.due_time:
                due_date_text = f"{task.due_date}, {task.due_time}"
            elif task.due_date:
                due_date_text = task.due_date
            else:
                due_date_text = "Bezterminowe"

            fg_color = "#910412" if task.due_date and datetime.strptime(task.due_date,
                             "%d/%m/%y").date() < datetime.today().date() else "#262624"
            date_label = ctk.CTkLabel(task_frame, text=due_date_text,
                                      font=("Arial", 16),
                                      width=120, height=40, fg_color=fg_color, corner_radius=5, anchor="center")
            date_label.pack(side="right", padx=10)

        # Oddzielenie ukończonych zadań
        if completed_tasks:
            separator = ctk.CTkLabel(self.task_scroll_frame, text="--- Ukończone zadania ---", font=("Arial", 12))
            separator.pack(pady=10)

        # Wyświetlanie ukończonych zadań
        for task in completed_tasks:
            task_frame = ctk.CTkFrame(self.task_scroll_frame, corner_radius=10, fg_color="#30302f")
            task_frame.pack(fill="x", padx=10, pady=5, ipady=10)

            priority_label = ctk.CTkLabel(task_frame, text=task.priority[0].upper(),
                                          font=("Arial", 16, "bold"),
                                          width=40, height=40, fg_color="#2e2d2d", corner_radius=5, anchor="center")
            priority_label.pack(side="left", padx=10)

            task_title = ctk.CTkLabel(task_frame, text=task.title, font=("Arial", 16), text_color="gray")
            task_title.pack(side="left", padx=10)

            # Przycisk usunięcia zadania
            delete_button = ctk.CTkButton(task_frame, text="🗑", font=("Arial", 16), width=40, height=40,
                                          fg_color="red", command=lambda t=task: self.delete_task(t))
            delete_button.pack(side="right", padx=10)

            # Przycisk ukończenia zadania (✔)
            complete_button = ctk.CTkButton(task_frame, text="✔", font=("Arial", 16), width=40, height=40,
                                            fg_color="#262624", command=lambda t=task: self.toggle_task_completed(t))
            complete_button.pack(side="right", padx=10)

            # Wyświetlanie daty
            if task.due_date and task.due_time:
                due_date_text = f"{task.due_date}, {task.due_time}"
            elif task.due_date:
                due_date_text = task.due_date
            else:
                due_date_text = "Bezterminowe"

            date_label = ctk.CTkLabel(task_frame, text=due_date_text,
                                      font=("Arial", 16),
                                      width=120, height=40, fg_color="#2e2d2d", corner_radius=5, anchor="center")
            date_label.pack(side="right", padx=10)

    def toggle_task_completed(self, task):
        """Przełącz status ukończenia zadania"""
        self.task_manager.mark_task_completed(task)
        self.update_task_list()  # Odświeżamy listę zadań

    def delete_task(self, task):
        self.task_manager.remove_task(task)
        self.update_task_list()

    def sort_tasks(self, sort_option):
        def get_sort_key_by_date(task):
            # Konwertujemy daty na obiekt datetime, zadania bez daty są sortowane na końcu
            if task.due_date:
                return datetime.strptime(task.due_date, "%d/%m/%y"), task.due_time or "00:00"
            else:
                return datetime.max, "23:59"  # Zadania bezterminowe na końcu

        if sort_option == "Data (najbliższa)":
            # Sortujemy po dacie (najbliższa), zadania bez daty na końcu
            self.task_manager.tasks.sort(key=get_sort_key_by_date)
        elif sort_option == "Data (najdalsza)":
            # Sortujemy po dacie (najdalsza), zadania bez daty na końcu
            self.task_manager.tasks.sort(key=get_sort_key_by_date, reverse=True)
        elif sort_option == "Priorytet (najwyższy)":
            # Sortowanie po priorytecie - zadania z najwyższym priorytetem na górze
            priority_map = {"Wysoki": 1, "Średni": 2, "Niski": 3}
            self.task_manager.tasks.sort(
                key=lambda task: (priority_map.get(task.priority, 99), task.due_date or "9999-12-31"))
        elif sort_option == "Priorytet (najniższy)":
            # Sortowanie po priorytecie odwrotnie
            priority_map = {"Wysoki": 1, "Średni": 2, "Niski": 3}
            self.task_manager.tasks.sort(
                key=lambda task: (priority_map.get(task.priority, 99), task.due_date or "9999-12-31"), reverse=True)

        # Po posortowaniu, odświeżamy listę zadań
        self.update_task_list()
