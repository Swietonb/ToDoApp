import sqlite3
from task import Task

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.deleted_tasks = []
        self.conn = sqlite3.connect('tasks.db')
        self.create_table()

    def create_table(self):
        """Tworzymy tabelę, jeśli jeszcze nie istnieje"""
        query = """
        CREATE TABLE IF NOT EXISTS Tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            priority TEXT,
            category TEXT,
            is_deleted BOOLEAN,
            is_completed BOOLEAN DEFAULT 0
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def load_tasks_from_db(self):
        """Ładujemy wszystkie zadania z bazy danych (zarówno aktywne, jak i usunięte) do pamięci"""
        query = "SELECT * FROM Tasks"
        cursor = self.conn.execute(query)
        for row in cursor:
            task = Task(title=row[1], priority=row[2], category=row[3])
            task.id = row[0]
            task.is_deleted = row[4]  # Kolumna is_deleted
            task.is_completed = row[5]  # Kolumna is_completed
            if task.is_deleted:
                self.deleted_tasks.append(task)
            else:
                self.tasks.append(task)

    def add_task(self, task):
        """Dodaj zadanie do pamięci i bazy danych"""
        self.tasks.append(task)
        query = "INSERT INTO Tasks (title, priority, category, is_deleted, is_completed) VALUES (?, ?, ?, 0, 0)"
        cursor = self.conn.execute(query, (task.title, task.priority, task.category))
        self.conn.commit()
        task.id = cursor.lastrowid  # Pobieramy wygenerowane id zadania

    def remove_task(self, task):
        """Oznaczamy zadanie jako usunięte"""
        self.tasks.remove(task)
        self.deleted_tasks.append(task)
        if hasattr(task, 'id'):  # Sprawdzamy, czy zadanie ma przypisane id
            query = "UPDATE Tasks SET is_deleted = 1 WHERE id = ?"
            self.conn.execute(query, (task.id,))
            self.conn.commit()

    def restore_task(self, task):
        """Przywracamy usunięte zadanie"""
        # Znajdujemy zadanie w usuniętych po id
        task_to_restore = next((t for t in self.deleted_tasks if t.id == task.id), None)
        if task_to_restore:
            self.deleted_tasks.remove(task_to_restore)  # Usuwamy zadanie z listy usuniętych
            self.tasks.append(task_to_restore)  # Dodajemy zadanie z powrotem do listy aktywnych
            query = "UPDATE Tasks SET is_deleted = 0 WHERE id = ?"
            self.conn.execute(query, (task.id,))
            self.conn.commit()
            return task_to_restore  # Zwracamy przywrócone zadanie

    def get_tasks_by_category(self, category):
        """Pobieramy zadania według kategorii"""
        if category == "All":
            return self.tasks
        return [task for task in self.tasks if task.category == category]

    def get_deleted_tasks(self):
        """Pobieramy usunięte zadania"""
        return self.deleted_tasks

    def mark_task_completed(self, task):
        """Oznaczamy zadanie jako ukończone lub nieukończone"""
        task.is_completed = not task.is_completed
        query = "UPDATE Tasks SET is_completed = ? WHERE id = ?"
        self.conn.execute(query, (task.is_completed, task.id))
        self.conn.commit()
