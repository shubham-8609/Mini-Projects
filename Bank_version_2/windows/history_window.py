import tkinter as tk
from tkinter import ttk


class HistoryWindow:

    def __init__(self, parent, manager, user_id):
        self.manager = manager
        self.user_id = user_id

        self.window = tk.Toplevel(parent)
        self.window.title("Transaction History")
        self.window.geometry("860x520")
        self.window.resizable(False, False)
        self.window.configure(bg="#EEF2F7")
        self.window.grab_set()

        # ── Header ───────────────────────────────────────
        header = tk.Frame(self.window, bg="#1A56A4", height=64)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="📜  Transaction History",
            bg="#1A56A4", fg="#FFFFFF",
            font=("Segoe UI", 16, "bold")
        ).place(relx=0.5, rely=0.5, anchor="center")

        # ── Table card ───────────────────────────────────
        card = tk.Frame(
            self.window, bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#E5E7EB"
        )
        card.pack(fill="both", expand=True, padx=24, pady=20)

        # ── Treeview style ───────────────────────────────
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Bank.Treeview",
            background="#FFFFFF",
            foreground="#111827",
            rowheight=30,
            fieldbackground="#FFFFFF",
            font=("Segoe UI", 10)
        )
        style.configure(
            "Bank.Treeview.Heading",
            background="#1A56A4",
            foreground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )
        style.map(
            "Bank.Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", "#1A56A4")]
        )

        columns = ("date", "type", "direction", "amount", "counterparty")

        self.tree = ttk.Treeview(
            card,
            columns=columns,
            show="headings",
            height=16,
            style="Bank.Treeview"
        )

        self.tree.heading("date",         text="Date & Time")
        self.tree.heading("type",         text="Type")
        self.tree.heading("direction",    text="Direction")
        self.tree.heading("amount",       text="Amount")
        self.tree.heading("counterparty", text="Counterparty")

        self.tree.column("date",         width=180, anchor="w")
        self.tree.column("type",         width=130, anchor="center")
        self.tree.column("direction",    width=90,  anchor="center")
        self.tree.column("amount",       width=120, anchor="e")
        self.tree.column("counterparty", width=290, anchor="w")

        scrollbar = ttk.Scrollbar(card, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0), pady=8)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=8, padx=(0, 8))

        # ── Row tag colours ──────────────────────────────
        self.tree.tag_configure("in",      foreground="#166534")   # green  — money received
        self.tree.tag_configure("out",     foreground="#991B1B")   # red    — money sent
        self.tree.tag_configure("neutral", foreground="#374151")   # grey   — deposit / withdraw

        # ── Footer ───────────────────────────────────────
        tk.Label(
            self.window,
            text="© 2026 Shubham Bank  •  All rights reserved",
            font=("Segoe UI", 8),
            fg="#9CA3AF", bg="#EEF2F7"
        ).pack(pady=(0, 10))

        self.load_transactions()

    # ─────────────────────────────────────────────────────
    def load_transactions(self):
        transactions = self.manager.get_transactions(self.user_id)

        for t in transactions:
            tx_type    = t["transaction_type"]
            amount     = t["amount"]
            time_str   = t["transaction_time"]

            # ── Determine direction & counterparty ───────
            if tx_type == "DEPOSIT":
                direction    = "IN ↓"
                tag          = "in"
                amount_str   = f"+ ₹ {float(amount):,.2f}"
                counterparty = "Bank (Deposit)"

            elif tx_type == "WITHDRAW":
                direction    = "OUT ↑"
                tag          = "out"
                amount_str   = f"- ₹ {float(amount):,.2f}"
                counterparty = "Bank (Withdrawal)"

            elif tx_type == "TRANSFER_OUT":
                # This user sent money → receiver is the counterparty
                direction    = "OUT ↑"
                tag          = "out"
                amount_str   = f"- ₹ {float(amount):,.2f}"
                counterparty = self.format_party(
                    t["receiver_id"], t["receiver_username"]
                )

            elif tx_type == "TRANSFER_IN":
                # This user received money → sender is the counterparty
                direction    = "IN ↓"
                tag          = "in"
                amount_str   = f"+ ₹ {float(amount):,.2f}"
                counterparty = self.format_party(
                    t["sender_id"], t["sender_username"]
                )

            else:
                direction    = "-"
                tag          = "neutral"
                amount_str   = f"₹ {float(amount):,.2f}"
                counterparty = "-"

            self.tree.insert(
                "", tk.END,
                values=(
                    time_str,
                    tx_type.replace("_", " "),
                    direction,
                    amount_str,
                    counterparty
                ),
                tags=(tag,)
            )

    # ─────────────────────────────────────────────────────
    def format_party(self, account_id, username):
        if account_id is None:
            return "-"
        if username is None:
            return f"Account #{account_id}"
        return f"{username}  (ID: {account_id})"