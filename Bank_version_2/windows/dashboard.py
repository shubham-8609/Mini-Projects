import tkinter as tk
from tkinter import messagebox

from windows.deposit_window import DepositWindow
from windows.history_window import HistoryWindow
from windows.transfer_window import TransferWindow
from windows.withdraw_window import WithdrawWindow


class DashboardWindow:

    def __init__(self, parent, manager, user, on_logout):
        self.parent = parent
        self.manager = manager
        self.user = user
        self.on_logout = on_logout

        self.window = tk.Toplevel(parent)
        self.window.title("Customer Dashboard")
        self.window.geometry("560x440")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.logout)

        tk.Label(
            self.window,
            text="Customer Dashboard",
            font=("Arial", 18, "bold")
        ).pack(pady=(24, 12))

        self.account_label = tk.Label(self.window, font=("Arial", 11))
        self.account_label.pack()

        self.balance_label = tk.Label(
            self.window,
            font=("Arial", 16, "bold")
        )
        self.balance_label.pack(pady=(8, 24))

        button_frame = tk.Frame(self.window)
        button_frame.pack()

        buttons = [
            ("Deposit", self.open_deposit),
            ("Withdraw", self.open_withdraw),
            ("Transfer", self.open_transfer),
            ("Transaction History", self.open_history),
            ("Change Password", self.change_password),
            ("Logout", self.logout),
        ]

        for index, (text, command) in enumerate(buttons):
            row = index // 2
            column = index % 2
            tk.Button(
                button_frame,
                text=text,
                width=22,
                command=command
            ).grid(row=row, column=column, padx=10, pady=8)

        self.refresh_user()

    def refresh_user(self):
        latest_user = self.manager.get_user(self.user["id"])

        if latest_user is None:
            messagebox.showerror("Error", "Account could not be loaded.")
            self.logout()
            return

        self.user = latest_user
        self.account_label.config(
            text=f"Username: {self.user['username']}    Account ID: {self.user['id']}"
        )
        self.balance_label.config(
            text=f"Balance: Rs. {self.user['balance']}"
        )

    def open_deposit(self):
        DepositWindow(self.window, self.manager, self.user["id"], self.refresh_user)

    def open_withdraw(self):
        WithdrawWindow(self.window, self.manager, self.user["id"], self.refresh_user)

    def open_transfer(self):
        TransferWindow(self.window, self.manager, self.user["id"], self.refresh_user)

    def open_history(self):
        HistoryWindow(self.window, self.manager, self.user["id"])

    def change_password(self):
        change_window = tk.Toplevel(self.window)
        change_window.title("Change Password")
        change_window.geometry("420x320")
        change_window.resizable(False, False)
        change_window.grab_set()

        tk.Label(
            change_window,
            text="Change Password",
            font=("Arial", 16, "bold")
        ).pack(pady=(24, 18))

        tk.Label(change_window, text="Current Password").pack()
        current_password_entry = tk.Entry(change_window, show="*", width=30)
        current_password_entry.pack(pady=(4, 12))
        current_password_entry.focus()

        tk.Label(change_window, text="New Password").pack()
        new_password_entry = tk.Entry(change_window, show="*", width=30)
        new_password_entry.pack(pady=(4, 12))

        tk.Label(change_window, text="Confirm New Password").pack()
        confirm_password_entry = tk.Entry(change_window, show="*", width=30)
        confirm_password_entry.pack(pady=(4, 18))

        def submit_change_password():
            current_password = current_password_entry.get()
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()

            if not current_password or not new_password or not confirm_password:
                messagebox.showerror("Error", "All password fields are required.")
                return

            stored_user = self.manager.get_user(self.user["id"])

            if stored_user is None:
                messagebox.showerror("Error", "Account could not be loaded.")
                change_window.destroy()
                return

            if stored_user["password_hash"] != self.manager.hash_password(current_password):
                messagebox.showerror("Error", "The current password entered is incorrect.")
                return

            if new_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match.")
                return

            if self.manager.change_password(
                self.user["id"],
                current_password,
                new_password
            ):
                messagebox.showinfo("Success", "Password changed successfully.")
                change_window.destroy()
            else:
                messagebox.showerror("Error", "Password could not be changed.")

        tk.Button(
            change_window,
            text="Change Password",
            width=20,
            command=submit_change_password
        ).pack()

        change_window.bind("<Return>", lambda event: submit_change_password())

    def logout(self):
        self.window.destroy()
        self.on_logout()
