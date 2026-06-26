import tkinter as tk
from decimal import Decimal, InvalidOperation
from tkinter import messagebox


class RegisterWindow:

    def __init__(self, parent, manager):
        self.parent = parent
        self.manager = manager
        self.window = tk.Toplevel(parent)
        self.window.title("Register Customer")
        self.window.geometry("480x600")
        self.window.resizable(False, False)
        self.window.configure(bg="#EEF2F7")
        self.window.grab_set()

        # ── Center everything ────────────────────────────
        page = tk.Frame(self.window, bg="#EEF2F7")
        page.place(relx=0.5, rely=0.5, anchor="center")

        # ── Icon + heading ───────────────────────────────
        tk.Label(page, text="🏦",
                 font=("Segoe UI Emoji", 30),
                 bg="#EEF2F7").pack()

        tk.Label(page,
                 text="Create Account",
                 font=("Segoe UI", 15, "bold"),
                 fg="#111827", bg="#EEF2F7").pack(pady=(6, 2))

        tk.Label(page,
                 text="Fill in your details to get started.",
                 font=("Segoe UI", 9),
                 fg="#9CA3AF", bg="#EEF2F7").pack(pady=(0, 18))

        # ── White card ───────────────────────────────────
        card = tk.Frame(page, bg="#FFFFFF",
                        highlightthickness=1,
                        highlightbackground="#E5E7EB",
                        padx=40, pady=32)
        card.pack()

        # Username
        tk.Label(card, text="Username",
                 font=("Segoe UI", 9), fg="#374151",
                 bg="#FFFFFF", anchor="w").pack(fill="x")
        self.username_entry = tk.Entry(card,
                                       font=("Segoe UI", 11),
                                       fg="#111827", bg="#F9FAFB",
                                       relief="flat", bd=0,
                                       highlightthickness=1,
                                       highlightbackground="#D1D5DB",
                                       highlightcolor="#1A56A4",
                                       width=30)
        self.username_entry.pack(fill="x", ipady=7, pady=(3, 14))

        # Password
        tk.Label(card, text="Password",
                 font=("Segoe UI", 9), fg="#374151",
                 bg="#FFFFFF", anchor="w").pack(fill="x")
        self.password_entry = tk.Entry(card, show="*",
                                       font=("Segoe UI", 11),
                                       fg="#111827", bg="#F9FAFB",
                                       relief="flat", bd=0,
                                       highlightthickness=1,
                                       highlightbackground="#D1D5DB",
                                       highlightcolor="#1A56A4",
                                       width=30)
        self.password_entry.pack(fill="x", ipady=7, pady=(3, 14))

        # Confirm Password
        tk.Label(card, text="Confirm Password",
                 font=("Segoe UI", 9), fg="#374151",
                 bg="#FFFFFF", anchor="w").pack(fill="x")
        self.confirm_password_entry = tk.Entry(card, show="*",
                                               font=("Segoe UI", 11),
                                               fg="#111827", bg="#F9FAFB",
                                               relief="flat", bd=0,
                                               highlightthickness=1,
                                               highlightbackground="#D1D5DB",
                                               highlightcolor="#1A56A4",
                                               width=30)
        self.confirm_password_entry.pack(fill="x", ipady=7, pady=(3, 14))

        # Initial Balance
        tk.Label(card, text="Initial Balance",
                 font=("Segoe UI", 9), fg="#374151",
                 bg="#FFFFFF", anchor="w").pack(fill="x")
        self.balance_entry = tk.Entry(card,
                                      font=("Segoe UI", 11),
                                      fg="#111827", bg="#F9FAFB",
                                      relief="flat", bd=0,
                                      highlightthickness=1,
                                      highlightbackground="#D1D5DB",
                                      highlightcolor="#1A56A4",
                                      width=30)
        self.balance_entry.insert(0, "0")
        self.balance_entry.pack(fill="x", ipady=7, pady=(3, 28))

        # ── Register button (full width) ─────────────────
        tk.Button(card,
                  text="Create Account",
                  command=self.register,
                  font=("Segoe UI", 10, "bold"),
                  fg="#FFFFFF", bg="#1A56A4",
                  activebackground="#154291",
                  activeforeground="#FFFFFF",
                  relief="flat", bd=0,
                  cursor="hand2",
                  height=2).pack(fill="x")

        # ── Footer ───────────────────────────────────────
        tk.Label(page,
                 text="© 2026 Shubham Bank  •  All rights reserved",
                 font=("Segoe UI", 8),
                 fg="#9CA3AF", bg="#EEF2F7").pack(pady=(16, 0))

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