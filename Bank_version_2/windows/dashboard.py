import tkinter as tk
from tkinter import messagebox

from windows.deposit_window import DepositWindow
from windows.history_window import HistoryWindow
from windows.transfer_window import TransferWindow
from windows.withdraw_window import WithdrawWindow


class DashboardWindow:

    PRIMARY_COLOR = "#1565C0"
    BACKGROUND = "#F4F6F9"
    CARD_BG = "white"

    def __init__(self, parent, manager, user, on_logout):

        self.parent = parent
        self.manager = manager
        self.user = user
        self.on_logout = on_logout

        self.window = tk.Toplevel(parent)
        self.window.title("Bank Management System")
        self.window.geometry("850x650")
        self.window.minsize(760, 560)
        self.window.resizable(True, True)
        self.window.configure(bg=self.BACKGROUND)
        self.window.protocol("WM_DELETE_WINDOW", self.logout)

        # ====================================================
        # HEADER
        # ====================================================

        header = tk.Frame(
            self.window,
            bg=self.PRIMARY_COLOR,
            height=80
        )

        header.pack(fill="x")

        tk.Label(
            header,
            text="🏦  BANK MANAGEMENT SYSTEM",
            bg=self.PRIMARY_COLOR,
            fg="white",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=22)

        # ====================================================
        # ACCOUNT CARD
        # ====================================================

        card = tk.Frame(
            self.window,
            bg=self.CARD_BG,
            bd=2,
            relief="groove"
        )

        card.pack(
            fill="x",
            padx=35,
            pady=30
        )

        tk.Label(
            card,
            text="Welcome Back!",
            bg=self.CARD_BG,
            fg="#555555",
            font=("Segoe UI", 14)
        ).pack(pady=(20, 5))

        self.username_label = tk.Label(
            card,
            bg=self.CARD_BG,
            fg="black",
            font=("Segoe UI", 18, "bold")
        )

        self.username_label.pack()

        self.account_label = tk.Label(
            card,
            bg=self.CARD_BG,
            fg="gray",
            font=("Segoe UI", 11)
        )

        self.account_label.pack(pady=(8, 18))

        tk.Label(
            card,
            text="Current Balance",
            bg=self.CARD_BG,
            fg="gray",
            font=("Segoe UI", 12)
        ).pack()

        self.balance_label = tk.Label(
            card,
            bg=self.CARD_BG,
            fg=self.PRIMARY_COLOR,
            font=("Segoe UI", 26, "bold")
        )

        self.balance_label.pack(pady=(6, 22))

        # ====================================================
        # BUTTONS
        # ====================================================

        button_frame = tk.Frame(
            self.window,
            bg=self.BACKGROUND
        )

        button_frame.pack(pady=10)

        self.create_button(
            button_frame,
            "💰 Deposit",
            self.open_deposit,
            0,
            0
        )

        self.create_button(
            button_frame,
            "💸 Withdraw",
            self.open_withdraw,
            0,
            1
        )

        self.create_button(
            button_frame,
            "🔁 Transfer",
            self.open_transfer,
            1,
            0
        )

        self.create_button(
            button_frame,
            "📜 History",
            self.open_history,
            1,
            1
        )

        self.create_button(
            button_frame,
            "🔒 Change Password",
            self.change_password,
            2,
            0
        )

        self.create_button(
            button_frame,
            "🚪 Logout",
            self.logout,
            2,
            1
        )

        # ====================================================
        # FOOTER
        # ====================================================

        footer = tk.Label(
            self.window,
            text="© 2026 Shubham Bank",
            bg=self.BACKGROUND,
            fg="gray",
            font=("Segoe UI", 10)
        )

        footer.pack(side="bottom", pady=18)

        self.refresh_user()

    # ====================================================

    def create_button(self, parent, text, command, row, column):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            width=20,
            height=2,
            bg=self.PRIMARY_COLOR,
            fg="white",
            activebackground="#0D47A1",
            activeforeground="white",
            cursor="hand2",
            relief="flat",
            font=("Segoe UI", 11, "bold")
        )

        button.grid(
            row=row,
            column=column,
            padx=15,
            pady=15
        )

    # ====================================================

    def refresh_user(self):

        latest_user = self.manager.get_user(self.user["id"])

        if latest_user is None:
            messagebox.showerror(
                "Error",
                "Account could not be loaded."
            )
            self.logout()
            return

        self.user = latest_user

        self.username_label.config(
            text=self.user["username"]
        )

        self.account_label.config(
            text=f"Account ID : {self.user['id']}"
        )

        self.balance_label.config(
            text=f"₹ {float(self.user['balance']):,.2f}"
        )

    # ====================================================

    def open_deposit(self):

        DepositWindow(
            self.window,
            self.manager,
            self.user["id"],
            self.refresh_user
        )

    def open_withdraw(self):

        WithdrawWindow(
            self.window,
            self.manager,
            self.user["id"],
            self.refresh_user
        )

    def open_transfer(self):

        TransferWindow(
            self.window,
            self.manager,
            self.user["id"],
            self.refresh_user
        )

    def open_history(self):

        HistoryWindow(
            self.window,
            self.manager,
            self.user["id"]
        )

    # ====================================================

    def change_password(self):

        change_window = tk.Toplevel(self.window)

        change_window.title("Change Password")

        change_window.geometry("430x340")

        change_window.resizable(False, False)

        change_window.configure(bg=self.BACKGROUND)

        change_window.grab_set()

        tk.Label(
            change_window,
            text="🔒 Change Password",
            bg=self.BACKGROUND,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=20)

        tk.Label(
            change_window,
            text="Current Password",
            bg=self.BACKGROUND
        ).pack()

        current_password_entry = tk.Entry(
            change_window,
            show="*",
            width=32
        )

        current_password_entry.pack(pady=6)

        tk.Label(
            change_window,
            text="New Password",
            bg=self.BACKGROUND
        ).pack()

        new_password_entry = tk.Entry(
            change_window,
            show="*",
            width=32
        )

        new_password_entry.pack(pady=6)

        tk.Label(
            change_window,
            text="Confirm Password",
            bg=self.BACKGROUND
        ).pack()

        confirm_password_entry = tk.Entry(
            change_window,
            show="*",
            width=32
        )

        confirm_password_entry.pack(pady=6)

        def submit_change_password():

            current_password = current_password_entry.get()

            new_password = new_password_entry.get()

            confirm_password = confirm_password_entry.get()

            if not current_password or not new_password or not confirm_password:

                messagebox.showerror(
                    "Error",
                    "Please fill all fields."
                )

                return

            if new_password != confirm_password:

                messagebox.showerror(
                    "Error",
                    "Passwords do not match."
                )

                return

            success = self.manager.change_password(
                self.user["id"],
                current_password,
                new_password
            )

            if success:

                messagebox.showinfo(
                    "Success",
                    "Password changed successfully."
                )

                change_window.destroy()

            else:

                messagebox.showerror(
                    "Error",
                    "Current password is incorrect."
                )

        tk.Button(
            change_window,
            text="Change Password",
            command=submit_change_password,
            bg=self.PRIMARY_COLOR,
            fg="white",
            width=20,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        ).pack(pady=20)

        change_window.bind(
            "<Return>",
            lambda event: submit_change_password()
        )

    # ====================================================

    def logout(self):

        self.window.destroy()

        self.on_logout()