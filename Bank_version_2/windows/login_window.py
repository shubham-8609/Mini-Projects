import tkinter as tk
from tkinter import messagebox

from manager import Manager
from windows.admin_login_window import AdminLoginWindow
from windows.dashboard import DashboardWindow
from windows.register_window import RegisterWindow


class LoginWindow:

    def __init__(self):
        self.manager = Manager()
        self.window = tk.Tk()
        self.window.title("Bank Management System Pro")
        self.window.geometry("480x540")
        self.window.resizable(False, False)
        self.window.configure(bg="#EEF2F7")
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        # ── Page background ──────────────────────────────
        page = tk.Frame(self.window, bg="#EEF2F7")
        page.place(relx=0.5, rely=0.5, anchor="center")

        # ── Icon + heading ───────────────────────────────
        tk.Label(page, text="🏦",
                 font=("Segoe UI Emoji", 34),
                 bg="#EEF2F7").pack()

        tk.Label(page,
                 text="Bank Management System Pro",
                 font=("Segoe UI", 15, "bold"),
                 fg="#111827", bg="#EEF2F7").pack(pady=(6, 2))

        tk.Label(page,
                 text="Welcome back! Sign in to continue.",
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
                 font=("Segoe UI", 9),
                 fg="#374151", bg="#FFFFFF",
                 anchor="w").pack(fill="x")

        self.username_entry = tk.Entry(card,
                                       font=("Segoe UI", 11),
                                       fg="#111827", bg="#F9FAFB",
                                       relief="flat", bd=0,
                                       highlightthickness=1,
                                       highlightbackground="#D1D5DB",
                                       highlightcolor="#1A56A4",
                                       width=30)
        self.username_entry.pack(fill="x", ipady=7, pady=(3, 16))

        # Password
        tk.Label(card, text="Password",
                 font=("Segoe UI", 9),
                 fg="#374151", bg="#FFFFFF",
                 anchor="w").pack(fill="x")

        self.password_entry = tk.Entry(card, show="*",
                                       font=("Segoe UI", 11),
                                       fg="#111827", bg="#F9FAFB",
                                       relief="flat", bd=0,
                                       highlightthickness=1,
                                       highlightbackground="#D1D5DB",
                                       highlightcolor="#1A56A4",
                                       width=30)
        self.password_entry.pack(fill="x", ipady=7, pady=(3, 28))

        # ── Login + Register row ─────────────────────────
        btn_row = tk.Frame(card, bg="#FFFFFF")
        btn_row.pack()

        tk.Button(btn_row,
                  text="Login",
                  command=self.login,
                  font=("Segoe UI", 10, "bold"),
                  fg="#FFFFFF", bg="#1A56A4",
                  activebackground="#154291",
                  activeforeground="#FFFFFF",
                  relief="flat", bd=0,
                  cursor="hand2",
                  width=13, height=2).grid(row=0, column=0, padx=(0, 8))

        tk.Button(btn_row,
                  text="Register",
                  command=self.open_register,
                  font=("Segoe UI", 10, "bold"),
                  fg="#1A56A4", bg="#FFFFFF",
                  activebackground="#EEF2F7",
                  activeforeground="#1A56A4",
                  relief="solid", bd=1,
                  highlightbackground="#1A56A4",
                  cursor="hand2",
                  width=13, height=2).grid(row=0, column=1)

        # ── Admin Login (subtle link) ────────────────────
        admin_lbl = tk.Label(card,
                             text="Admin Login",
                             font=("Segoe UI", 9, "underline"),
                             fg="#6B7280", bg="#FFFFFF",
                             cursor="hand2")
        admin_lbl.pack(pady=(18, 0))
        admin_lbl.bind("<Button-1>", lambda _: self.open_admin_login())
        admin_lbl.bind("<Enter>",    lambda _: admin_lbl.config(fg="#1A56A4"))
        admin_lbl.bind("<Leave>",    lambda _: admin_lbl.config(fg="#6B7280"))

        # ── Footer ───────────────────────────────────────
        tk.Label(page,
                 text="© 2026 Shubham Bank  •  All rights reserved",
                 font=("Segoe UI", 8),
                 fg="#9CA3AF", bg="#EEF2F7").pack(pady=(16, 0))

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

    def open_admin_login(self):
        AdminLoginWindow(self.window, self.manager)

    def show_login(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.window.deiconify()

    def close(self):
        self.manager.close()
        self.window.destroy()

    def run(self):
        self.window.mainloop()