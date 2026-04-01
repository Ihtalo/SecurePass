import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ui.login_screen import LoginScreen
from ui.dashboard import Dashboard
from ui.add_password import AddPasswordScreen

class SecurePassApp:
    def __init__(self):
        # Janela com tema moderno
        self.root = ttk.Window(themename="darkly")
        self.root.title("SecurePass")
        self.root.geometry("700x450")
        self.root.resizable(False, False)

        self.current_frame = None
        self.show_login()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_login(self):
        self.clear_frame()
        self.current_frame = LoginScreen(self.root, self.show_dashboard)
        self.current_frame.pack(fill="both", expand=True)

    def show_dashboard(self):
        self.clear_frame()
        self.current_frame = Dashboard(self.root, self.show_add_password)
        self.current_frame.pack(fill="both", expand=True)

    def show_add_password(self):
        self.clear_frame()
        self.current_frame = AddPasswordScreen(self.root, self.show_dashboard)
        self.current_frame.pack(fill="both", expand=True)

    def run(self):
        self.root.mainloop()