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
        if not username or not password:
            return False

        if initial_balance < 0:
            return False

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
        if amount <= 0:
            return False

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
        if amount <= 0:
            return False

        try:
            user = self.get_user(user_id)

            if user is None:
                return False

            if user["balance"] < amount:
                return False

            self.db.begin_transaction()

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
        SELECT
            t.transaction_id,
            t.sender_id,
            sender.username  AS sender_username,
            t.receiver_id,
            receiver.username AS receiver_username,
            t.transaction_type,
            t.amount,
            t.transaction_time
        FROM transactions t
        LEFT JOIN users sender
            ON t.sender_id = sender.id
        LEFT JOIN users receiver
            ON t.receiver_id = receiver.id
        WHERE t.sender_id = %s
        OR  t.receiver_id = %s
        ORDER BY t.transaction_time DESC
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
            sender   = self.get_user(sender_id)
            receiver = self.get_user(receiver_id)

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

            self.db.begin_transaction()

            # Deduct from sender
            query = """
            UPDATE users
            SET balance = balance - %s
            WHERE id = %s
            """
            self.db.cursor.execute(query, (amount, sender_id))

            # Credit to receiver
            query = """
            UPDATE users
            SET balance = balance + %s
            WHERE id = %s
            """
            self.db.cursor.execute(query, (amount, receiver_id))

            insert_query = """
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

            # TRANSFER_OUT record  — sender's perspective
            # sender_id = who sent,  receiver_id = who received  ✓
            self.db.cursor.execute(
                insert_query,
                (
                    sender_id,
                    receiver_id,
                    "TRANSFER_OUT",
                    amount
                )
            )

            # TRANSFER_IN record  — receiver's perspective
            # FIX: sender_id = original sender,  receiver_id = original receiver
            # (was incorrectly swapped: receiver_id came first before this fix)
            self.db.cursor.execute(
                insert_query,
                (
                    sender_id,      # ← who originally sent the money
                    receiver_id,    # ← who received it  (was swapped before)
                    "TRANSFER_IN",
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
    # Change Password
    # ---------------------------------------

    def change_password(self, user_id, current_password, new_password):
        user = self.get_user(user_id)

        if user is None:
            return False

        if not current_password or not new_password:
            return False

        if user["password_hash"] != self.hash_password(current_password):
            return False

        query = """
        UPDATE users
        SET password_hash = %s
        WHERE id = %s
        """

        return self.db.execute(
            query,
            (
                self.hash_password(new_password),
                user_id
            )
        )

    # ---------------------------------------
    # Admin Login
    # ---------------------------------------

    def login_admin(self, username, password):
        hashed_password = self.hash_password(password)

        query = """
        SELECT admin_id, username
        FROM admins
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
    # Admin - Users
    # ---------------------------------------

    def get_all_users(self):
        query = """
        SELECT
            id,
            username,
            balance,
            created_at
        FROM users
        ORDER BY id DESC
        """

        return self.db.fetch_all(query)

    def search_users(self, keyword):
        query = """
        SELECT
            id,
            username,
            balance,
            created_at
        FROM users
        WHERE username LIKE %s
        OR CAST(id AS CHAR) LIKE %s
        ORDER BY id DESC
        """

        search_term = f"%{keyword}%"

        return self.db.fetch_all(
            query,
            (
                search_term,
                search_term
            )
        )

    def delete_user(self, user_id):
        try:
            self.db.begin_transaction()

            query = """
            DELETE FROM users
            WHERE id = %s
            """

            self.db.cursor.execute(query, (user_id,))

            if self.db.cursor.rowcount == 0:
                self.db.rollback()
                return False

            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            print(e)
            return False

    # ---------------------------------------
    # Admin - Transactions and Reports
    # ---------------------------------------

    def get_all_transactions(self):
        query = """
        SELECT
            t.transaction_id,
            t.sender_id,
            sender.username  AS sender_username,
            t.receiver_id,
            receiver.username AS receiver_username,
            t.transaction_type,
            t.amount,
            t.transaction_time
        FROM transactions t
        LEFT JOIN users sender
            ON t.sender_id = sender.id
        LEFT JOIN users receiver
            ON t.receiver_id = receiver.id
        ORDER BY t.transaction_time DESC
        """

        return self.db.fetch_all(query)

    def get_total_bank_balance(self):
        query = """
        SELECT COALESCE(SUM(balance), 0) AS total_balance
        FROM users
        """

        result = self.db.fetch_one(query)

        if result is None:
            return 0

        return result["total_balance"]

    # ---------------------------------------
    # Close Database
    # ---------------------------------------

    def close(self):
        self.db.close()