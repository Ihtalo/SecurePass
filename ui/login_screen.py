import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from core.auth import (
    master_password_exists,
    set_master_password,
    verify_master_password
)

class LoginScreen(ttk.Frame):
    def __init__(self, master, success_callback):
        super().__init__(master, padding=20)
        self.success_callback = success_callback

        ttk.Label(self, text="SecurePass", font=("Segoe UI", 20, "bold")).pack(pady=20)

        self.password_entry = ttk.Entry(self, show="*", width=30)
        self.password_entry.pack(pady=10)

        self.action_button = ttk.Button(self, bootstyle="primary")
        self.action_button.pack(pady=10)

        self.update_mode()

    def update_mode(self):
        if master_password_exists():
            self.action_button.config(text="Entrar", command=self.login)
        else:
            self.action_button.config(text="Criar senha mestre", command=self.create_password)

    def create_password(self):
        pwd = self.password_entry.get()
        if not pwd:
            messagebox.showerror("Erro", "Digite uma senha")
            return

        set_master_password(pwd)
        messagebox.showinfo("Sucesso", "Senha mestre criada")
        self.success_callback()

    def login(self):
        pwd = self.password_entry.get()
        if verify_master_password(pwd):
            self.success_callback()
        else:
            messagebox.showerror("Erro", "Senha incorreta")