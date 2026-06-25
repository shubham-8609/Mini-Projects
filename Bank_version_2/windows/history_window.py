import tkinter as tk
from tkinter import ttk


class HistoryWindow:

    def __init__(self, parent, manager, user_id):
        self.manager = manager
        self.user_id = user_id

        self.window = tk.Toplevel(parent)
        self.window.title("Transaction History")
        self.window.geometry("820x420")
        self.window.resizable(False, False)

        tk.Label(
            self.window,
            text="Transaction History",
            font=("Arial", 15, "bold")
        ).pack(pady=(18, 12))

        columns = (
            "date",
            "type",
            "amount",
            "sender",
            "receiver"
        )

        self.tree = ttk.Treeview(
            self.window,
            columns=columns,
            show="headings",
            height=14
        )

        self.tree.heading("date", text="Date")
        self.tree.heading("type", text="Type")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("sender", text="Sender")
        self.tree.heading("receiver", text="Receiver")

        self.tree.column("date", width=170)
        self.tree.column("type", width=130)
        self.tree.column("amount", width=110)
        self.tree.column("sender", width=180)
        self.tree.column("receiver", width=180)

        scrollbar = ttk.Scrollbar(
            self.window,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        table_frame = tk.Frame(self.window)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=18, pady=(0, 18))

        self.tree.pack(in_=table_frame, side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(in_=table_frame, side=tk.RIGHT, fill=tk.Y)

        self.load_transactions()

    def load_transactions(self):
        transactions = self.manager.get_transactions(self.user_id)

        for transaction in transactions:
            self.tree.insert(
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
