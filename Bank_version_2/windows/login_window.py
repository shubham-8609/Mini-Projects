import tkinter as tk
from tkinter import messagebox

from manager import Manager
from windows.dashboard import DashboardWindow
from windows.register_window import RegisterWindow


class LoginWindow:

    def __init__(self):
        self.manager = Manager()
        self.window = tk.Tk()
        self.window.title("Bank Management System Pro")
        self.window.geometry("460x360")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        title = tk.Label(
            self.window,
            text="Bank Management System Pro",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=(28, 20))

        tk.Label(self.window, text="Username").pack()
        self.username_entry = tk.Entry(self.window, width=32)
        self.username_entry.pack(pady=(4, 12))

        tk.Label(self.window, text="Password").pack()
        self.password_entry = tk.Entry(self.window, show="*", width=32)
        self.password_entry.pack(pady=(4, 18))

        tk.Button(
            self.window,
            text="Login",
            width=22,
            command=self.login
        ).pack(pady=(0, 10))

        tk.Button(
            self.window,
            text="Register",
            width=22,
            command=self.open_register
        ).pack()

        self.window.bind("<Return>", lambda event: self.login())

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password.")
            return

        user = self.manager.login(username, password)

        if user:
            self.window.withdraw()
            DashboardWindow(
                self.window,
                self.manager,
                user,
                self.show_login
            )
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def open_register(self):
        RegisterWindow(self.window, self.manager)

    def show_login(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.window.deiconify()

    def close(self):
        self.manager.close()
        self.window.destroy()

    def run(self):
        self.window.mainloop()
