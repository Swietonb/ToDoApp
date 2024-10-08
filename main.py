import customtkinter as ctk
from ui import TaskManagerApp

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = TaskManagerApp()
    app.mainloop()
