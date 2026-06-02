import tkinter as tk
from services.api import scan_request
from pages.history import History

class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.config(bg = "white")
        self.controller = controller

        label = tk.Label(self, text = "Welcome to the dashboard !", bg="white", font=("Times New Roman", 24), fg="#031436")
        label.pack(pady=(20, 20))

        question = tk.Label(self, text = "Which adress would you like to check ?", bg="white", font=("Arial", 12), fg="#031436")
        question.pack(pady=(0, 20))

        cont = tk.Frame(self, bg="white")
        cont.pack(pady=(10, 20))

        adress_label = tk.Label(cont, text = "Adress or IP adress:", bg="white", font=("Arial", 13), fg="#031436")
        adress_label.grid(
            row=0,
            column=0,
            padx= 30,
            sticky="e"
        )

        self.address_entry = tk.Entry(cont, font=("Arial", 12), width=30, fg="#031436", bg="white")
        self.address_entry.grid(
            row=0,
            column= 1,
            padx= 10,
            pady= 10
        )

        form = tk.Frame(self, bg="white")
        form.pack()

        check_button = tk.Button(form, text="Check", font=("Arial", 13), bg="#031436", fg="white", width=10, command=self.scan)
        check_button.grid(
            row=0,
            column= 0,
            padx= 10,
            pady= 10
        )

        history_button = tk.Button(form, text="History", font=("Arial", 13), bg="#031436", fg="white",width=10, command=self.direction)
        history_button.grid(
            row=0,
            column= 1,
            padx= 10,
            pady= 10
        )

        self.label3 = tk.Label(self, text = "", bg="white", font=("Arial", 12), fg="#031436", justify="left")
        self.label3.pack(pady=(10, 0))
        
        self.risque = tk.Label(self, text ="", bg="white", fg="#031436", font=("Arial", 12))
        self.risque.pack()

    def scan(self):
        host = self.address_entry.get().strip()
        token = self.controller.token

        if not host:
            self.label3.config(text="Veuillez saisir une adresse ou un IP.", fg="#CF0B0B")
            return

        result = scan_request(token, host)

        if result:
            self.label3.config(
                text=(
                    f"Host: {result.get('host')}\n"
                    f"Open ports: {result.get('open_ports')}\n"
                    f"Score : {result.get('score')}"
                ),
                fg="#031436"
            )
        else:
            self.label3.config(text="Failed to perform scan.", fg="#CF0B0B")

    def direction(self):
        self.controller.show_frame(History)