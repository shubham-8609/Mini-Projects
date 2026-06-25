# manager.py

import random
from datetime import datetime
from User import User


class Manager:

    def __init__(self):
        self.users = {}     # {user_id : User}
        self.ids = set()

    # ---------------------------------
    # Register User
    # ---------------------------------
    def register(self, username, password, initial_balance):

        if username is None or password is None:
            return None

        if initial_balance < 0:
            return None

        # Check if username already exists
        for user in self.users.values():

            if user.get_username().lower() == username.lower():
                return None

        new_id = self.generate_unique_id()

        new_user = User(
            username,
            password,
            initial_balance,
            new_id
        )

        self.users[new_id] = new_user

        return new_user

    # ---------------------------------
    # Login
    # ---------------------------------
    def login(self, username, password):

        if username is None or password is None:
            return None

        for user in self.users.values():

            if (
                user.get_username().lower() == username.lower()
                and
                user.get_password() == password
            ):

                print("\n\t\tLogin Successful")

                return user

        return None

    # ---------------------------------
    # Check Username Exists
    # ---------------------------------
    def check_user_exists(self, username):

        for user in self.users.values():

            if user.get_username().lower() == username.lower():
                return True

        return False

    # ---------------------------------
    # Check User ID Exists
    # ---------------------------------
    def check_user_id_exists(self, user_id):

        return user_id in self.users

    # ---------------------------------
    # Generate Unique ID
    # ---------------------------------
    def generate_unique_id(self):

        while True:

            new_id = random.randint(0, 99999)

            if new_id not in self.ids:

                self.ids.add(new_id)

                return new_id

    # ---------------------------------
    # Transfer Money
    # ---------------------------------
    def transfer_money(self, sender_id, receiver_id, amount):

        sender = self.users.get(sender_id)
        receiver = self.users.get(receiver_id)

        if sender is None or receiver is None:
            return False

        if amount <= 0:
            return False

        if sender.get_balance() < amount:
            return False

        sender.withdraw(amount)
        receiver.deposit(amount)

        # Add better transaction history
        sender.add_transaction(
            amount,
            sender.get_balance(),
            datetime.now(),
            "transfer_sent"
        )

        receiver.add_transaction(
            amount,
            receiver.get_balance(),
            datetime.now(),
            "transfer_received"
        )

        return True

    # ---------------------------------
    # Get User using ID
    # ---------------------------------
    def get_user(self, user_id):

        return self.users.get(user_id)

    # ---------------------------------
    # Print all users (Optional)
    # ---------------------------------
    def print_users(self):

        for user in self.users.values():
            print(user)