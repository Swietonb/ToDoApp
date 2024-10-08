import customtkinter as ctk
from ui import TaskManagerApp

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Możesz ustawić tryb jasny lub ciemny
    app = TaskManagerApp()
    app.mainloop()
