import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
from core.storage import load_passwords, delete_password
from core.backup import export_passwords, import_passwords

class Dashboard(ttk.Frame):
    def __init__(self, master, add_callback):
        super().__init__(master, padding=10)
        self.add_callback = add_callback
        self.passwords = []
        self.password_visible = False

        ttk.Label(self, text="SecurePass - Cofre", font=("Segoe UI", 16, "bold")).pack(pady=10)

        # Tabela moderna
        columns = ("service", "username")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        self.tree.heading("service", text="Serviço")
        self.tree.heading("username", text="Usuário")
        self.tree.pack(fill="both", expand=True, pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Área de detalhes
        detail = ttk.Frame(self)
        detail.pack(fill="x", pady=5)

        self.service_label = ttk.Label(detail, text="Serviço: -")
        self.service_label.pack(anchor="w")

        self.user_label = ttk.Label(detail, text="Usuário: -")
        self.user_label.pack(anchor="w")

        self.password_label = ttk.Label(detail, text="Senha: -")
        self.password_label.pack(anchor="w")

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Mostrar/Ocultar senha", command=self.toggle_password, bootstyle="info").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Copiar senha", command=self.copy_password, bootstyle="secondary").pack(side="left", padx=5)

        # Botões inferiores
        bottom = ttk.Frame(self)
        bottom.pack(fill="x", pady=5)

        ttk.Button(bottom, text="Adicionar", command=self.add_callback, bootstyle="success").pack(side="left", padx=5)
        ttk.Button(bottom, text="Excluir", command=self.delete_selected, bootstyle="danger").pack(side="left", padx=5)
        ttk.Button(bottom, text="Exportar", command=self.export_data, bootstyle="primary").pack(side="right", padx=5)
        ttk.Button(bottom, text="Importar", command=self.import_data, bootstyle="primary").pack(side="right", padx=5)

        self.refresh_list()

    def refresh_list(self):
        self.passwords = load_passwords()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for entry in self.passwords:
            self.tree.insert("", "end", values=(entry["service"], entry["username"]))

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        index = self.tree.index(selected[0])
        entry = self.passwords[index]

        self.service_label.config(text=f"Serviço: {entry['service']}")
        self.user_label.config(text=f"Usuário: {entry['username']}")

        self.current_password = entry["password"]
        self.password_visible = False
        self.password_label.config(text="Senha: ********")

    def toggle_password(self):
        if not hasattr(self, "current_password"):
            return

        self.password_visible = not self.password_visible

        if self.password_visible:
            self.password_label.config(text=f"Senha: {self.current_password}")
        else:
            self.password_label.config(text="Senha: ********")

    def copy_password(self):
        if not hasattr(self, "current_password"):
            return

        self.clipboard_clear()
        self.clipboard_append(self.current_password)
        messagebox.showinfo("Copiado", "Senha copiada")

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            return

        index = self.tree.index(selected[0])
        service = self.passwords[index]["service"]

        delete_password(service)
        self.refresh_list()
        messagebox.showinfo("Removido", "Senha excluída")

    def export_data(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".spass",
            filetypes=[("SecurePass Backup", "*.spass")]
        )
        if file_path:
            export_passwords(file_path)
            messagebox.showinfo("Exportado", "Backup salvo")

    def import_data(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("SecurePass Backup", "*.spass")]
        )
        if file_path:
            try:
                import_passwords(file_path)
                self.refresh_list()
                messagebox.showinfo("Importado", "Backup restaurado")
            except Exception as e:
                messagebox.showerror("Erro", str(e))