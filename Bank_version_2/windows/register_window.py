import tkinter as tk
from decimal import Decimal, InvalidOperation
from tkinter import messagebox


class RegisterWindow:

    def __init__(self, parent, manager):
        self.parent = parent
        self.manager = manager
        self.window = tk.Toplevel(parent)
        self.window.title("Register Customer")
        self.window.geometry("420x420")
        self.window.resizable(False, False)
        self.window.grab_set()

        tk.Label(
            self.window,
            text="Create Account",
            font=("Arial", 16, "bold")
        ).pack(pady=(24, 18))

        tk.Label(self.window, text="Username").pack()
        self.username_entry = tk.Entry(self.window, width=30)
        self.username_entry.pack(pady=(4, 12))

        tk.Label(self.window, text="Password").pack()
        self.password_entry = tk.Entry(self.window, show="*", width=30)
        self.password_entry.pack(pady=(4, 12))

        tk.Label(self.window, text="Confirm Password").pack()
        self.confirm_password_entry = tk.Entry(self.window, show="*", width=30)
        self.confirm_password_entry.pack(pady=(4, 12))

        tk.Label(self.window, text="Initial Balance").pack()
        self.balance_entry = tk.Entry(self.window, width=30)
        self.balance_entry.insert(0, "0")
        self.balance_entry.pack(pady=(4, 18))

        tk.Button(
            self.window,
            text="Register",
            width=20,
            command=self.register
        ).pack()

        self.window.bind("<Return>", lambda event: self.register())

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        try:
            initial_balance = Decimal(self.balance_entry.get())
        except InvalidOperation:
            messagebox.showerror("Error", "Initial balance must be a number.")
            return

        if initial_balance < 0:
            messagebox.showerror("Error", "Initial balance cannot be negative.")
            return

        if self.manager.username_exists(username):
            messagebox.showerror("Error", "Username already exists.")
            return

        if self.manager.register(username, password, initial_balance):
            messagebox.showinfo("Success", "Account created successfully.")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Account could not be created.")
