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
        self.window.geometry("360x220")
        self.window.resizable(False, False)
        self.window.grab_set()

        tk.Label(
            self.window,
            text="Withdraw Money",
            font=("Arial", 15, "bold")
        ).pack(pady=(24, 16))

        tk.Label(self.window, text="Amount").pack()
        self.amount_entry = tk.Entry(self.window, width=28)
        self.amount_entry.pack(pady=(4, 16))
        self.amount_entry.focus()

        tk.Button(
            self.window,
            text="Withdraw",
            width=18,
            command=self.withdraw
        ).pack()

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
