from task import Task
import customtkinter as ctk
from tkcalendar import Calendar
import tkinter as tk
from datetime import date, datetime


class AddTaskDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Referencja do głównego okna
        self.title("Dodaj nowe zadanie")
        self.geometry("500x600")  # Rozmiar okna

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
        priority_menu = ctk.CTkComboBox(self, values=["Wysoki", "Średni", "Niski"], variable=self.priority_var,
                                        width=300)
        priority_menu.pack(pady=10)

        # Etykieta i menu rozwijane dla kategorii
        category_label = ctk.CTkLabel(self, text="Kategoria:", font=("Arial", 18))
        category_label.pack(pady=10)

        self.category_var = ctk.StringVar(value="Others")
        category_menu = ctk.CTkComboBox(self, values=["Work", "Personal", "Others"], variable=self.category_var,
                                        width=300)
        category_menu.pack(pady=10)

        # Etykieta i pole na datę
        ctk.CTkLabel(self, text="Data wykonania:", font=("Arial", 18)).pack(pady=10)

        date_frame = ctk.CTkFrame(self)
        date_frame.pack(pady=10)

        self.selected_date = tk.StringVar(value="Wybierz datę")

        # Pole do wyświetlania wybranej daty
        self.date_entry = ctk.CTkEntry(date_frame, textvariable=self.selected_date, state="readonly", width=200)
        self.date_entry.pack(side="left", padx=5)

        # Przycisk otwierający kalendarz
        date_button = ctk.CTkButton(date_frame, text="📅", width=40, command=self.open_calendar)
        date_button.pack(side="left", padx=5)

        # Wybór godziny z list rozwijanych
        ctk.CTkLabel(self, text="Godzina wykonania:", font=("Arial", 18)).pack(pady=10)

        time_frame = ctk.CTkFrame(self)
        time_frame.pack(pady=10)

        # Lista rozwijana dla godzin
        self.hour_var = tk.StringVar(value="")  # Pusta wartość początkowa
        hour_combo = ctk.CTkComboBox(time_frame, values=[f"{i:02d}" for i in range(24)], variable=self.hour_var,
                                     width=80)
        hour_combo.pack(side="left", padx=5)

        # Lista rozwijana dla minut
        self.minute_var = tk.StringVar(value="")  # Pusta wartość początkowa
        minute_combo = ctk.CTkComboBox(time_frame, values=[f"{i:02d}" for i in range(60)], variable=self.minute_var,
                                       width=80)
        minute_combo.pack(side="left", padx=5)

        # Sekcja przycisków na dole (Dodaj i Anuluj)
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(pady=20)

        add_task_btn = ctk.CTkButton(buttons_frame, text="Dodaj zadanie", command=self.add_task, width=140)
        add_task_btn.grid(row=0, column=0, padx=10)

        cancel_btn = ctk.CTkButton(buttons_frame, text="Anuluj", command=self.destroy, width=140)
        cancel_btn.grid(row=0, column=1, padx=10)

    def open_calendar(self):
        """Otwieramy okno z kalendarzem do wyboru daty"""
        cal_window = ctk.CTkToplevel(self)
        cal_window.title("Wybierz datę")

        # Ustawienie okna na wierzchu
        cal_window.lift()
        cal_window.grab_set()

        # Kalendarz do wyboru daty
        cal = Calendar(cal_window, selectmode="day", year=date.today().year, month=date.today().month,
                       day=date.today().day)
        cal.pack(pady=20)

        # Przycisk do zatwierdzenia daty
        select_button = ctk.CTkButton(cal_window, text="Zatwierdź", command=lambda: self.set_date(cal, cal_window))
        select_button.pack(pady=10)

    def set_date(self, cal, window):
        """Ustawia wybraną datę w odpowiednim formacie"""
        selected_date = cal.get_date()
        # Konwersja daty z formatu 'mm/dd/yy' na 'dd/mm/yy'
        formatted_date = datetime.strptime(selected_date, "%m/%d/%y").strftime("%d/%m/%y")
        self.selected_date.set(formatted_date)
        window.destroy()

    def add_task(self):
        task_title = self.task_title_entry.get()
        if not task_title:
            ctk.CTkLabel(self, text="Tytuł nie może być pusty!", font=("Arial", 14), fg_color="red").pack()
            return

        task_priority = self.priority_var.get()
        task_category = self.category_var.get()
        task_due_date = self.selected_date.get()

        # Pobieranie godziny i minut z ComboBox
        task_hour = self.hour_var.get()
        task_minute = self.minute_var.get()

        # Jeśli godzina i minuta są puste, ustawiamy task_due_time na None
        if not task_hour and not task_minute:
            task_due_time = None
        else:
            task_due_time = f"{task_hour or '00'}:{task_minute or '00'}"

        # Obsługa błędów:
        if task_due_time is not None and task_due_date == "Wybierz datę":
            # Nie można ustawić godziny bez daty
            ctk.CTkLabel(self, text="Nie można ustawić godziny bez daty!", font=("Arial", 14), fg_color="red").pack()
            return

        # Jeśli użytkownik nie wybrał daty, ustawiamy 'None' zamiast 'Wybierz datę'
        if task_due_date == "Wybierz datę":
            task_due_date = None
            task_due_time = None  # Jeśli brak daty, resetujemy godzinę na None

        # Tworzymy nowe zadanie na podstawie wprowadzonych danych
        task = Task(title=task_title, priority=task_priority, category=task_category, due_date=task_due_date,
                    due_time=task_due_time)
        self.task = task  # Zapisywanie utworzonego zadania
        self.destroy()

