import tkinter as tk
from decimal import Decimal, InvalidOperation
from tkinter import messagebox


class TransferWindow:

    def __init__(self, parent, manager, user_id, on_success):
        self.manager = manager
        self.user_id = user_id
        self.on_success = on_success

        self.window = tk.Toplevel(parent)
        self.window.title("Transfer Money")
        self.window.geometry("380x280")
        self.window.resizable(False, False)
        self.window.grab_set()

        tk.Label(
            self.window,
            text="Transfer Money",
            font=("Arial", 15, "bold")
        ).pack(pady=(24, 16))

        tk.Label(self.window, text="Receiver Account ID").pack()
        self.receiver_entry = tk.Entry(self.window, width=28)
        self.receiver_entry.pack(pady=(4, 12))
        self.receiver_entry.focus()

        tk.Label(self.window, text="Amount").pack()
        self.amount_entry = tk.Entry(self.window, width=28)
        self.amount_entry.pack(pady=(4, 18))

        tk.Button(
            self.window,
            text="Transfer",
            width=18,
            command=self.transfer
        ).pack()

        self.window.bind("<Return>", lambda event: self.transfer())

    def transfer(self):
        receiver_id = self.get_receiver_id()
        amount = self.get_amount()

        if receiver_id is None or amount is None:
            return

        if self.manager.transfer(self.user_id, receiver_id, amount):
            messagebox.showinfo("Success", "Transfer completed successfully.")
            self.on_success()
            self.window.destroy()
        else:
            messagebox.showerror(
                "Error",
                "Transfer failed. Check receiver ID, balance, and amount."
            )

    def get_receiver_id(self):
        try:
            receiver_id = int(self.receiver_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Receiver account ID must be a number.")
            return None

        if receiver_id <= 0:
            messagebox.showerror("Error", "Receiver account ID is invalid.")
            return None

        return receiver_id

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
