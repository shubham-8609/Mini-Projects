import tkinter as tk
from tkinter import messagebox, simpledialog, ttk


class AdminDashboardWindow:

    def __init__(self, parent, manager, admin, on_logout):
        self.parent = parent
        self.manager = manager
        self.admin = admin
        self.on_logout = on_logout

        self.window = tk.Toplevel(parent)
        self.window.title("Admin Dashboard")
        self.window.geometry("680x420")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.logout)

        tk.Label(
            self.window,
            text="Admin Dashboard",
            font=("Arial", 18, "bold")
        ).pack(pady=(22, 10))

        self.info_label = tk.Label(self.window, font=("Arial", 11))
        self.info_label.pack(pady=(0, 22))

        button_frame = tk.Frame(self.window)
        button_frame.pack()

        buttons = [
            ("Search Customer", self.search_customer),
            ("Delete Customer", self.delete_customer),
            ("View All Customers", self.view_all_customers),
            ("View All Transactions", self.view_all_transactions),
            ("Total Bank Balance", self.show_total_bank_balance),
            ("Logout", self.logout),
        ]

        for index, (text, command) in enumerate(buttons):
            row = index // 2
            column = index % 2
            tk.Button(
                button_frame,
                text=text,
                width=24,
                command=command
            ).grid(row=row, column=column, padx=10, pady=8)

        self.refresh_admin()

    def refresh_admin(self):
        self.info_label.config(
            text=f"Username: {self.admin['username']}    Admin ID: {self.admin['admin_id']}"
        )

    def search_customer(self):
        keyword = simpledialog.askstring(
            "Search Customer",
            "Enter customer username or account ID:",
            parent=self.window
        )

        if not keyword:
            return

        users = self.manager.search_users(keyword.strip())

        if not users:
            messagebox.showinfo("Search Result", "No matching customers found.")
            return

        self.show_users_window(f"Search Results for '{keyword.strip()}'", users)

    def delete_customer(self):
        user_id = simpledialog.askinteger(
            "Delete Customer",
            "Enter customer account ID:",
            parent=self.window,
            minvalue=1
        )

        if user_id is None:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete customer account {user_id}? This action cannot be undone."
        )

        if not confirm:
            return

        if self.manager.delete_user(user_id):
            messagebox.showinfo("Success", "Customer deleted successfully.")
        else:
            messagebox.showerror("Error", "Customer could not be deleted.")

    def view_all_customers(self):
        users = self.manager.get_all_users()

        if not users:
            messagebox.showinfo("Customers", "No customers found.")
            return

        self.show_users_window("All Customers", users)

    def view_all_transactions(self):
        transactions = self.manager.get_all_transactions()

        if not transactions:
            messagebox.showinfo("Transactions", "No transactions found.")
            return

        self.show_transactions_window("All Transactions", transactions)

    def show_total_bank_balance(self):
        total_balance = self.manager.get_total_bank_balance()
        messagebox.showinfo("Total Bank Balance", f"Total bank balance: Rs. {total_balance}")

    def show_users_window(self, title, users):
        window = tk.Toplevel(self.window)
        window.title(title)
        window.geometry("640x360")
        window.resizable(False, False)

        columns = ("id", "username", "balance", "created_at")

        tree = ttk.Treeview(window, columns=columns, show="headings", height=12)
        tree.heading("id", text="ID")
        tree.heading("username", text="Username")
        tree.heading("balance", text="Balance")
        tree.heading("created_at", text="Created At")

        tree.column("id", width=80)
        tree.column("username", width=200)
        tree.column("balance", width=120)
        tree.column("created_at", width=200)

        scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(12, 0), pady=12)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=12, padx=(0, 12))

        for user in users:
            tree.insert(
                "",
                tk.END,
                values=(
                    user["id"],
                    user["username"],
                    f"Rs. {user['balance']}",
                    user["created_at"]
                )
            )

    def show_transactions_window(self, title, transactions):
        window = tk.Toplevel(self.window)
        window.title(title)
        window.geometry("860x380")
        window.resizable(False, False)

        columns = ("date", "type", "amount", "sender", "receiver")

        tree = ttk.Treeview(window, columns=columns, show="headings", height=12)
        tree.heading("date", text="Date")
        tree.heading("type", text="Type")
        tree.heading("amount", text="Amount")
        tree.heading("sender", text="Sender")
        tree.heading("receiver", text="Receiver")

        tree.column("date", width=180)
        tree.column("type", width=140)
        tree.column("amount", width=110)
        tree.column("sender", width=210)
        tree.column("receiver", width=210)

        scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(12, 0), pady=12)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=12, padx=(0, 12))

        for transaction in transactions:
            tree.insert(
                "",
                tk.END,
                values=(
                    transaction["transaction_time"],
                    transaction["transaction_type"],
                    f"Rs. {transaction['amount']}",
                    self.format_party(
                        transaction["sender_id"],
                        transaction["sender_username"]
                    ),
                    self.format_party(
                        transaction["receiver_id"],
                        transaction["receiver_username"]
                    )
                )
            )

    def format_party(self, account_id, username):
        if account_id is None:
            return "-"

        if username is None:
            return f"Account {account_id}"

        return f"{username} ({account_id})"

    def logout(self):
        self.window.destroy()
        self.on_logout()
