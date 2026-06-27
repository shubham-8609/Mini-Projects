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
        self.window.geometry("480x420")
        self.window.resizable(False, False)
        self.window.configure(bg="#EEF2F7")
        self.window.grab_set()

        # ── Center everything ────────────────────────────
        page = tk.Frame(self.window, bg="#EEF2F7")
        page.place(relx=0.5, rely=0.5, anchor="center")

        # ── Icon + heading ───────────────────────────────
        tk.Label(page, text="💸",
                 font=("Segoe UI Emoji", 30),
                 bg="#EEF2F7").pack()

        tk.Label(page,
                 text="Transfer Money",
                 font=("Segoe UI", 15, "bold"),
                 fg="#111827", bg="#EEF2F7").pack(pady=(6, 2))

        tk.Label(page,
                 text="Send funds to another account instantly.",
                 font=("Segoe UI", 9),
                 fg="#9CA3AF", bg="#EEF2F7").pack(pady=(0, 18))

        # ── White card ───────────────────────────────────
        card = tk.Frame(page, bg="#FFFFFF",
                        highlightthickness=1,
                        highlightbackground="#E5E7EB",
                        padx=40, pady=32)
        card.pack()

        # Receiver Account ID
        tk.Label(card, text="Receiver Account ID",
                 font=("Segoe UI", 9), fg="#374151",
                 bg="#FFFFFF", anchor="w").pack(fill="x")
        self.receiver_entry = tk.Entry(card,
                                       font=("Segoe UI", 11),
                                       fg="#111827", bg="#F9FAFB",
                                       relief="flat", bd=0,
                                       highlightthickness=1,
                                       highlightbackground="#D1D5DB",
                                       highlightcolor="#1A56A4",
                                       width=30)
        self.receiver_entry.pack(fill="x", ipady=7, pady=(3, 14))
        self.receiver_entry.focus()

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

        # ── Transfer button (full width) ──────────────────
        tk.Button(card,
                  text="Transfer",
                  command=self.transfer,
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