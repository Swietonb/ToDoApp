import customtkinter as ctk

class SimpleDialog(ctk.CTkToplevel):
    def __init__(self, parent, message, confirm_callback, max_line_length=50):
        super().__init__(parent)
        self.title("Potwierdzenie")
        self.geometry("350x150")
        self.parent = parent
        self.confirm_callback = confirm_callback

        # Ustawiamy okno na wierzchu
        self.attributes("-topmost", True)

        # Sprawdzenie długości tekstu i dzielenie na dwie linie, jeśli za długi
        self.message = self.split_message(message, max_line_length)

        # Etykieta z wiadomością (wyśrodkowana)
        self.label = ctk.CTkLabel(self, text=self.message, anchor="center", justify="center")
        self.label.pack(pady=20)

        # Ramka na przyciski
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10, padx=10, fill="x", expand=True)

        # Przycisk "Tak"
        confirm_button = ctk.CTkButton(button_frame, text="Tak", command=self.on_confirm, width=80)
        confirm_button.pack(side="left", padx=10)

        # Przycisk "Nie"
        cancel_button = ctk.CTkButton(button_frame, text="Nie", command=self.on_cancel, width=80)
        cancel_button.pack(side="right", padx=10)

    def split_message(self, message, max_length):
        """Dzieli wiadomość na dwie linie, jeśli jej długość przekracza max_length"""
        if len(message) <= max_length:
            return message
        # Znajdujemy środek wiadomości, ale dzielimy na słowach (jeśli to możliwe)
        midpoint = max_length // 2
        space_index = message.find(' ', midpoint)
        if space_index == -1:
            space_index = midpoint
        return message[:space_index] + '\n' + message[space_index+1:]

    def on_confirm(self):
        """Akcja po kliknięciu przycisku 'Tak'."""
        if self.confirm_callback:
            self.confirm_callback()
        self.destroy()

    def on_cancel(self):
        """Akcja po kliknięciu przycisku 'Nie'."""
        self.destroy()
