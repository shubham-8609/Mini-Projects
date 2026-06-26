import tkinter as tk
from decimal import Decimal, InvalidOperation
from tkinter import messagebox


class WithdrawWindow:

    def __init__(self, parent, manager, user_id, on_success):
        self.manager = manager
        self.user_id = user_id
        self.on_success = on_success

        self.window = tk.Toplevel(parent)
        self.window.title("Withdraw Money")
        self.window.geometry("480x380")
        self.window.resizable(False, False)
        self.window.configure(bg="#EEF2F7")
        self.window.grab_set()

        # ── Center everything ────────────────────────────
        page = tk.Frame(self.window, bg="#EEF2F7")
        page.place(relx=0.5, rely=0.5, anchor="center")

        # ── Icon + heading ───────────────────────────────
        tk.Label(page, text="🏧",
                 font=("Segoe UI Emoji", 30),
                 bg="#EEF2F7").pack()

        tk.Label(page,
                 text="Withdraw Money",
                 font=("Segoe UI", 15, "bold"),
                 fg="#111827", bg="#EEF2F7").pack(pady=(6, 2))

        tk.Label(page,
                 text="Enter the amount you wish to withdraw.",
                 font=("Segoe UI", 9),
                 fg="#9CA3AF", bg="#EEF2F7").pack(pady=(0, 18))

        # ── White card ───────────────────────────────────
        card = tk.Frame(page, bg="#FFFFFF",
                        highlightthickness=1,
                        highlightbackground="#E5E7EB",
                        padx=40, pady=32)
        card.pack()

        # Amount
        tk.Label(card, text="Amount",
                 font=("Segoe UI", 9), fg="#374151",
                 bg="#FFFFFF", anchor="w").pack(fill="x")
        self.amount_entry = tk.Entry(card,
                                     font=("Segoe UI", 11),
                                     fg="#111827", bg="#F9FAFB",
                                     relief="flat", bd=0,
                                     highlightthickness=1,
                                     highlightbackground="#D1D5DB",
                                     highlightcolor="#1A56A4",
                                     width=30)
        self.amount_entry.pack(fill="x", ipady=7, pady=(3, 28))
        self.amount_entry.focus()

        # ── Withdraw button (full width) ──────────────────
        tk.Button(card,
                  text="Withdraw",
                  command=self.withdraw,
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

        self.window.bind("<Return>", lambda event: self.withdraw())

    def withdraw(self):
        amount = self.get_amount()

        if amount is None:
            return

        if self.manager.withdraw(self.user_id, amount):
            messagebox.showinfo("Success", "Amount withdrawn successfully.")
            self.on_success()
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Withdraw failed. Check your balance.")

    def get_amount(self):
        try:
            amount = Decimal(self.amount_entry.get())
        except InvalidOperation:
            messagebox.showerror("Error", "Amount must be a number.")
            return None

        if amount <= 0:
            messagebox.showerror("Error", "Amount must be greater than zero.")
            return None

        return amount