import tkinter as tk
import requests
from pages.dashboard import Dashboard
from services.api import login_request

TOKEN = None
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.config(bg = "white")
        self.controller = controller

        title = tk.Label(self, text = "Log in", bg="white", font=("Times New Roman", 34), fg="#031436")
        title.pack(pady=(30, 40))

        form_frame = tk.Frame(self, bg="white")
        form_frame.pack()

        username_label = tk.Label(form_frame, text="Username:", bg="white", font=("Arial", 12), fg="#031436")
        username_label.grid(
            row=0,
            column=0,
            sticky="e"
        )

        self.username_entry = tk.Entry(form_frame, font=("Arial", 12), width=28, fg="#031436", bg="white")
        self.username_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        password_label = tk.Label(form_frame, text="Password:", bg="white", font=("Arial", 12), fg="#031436")
        password_label.grid(
            row=1,
            column=0,
            pady=10,
            sticky="e"
        )

        self.password_entry = tk.Entry(form_frame, show="*", font=("Arial", 12), width=28, fg="#031436", bg="white")
        self.password_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=10
        )

        self.message_label = tk.Label(self, text="", bg="white", fg="#CF0B0B", font=("Times New Roman", 10))
        self.message_label.pack(pady=(15, 0))

        login_button = tk.Button(self, text="Log in", font=("Arial", 13), bg="#031436", fg="white", width=10, command=self.login)
        login_button.pack(pady=(20, 0))

    def login(self):
        global TOKEN

        username_value = self.username_entry.get()
        password_value = self.password_entry.get()

        token = login_request(username_value, password_value)

        if token:
            self.controller.token = token
            print("Login successful !")

            self.controller.show_frame(Dashboard)

        else:
            self.message_label.config(text="Invalid username or password ! Try again.")
            self.message_label.update()

