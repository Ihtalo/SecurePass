import tkinter as tk
from core.generator import generate_password
from core.storage import add_password

class AddPasswordScreen(tk.Frame):
    def __init__(self, master, back_callback):
        super().__init__(master)
        self.back_callback = back_callback

        tk.Label(self, text="Nova Senha", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Serviço").pack()
        self.service_entry = tk.Entry(self)
        self.service_entry.pack()

        tk.Label(self, text="Usuário").pack()
        self.user_entry = tk.Entry(self)
        self.user_entry.pack()

        tk.Label(self, text="Senha").pack()
        self.password_entry = tk.Entry(self)
        self.password_entry.pack()

        tk.Button(self, text="Gerar Senha", command=self.generate).pack(pady=5)
        tk.Button(self, text="Salvar", command=self.save).pack(pady=5)
        tk.Button(self, text="Voltar", command=self.back_callback).pack(pady=5)

    def generate(self):
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, generate_password())

    def save(self):
        entry = {
            "service": self.service_entry.get(),
            "username": self.user_entry.get(),
            "password": self.password_entry.get()
        }

        add_password(entry)
        self.back_callback()