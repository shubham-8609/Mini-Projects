import tkinter as tk
from tkinter import messagebox, simpledialog, ttk


class AdminDashboardWindow:

    BG      = "#EEF2F7"
    CARD_BG = "#FFFFFF"
    PRIMARY = "#1A56A4"
    DARK    = "#154291"

    def __init__(self, parent, manager, admin, on_logout):
        self.parent    = parent
        self.manager   = manager
        self.admin     = admin
        self.on_logout = on_logout

        self.window = tk.Toplevel(parent)
        self.window.title("Admin Dashboard")
        self.window.geometry("860x620")
        self.window.resizable(True, True)
        self.window.minsize(760, 540)
        self.window.configure(bg=self.BG)
        self.window.protocol("WM_DELETE_WINDOW", self.logout)

        self._build_ui()
        self.refresh_admin()

    # ─────────────────────────────────────────────────────
    def _build_ui(self):

        # ── Header bar ───────────────────────────────────
        header = tk.Frame(self.window, bg=self.PRIMARY, height=72)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🏦  BANK MANAGEMENT SYSTEM  —  ADMIN",
            bg=self.PRIMARY, fg="#FFFFFF",
            font=("Segoe UI", 18, "bold")
        ).place(relx=0.5, rely=0.5, anchor="center")

        # ── Admin info card ───────────────────────────────
        info_card = tk.Frame(
            self.window, bg=self.CARD_BG,
            highlightthickness=1, highlightbackground="#E5E7EB"
        )
        info_card.pack(fill="x", padx=30, pady=(22, 0))

        inner = tk.Frame(info_card, bg=self.CARD_BG, padx=28, pady=18)
        inner.pack(fill="x")

        tk.Label(inner, text="👤",
                 font=("Segoe UI Emoji", 24),
                 bg=self.CARD_BG).grid(row=0, column=0, rowspan=2, padx=(0, 16))

        tk.Label(inner, text="Administrator",
                 font=("Segoe UI", 10), fg="#9CA3AF",
                 bg=self.CARD_BG, anchor="w").grid(row=0, column=1, sticky="w")

        self.admin_name_label = tk.Label(
            inner, text="",
            font=("Segoe UI", 15, "bold"), fg="#111827",
            bg=self.CARD_BG, anchor="w"
        )
        self.admin_name_label.grid(row=1, column=1, sticky="w")

        self.admin_id_label = tk.Label(
            inner, text="",
            font=("Segoe UI", 10), fg="#6B7280",
            bg=self.CARD_BG, anchor="e"
        )
        self.admin_id_label.grid(row=0, column=2, rowspan=2, sticky="e", padx=(0, 4))
        inner.columnconfigure(2, weight=1)

        # ── Section label ─────────────────────────────────
        tk.Label(
            self.window, text="Admin Actions",
            font=("Segoe UI", 11, "bold"),
            fg="#374151", bg=self.BG, anchor="w"
        ).pack(fill="x", padx=30, pady=(22, 8))

        # ── Action buttons grid ───────────────────────────
        btn_card = tk.Frame(
            self.window, bg=self.CARD_BG,
            highlightthickness=1, highlightbackground="#E5E7EB",
            padx=24, pady=24
        )
        btn_card.pack(fill="x", padx=30)

        actions = [
            ("🔍  Search Customer",        self.search_customer,        0, 0),
            ("🗑️  Delete Customer",         self.delete_customer,        0, 1),
            ("👥  View All Customers",      self.view_all_customers,     1, 0),
            ("📊  View All Transactions",   self.view_all_transactions,  1, 1),
            ("💰  Total Bank Balance",      self.show_total_bank_balance, 2, 0),
            ("🚪  Logout",                  self.logout,                 2, 1),
        ]

        for text, cmd, row, col in actions:
            is_logout = "Logout" in text
            bg  = "#FEE2E2" if is_logout else self.PRIMARY
            fg  = "#991B1B" if is_logout else "#FFFFFF"
            abg = "#FECACA" if is_logout else self.DARK
            afg = "#7F1D1D" if is_logout else "#FFFFFF"

            tk.Button(
                btn_card,
                text=text,
                command=cmd,
                font=("Segoe UI", 10, "bold"),
                fg=fg, bg=bg,
                activebackground=abg, activeforeground=afg,
                relief="flat", bd=0, cursor="hand2",
                width=26, height=2
            ).grid(row=row, column=col, padx=10, pady=10)

        btn_card.columnconfigure(0, weight=1)
        btn_card.columnconfigure(1, weight=1)

        # ── Footer ───────────────────────────────────────
        tk.Label(
            self.window,
            text="© 2026 Shubham Bank  •  All rights reserved",
            font=("Segoe UI", 8), fg="#9CA3AF", bg=self.BG
        ).pack(side="bottom", pady=14)

    # ─────────────────────────────────────────────────────
    def refresh_admin(self):
        self.admin_name_label.config(text=self.admin["username"])
        self.admin_id_label.config(text=f"Admin ID : {self.admin['admin_id']}")

    # ─────────────────────────────────────────────────────
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
        messagebox.showinfo(
            "Total Bank Balance",
            f"Total balance held across all accounts:\n\n₹ {float(total_balance):,.2f}"
        )

    # ─────────────────────────────────────────────────────
    def _treeview_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Admin.Treeview",
            background="#FFFFFF", foreground="#111827",
            rowheight=28, fieldbackground="#FFFFFF",
            font=("Segoe UI", 10)
        )
        style.configure(
            "Admin.Treeview.Heading",
            background=self.PRIMARY, foreground="#FFFFFF",
            font=("Segoe UI", 10, "bold"), relief="flat"
        )
        style.map(
            "Admin.Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", self.PRIMARY)]
        )

    def _make_popup(self, title, width, height):
        win = tk.Toplevel(self.window)
        win.title(title)
        win.geometry(f"{width}x{height}")
        win.resizable(False, False)
        win.configure(bg=self.BG)
        win.grab_set()

        header = tk.Frame(win, bg=self.PRIMARY, height=52)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=title, bg=self.PRIMARY, fg="#FFFFFF",
                 font=("Segoe UI", 13, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        return win

    def show_users_window(self, title, users):
        self._treeview_style()
        win = self._make_popup(title, 700, 400)

        card = tk.Frame(win, bg=self.CARD_BG,
                        highlightthickness=1, highlightbackground="#E5E7EB")
        card.pack(fill="both", expand=True, padx=20, pady=16)

        columns = ("id", "username", "balance", "created_at")
        tree = ttk.Treeview(win, columns=columns, show="headings",
                            height=12, style="Admin.Treeview")

        tree.heading("id",         text="ID")
        tree.heading("username",   text="Username")
        tree.heading("balance",    text="Balance")
        tree.heading("created_at", text="Joined")

        tree.column("id",         width=60,  anchor="center")
        tree.column("username",   width=200, anchor="w")
        tree.column("balance",    width=140, anchor="e")
        tree.column("created_at", width=220, anchor="w")

        sb = ttk.Scrollbar(card, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=sb.set)

        tree.pack(in_=card, side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0), pady=8)
        sb.pack(in_=card, side=tk.RIGHT, fill=tk.Y, pady=8, padx=(0, 8))

        for user in users:
            tree.insert("", tk.END, values=(
                user["id"],
                user["username"],
                f"₹ {float(user['balance']):,.2f}",
                user["created_at"]
            ))

        tk.Label(win, text="© 2026 Shubham Bank  •  All rights reserved",
                 font=("Segoe UI", 8), fg="#9CA3AF", bg=self.BG
                 ).pack(pady=(0, 8))

    def show_transactions_window(self, title, transactions):
        self._treeview_style()
        win = self._make_popup(title, 920, 460)

        card = tk.Frame(win, bg=self.CARD_BG,
                        highlightthickness=1, highlightbackground="#E5E7EB")
        card.pack(fill="both", expand=True, padx=20, pady=16)

        columns = ("date", "type", "amount", "sender", "receiver")
        tree = ttk.Treeview(win, columns=columns, show="headings",
                            height=14, style="Admin.Treeview")

        tree.heading("date",     text="Date & Time")
        tree.heading("type",     text="Type")
        tree.heading("amount",   text="Amount")
        tree.heading("sender",   text="Sender")
        tree.heading("receiver", text="Receiver")

        tree.column("date",     width=180, anchor="w")
        tree.column("type",     width=130, anchor="center")
        tree.column("amount",   width=120, anchor="e")
        tree.column("sender",   width=220, anchor="w")
        tree.column("receiver", width=220, anchor="w")

        sb = ttk.Scrollbar(card, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=sb.set)

        tree.pack(in_=card, side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0), pady=8)
        sb.pack(in_=card, side=tk.RIGHT, fill=tk.Y, pady=8, padx=(0, 8))

        for t in transactions:
            tree.insert("", tk.END, values=(
                t["transaction_time"],
                t["transaction_type"].replace("_", " "),
                f"₹ {float(t['amount']):,.2f}",
                self.format_party(t["sender_id"],   t["sender_username"]),
                self.format_party(t["receiver_id"], t["receiver_username"])
            ))

        tk.Label(win, text="© 2026 Shubham Bank  •  All rights reserved",
                 font=("Segoe UI", 8), fg="#9CA3AF", bg=self.BG
                 ).pack(pady=(0, 8))

    # ─────────────────────────────────────────────────────
    def format_party(self, account_id, username):
        if account_id is None:
            return "-"
        if username is None:
            return f"Account #{account_id}"
        return f"{username}  (ID: {account_id})"

    # ─────────────────────────────────────────────────────
    def logout(self):
        self.window.destroy()
        self.on_logout()