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
        change_window.geometry("480x500")
        change_window.resizable(False, False)
        change_window.configure(bg="#EEF2F7")
        change_window.grab_set()

        # ── Center everything ────────────────────────────
        page = tk.Frame(change_window, bg="#EEF2F7")
        page.place(relx=0.5, rely=0.5, anchor="center")

        # ── Icon + heading ───────────────────────────────
        tk.Label(page, text="🔒",
                 font=("Segoe UI Emoji", 30),
                 bg="#EEF2F7").pack()

        tk.Label(page,
                 text="Change Password",
                 font=("Segoe UI", 15, "bold"),
                 fg="#111827", bg="#EEF2F7").pack(pady=(6, 2))

        tk.Label(page,
                 text="Keep your account safe with a strong password.",
                 font=("Segoe UI", 9),
                 fg="#9CA3AF", bg="#EEF2F7").pack(pady=(0, 18))

        # ── White card ───────────────────────────────────
        card = tk.Frame(page, bg="#FFFFFF",
                        highlightthickness=1,
                        highlightbackground="#E5E7EB",
                        padx=40, pady=32)
        card.pack()

        # Current Password
        tk.Label(card, text="Current Password",
                 font=("Segoe UI", 9), fg="#374151",
                 bg="#FFFFFF", anchor="w").pack(fill="x")
        current_password_entry = tk.Entry(card, show="*",
                                          font=("Segoe UI", 11),
                                          fg="#111827", bg="#F9FAFB",
                                          relief="flat", bd=0,
                                          highlightthickness=1,
                                          highlightbackground="#D1D5DB",
                                          highlightcolor="#1A56A4",
                                          width=30)
        current_password_entry.pack(fill="x", ipady=7, pady=(3, 14))

        # New Password
        tk.Label(card, text="New Password",
                 font=("Segoe UI", 9), fg="#374151",
                 bg="#FFFFFF", anchor="w").pack(fill="x")
        new_password_entry = tk.Entry(card, show="*",
                                      font=("Segoe UI", 11),
                                      fg="#111827", bg="#F9FAFB",
                                      relief="flat", bd=0,
                                      highlightthickness=1,
                                      highlightbackground="#D1D5DB",
                                      highlightcolor="#1A56A4",
                                      width=30)
        new_password_entry.pack(fill="x", ipady=7, pady=(3, 14))

        # Confirm Password
        tk.Label(card, text="Confirm Password",
                 font=("Segoe UI", 9), fg="#374151",
                 bg="#FFFFFF", anchor="w").pack(fill="x")
        confirm_password_entry = tk.Entry(card, show="*",
                                          font=("Segoe UI", 11),
                                          fg="#111827", bg="#F9FAFB",
                                          relief="flat", bd=0,
                                          highlightthickness=1,
                                          highlightbackground="#D1D5DB",
                                          highlightcolor="#1A56A4",
                                          width=30)
        confirm_password_entry.pack(fill="x", ipady=7, pady=(3, 28))

        def submit_change_password():

            current_password = current_password_entry.get()
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()

            if not current_password or not new_password or not confirm_password:
                messagebox.showerror("Error", "Please fill all fields.")
                return

            if new_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match.")
                return

            success = self.manager.change_password(
                self.user["id"],
                current_password,
                new_password
            )

            if success:
                messagebox.showinfo("Success", "Password changed successfully.")
                change_window.destroy()
            else:
                messagebox.showerror("Error", "Current password is incorrect.")

        # ── Change Password button (full width) ───────────
        tk.Button(card,
                  text="Change Password",
                  command=submit_change_password,
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

        change_window.bind("<Return>", lambda event: submit_change_password())
    # ====================================================

    def logout(self):

        self.window.destroy()

        self.on_logout()