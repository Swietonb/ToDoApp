from task import Task
import customtkinter as ctk

class AddTaskDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Referencja do głównego okna
        self.title("Dodaj nowe zadanie")
        self.geometry("500x400")  # Rozmiar okna

        self.task = None

        # Etykieta i pole tekstowe dla tytułu zadania
        task_title_label = ctk.CTkLabel(self, text="Tytuł zadania:", font=("Arial", 18))
        task_title_label.pack(pady=10)

        self.task_title_entry = ctk.CTkEntry(self, font=("Arial", 16), width=300)
        self.task_title_entry.pack(pady=10)

        # Etykieta i menu rozwijane dla priorytetu
        priority_label = ctk.CTkLabel(self, text="Priorytet:", font=("Arial", 18))
        priority_label.pack(pady=10)

        self.priority_var = ctk.StringVar(value="Średni")
        priority_menu = ctk.CTkComboBox(self, values=["Wysoki", "Średni", "Niski"], variable=self.priority_var, width=300)
        priority_menu.pack(pady=10)

        # Etykieta i menu rozwijane dla kategorii
        category_label = ctk.CTkLabel(self, text="Kategoria:", font=("Arial", 18))
        category_label.pack(pady=10)

        self.category_var = ctk.StringVar(value="Others")
        category_menu = ctk.CTkComboBox(self, values=["Work", "Personal", "Others"], variable=self.category_var, width=300)
        category_menu.pack(pady=10)

        # Sekcja przycisków na dole (Dodaj i Anuluj)
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(pady=20)

        add_task_btn = ctk.CTkButton(buttons_frame, text="Dodaj zadanie", command=self.add_task, width=140)
        add_task_btn.grid(row=0, column=0, padx=10)

        cancel_btn = ctk.CTkButton(buttons_frame, text="Anuluj", command=self.destroy, width=140)
        cancel_btn.grid(row=0, column=1, padx=10)

    def add_task(self):
        task_title = self.task_title_entry.get()
        if not task_title:
            ctk.CTkLabel(self, text="Tytuł nie może być pusty!", font=("Arial", 14), fg_color="red").pack()
            return

        # Tworzymy nowe zadanie na podstawie wprowadzonych danych
        task = Task(title=task_title, priority=self.priority_var.get(), category=self.category_var.get())
        self.task = task  # Zapisywanie utworzonego zadania
        self.destroy()
