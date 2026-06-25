import tkinter as tk
from tkinter import messagebox

from windows.admin_dashboard_window import AdminDashboardWindow


class AdminLoginWindow:

    def __init__(self, parent, manager):
        self.parent = parent
        self.manager = manager
        self.window = tk.Toplevel(parent)
        self.window.title("Admin Login")
        self.window.geometry("420x300")
        self.window.resizable(False, False)
        self.window.grab_set()

        tk.Label(
            self.window,
            text="Admin Login",
            font=("Arial", 17, "bold")
        ).pack(pady=(26, 18))

        tk.Label(self.window, text="Username").pack()
        self.username_entry = tk.Entry(self.window, width=30)
        self.username_entry.pack(pady=(4, 12))

        tk.Label(self.window, text="Password").pack()
        self.password_entry = tk.Entry(self.window, show="*", width=30)
        self.password_entry.pack(pady=(4, 18))

        tk.Button(
            self.window,
            text="Login",
            width=20,
            command=self.login
        ).pack()

        self.window.bind("<Return>", lambda event: self.login())

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password.")
            return

        admin = self.manager.login_admin(username, password)

        if admin:
            self.window.destroy()
            self.parent.withdraw()
            AdminDashboardWindow(
                self.parent,
                self.manager,
                admin,
                self.show_login
            )
        else:
            messagebox.showerror("Error", "Invalid admin username or password.")

    def show_login(self):
        self.parent.deiconify()
