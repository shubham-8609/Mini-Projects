# user.py

from datetime import datetime


class User:
    def __init__(self, username, password, balance, user_id):
        self.username = username
        self.password = password
        self.id = user_id
        self.balance = balance
        self.transaction_history = []

    # -----------------------------
    # Getters
    # -----------------------------
    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_id(self):
        return self.id

    def get_balance(self):
        return self.balance

    def get_transaction_history(self):
        return self.transaction_history.copy()

    # -----------------------------
    # Setters
    # -----------------------------
    def set_password(self, password):
        self.password = password

    # -----------------------------
    # Deposit
    # -----------------------------
    def deposit(self, amount):

        if amount <= 0:
            return False

        if amount > 50000:
            return False

        self.balance += amount

        self.add_transaction(
            amount,
            self.balance,
            datetime.now(),
            "deposit"
        )

        return True

    # -----------------------------
    # Withdraw
    # -----------------------------
    def withdraw(self, amount):

        if amount <= 0:
            return False

        if amount > self.balance:
            return False

        self.balance -= amount

        self.add_transaction(
            amount,
            self.balance,
            datetime.now(),
            "withdraw"
        )

        return True

    # -----------------------------
    # Print Details
    # -----------------------------
    def print_details(self):

        details = ""

        details += f"\nID : {self.id}"
        details += f"\nUsername : {self.username}"
        details += f"\nPassword : {self.password}"
        details += f"\nCurrent Balance : {self.balance:.2f}"

        return details

    # -----------------------------
    # Transaction History
    # -----------------------------
    def add_transaction(self, amount, balance, time, transaction_type):

        if transaction_type == "deposit":

            data = (
                f"Deposited : {amount:.2f}\n"
                f"At : {time}\n"
                f"Balance : {balance:.2f}\n"
            )

        elif transaction_type == "withdraw":

            data = (
                f"Withdrawn : {amount:.2f}\n"
                f"At : {time}\n"
                f"Balance : {balance:.2f}\n"
            )

        elif transaction_type == "transfer_sent":

            data = (
                f"Transferred : {amount:.2f}\n"
                f"At : {time}\n"
                f"Balance : {balance:.2f}\n"
            )

        elif transaction_type == "transfer_received":

            data = (
                f"Received : {amount:.2f}\n"
                f"At : {time}\n"
                f"Balance : {balance:.2f}\n"
            )

        else:

            data = (
                f"Transaction : {amount:.2f}\n"
                f"At : {time}\n"
                f"Balance : {balance:.2f}\n"
            )

        self.transaction_history.append(data)

    # -----------------------------
    # String Representation
    # -----------------------------
    def __str__(self):

        history = ""

        for transaction in self.transaction_history:
            history += transaction + "\n"

        return (
            f"Username : {self.username}\n"
            f"Balance : {self.balance:.2f}\n\n"
            f"Transaction History\n"
            f"{history}"
        )