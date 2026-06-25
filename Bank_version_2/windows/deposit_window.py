import tkinter as tk
from decimal import Decimal, InvalidOperation
from tkinter import messagebox


class DepositWindow:

    def __init__(self, parent, manager, user_id, on_success):
        self.manager = manager
        self.user_id = user_id
        self.on_success = on_success

        self.window = tk.Toplevel(parent)
        self.window.title("Deposit Money")
        self.window.geometry("360x220")
        self.window.resizable(False, False)
        self.window.grab_set()

        tk.Label(
            self.window,
            text="Deposit Money",
            font=("Arial", 15, "bold")
        ).pack(pady=(24, 16))

        tk.Label(self.window, text="Amount").pack()
        self.amount_entry = tk.Entry(self.window, width=28)
        self.amount_entry.pack(pady=(4, 16))
        self.amount_entry.focus()

        tk.Button(
            self.window,
            text="Deposit",
            width=18,
            command=self.deposit
        ).pack()

        self.window.bind("<Return>", lambda event: self.deposit())

    def deposit(self):
        amount = self.get_amount()

        if amount is None:
            return

        if self.manager.deposit(self.user_id, amount):
            messagebox.showinfo("Success", "Amount deposited successfully.")
            self.on_success()
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Deposit failed.")

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
