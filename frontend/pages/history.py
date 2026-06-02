import tkinter as tk
import requests
from services.api import history_request
from services.api import pdf_request

class History(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.config(bg = "white")
        self.controller = controller

        label = tk.Label(self, text = "Scan history", bg="white", font=("Times New Roman", 30), fg="#031436")
        label.pack(pady=20, padx=20)

        self.history_container = tk.Frame(self, bg="white")
        self.history_container.pack(pady=(10, 0), padx=40, fill="x")

        self.message_label = tk.Label(self, text="", bg="white", font=("Arial", 12), fg="#D33F3F")
        self.message_label.pack(pady=(5, 0))

        pdf_bouton = tk.Button(self, text="Download PDF report", font=("Arial", 13), bg="#031436", fg="white", width=20, command=self.download_pdf)
        pdf_bouton.pack(pady=20)

    def refresh(self):
        for widget in self.history_container.winfo_children():
            widget.destroy()

        self.message_label.config(text="")

        history = history_request(self.controller.token)

        if history is None:
            self.message_label.config(text="Failed to retrieve history. Vérifiez votre connexion ou jeton.")
            return

        if not history:
            self.message_label.config(text="Aucun historique disponible.")
            return

        for item in history:
            item_text = (
                f"Host: {item['host']}\n  Ports: {item['ports']}\n  Risque: {item['risque']}\n  Score: {item['score']}\n  Date: {item['date_scan']}"
            )
            item_label = tk.Label(self.history_container, text=item_text, bg="white", font=("Arial", 12), fg="#031436", anchor="w", justify="left")
            item_label.pack(fill="x", pady=10)

    def download_pdf(self):
        pdf_request(self.controller.token)
            