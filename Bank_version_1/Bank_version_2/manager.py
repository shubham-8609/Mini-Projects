import hashlib
from database import Database


class Manager:

    def __init__(self):
        self.db = Database()

    # ---------------------------------------
    # Password Hashing
    # ---------------------------------------

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # ---------------------------------------
    # Register User
    # ---------------------------------------

    def register(self, username, password, initial_balance):
        # Check if username already exists
        query = """
        SELECT id
        FROM users
        WHERE username = %s
        """

        result = self.db.fetch_one(query, (username,))

        if result is not None:
            return False

        hashed_password = self.hash_password(password)

        query = """
        INSERT INTO users
        (
            username,
            password_hash,
            balance
        )
        VALUES
        (
            %s,
            %s,
            %s
        )
        """

        return self.db.execute(
            query,
            (
                username,
                hashed_password,
                initial_balance
            )
        )

    # ---------------------------------------
    # Login
    # ---------------------------------------

    def login(self, username, password):
        hashed_password = self.hash_password(password)

        query = """
        SELECT *
        FROM users
        WHERE username = %s
        AND password_hash = %s
        """

        return self.db.fetch_one(
            query,
            (
                username,
                hashed_password
            )
        )

    # ---------------------------------------
    # Deposit
    # ---------------------------------------

    def deposit(self, user_id, amount):
        try:
            self.db.begin_transaction()

            query = """
            UPDATE users
            SET balance = balance + %s
            WHERE id = %s
            """

            self.db.cursor.execute(
                query,
                (
                    amount,
                    user_id
                )
            )

            query = """
            INSERT INTO transactions
            (
                sender_id,
                receiver_id,
                transaction_type,
                amount
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
            """

            self.db.cursor.execute(
                query,
                (
                    user_id,
                    None,
                    "DEPOSIT",
                    amount
                )
            )

            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    # ---------------------------------------
    # Withdraw
    # ---------------------------------------

    def withdraw(self, user_id, amount):
        try:
            user = self.get_user(user_id)

            if user is None:
                return False

            if user["balance"] < amount:
                return False

            self.db.begin_transaction()

            # Update balance
            query = """
            UPDATE users
            SET balance = balance - %s
            WHERE id = %s
            """

            self.db.cursor.execute(
                query,
                (
                    amount,
                    user_id
                )
            )

            # Insert transaction
            query = """
            INSERT INTO transactions
            (
                sender_id,
                receiver_id,
                transaction_type,
                amount
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
            """

            self.db.cursor.execute(
                query,
                (
                    user_id,
                    None,
                    "WITHDRAW",
                    amount
                )
            )

            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    # ---------------------------------------
    # Get User
    # ---------------------------------------

    def get_user(self, user_id):
        query = """
        SELECT *
        FROM users
        WHERE id = %s
        """

        return self.db.fetch_one(
            query,
            (
                user_id,
            )
        )

    # ---------------------------------------
    # Check Username
    # ---------------------------------------

    def username_exists(self, username):
        query = """
        SELECT id
        FROM users
        WHERE username = %s
        """

        return self.db.fetch_one(
            query,
            (
                username,
            )
        ) is not None

    

    # ---------------------------------------
    # Transaction History
    # ---------------------------------------

    def get_transactions(self, user_id):
        query = """
        SELECT *
        FROM transactions
        WHERE sender_id = %s
        OR receiver_id = %s
        ORDER BY transaction_time DESC
        """

        return self.db.fetch_all(
            query,
            (
                user_id,
                user_id
            )
        )

    # ---------------------------------------
    # Transfer Funds
    # ---------------------------------------

    def transfer(self, sender_id, receiver_id, amount):
        try:
            sender = self.get_user(sender_id)
            receiver = self.get_user(receiver_id)

            # -------------------------
            # Validation
            # -------------------------

            if sender is None:
                return False

            if receiver is None:
                return False

            if sender_id == receiver_id:
                return False

            if amount <= 0:
                return False

            if sender["balance"] < amount:
                return False

            # -------------------------
            # Start Transaction
            # -------------------------

            self.db.begin_transaction()

            # -------------------------
            # Withdraw from sender
            # -------------------------

            query = """
            UPDATE users
            SET balance = balance - %s
            WHERE id = %s
            """

            self.db.cursor.execute(
                query,
                (
                    amount,
                    sender_id
                )
            )

            # -------------------------
            # Deposit to receiver
            # -------------------------

            query = """
            UPDATE users
            SET balance = balance + %s
            WHERE id = %s
            """

            self.db.cursor.execute(
                query,
                (
                    amount,
                    receiver_id
                )
            )

            # -------------------------
            # Sender Transaction
            # -------------------------

            query = """
            INSERT INTO transactions
            (
                sender_id,
                receiver_id,
                transaction_type,
                amount
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
            """

            self.db.cursor.execute(
                query,
                (
                    sender_id,
                    receiver_id,
                    "TRANSFER_OUT",
                    amount
                )
            )

            # -------------------------
            # Receiver Transaction
            # -------------------------

            self.db.cursor.execute(
                query,
                (
                    receiver_id,
                    sender_id,
                    "TRANSFER_IN",
                    amount
                )
            )

            # -------------------------
            # Commit
            # -------------------------

            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    # ---------------------------------------
    # Close Database
    # ---------------------------------------

    def close(self):
        self.db.close()