import pickle
import time
from concurrent.futures import ThreadPoolExecutor

from Manager import Manager

# ---------------------------------------
# Global Variables
# ---------------------------------------

current_user_id = None

executor = ThreadPoolExecutor(max_workers=2)

DATA_FILE = "bankdata.pkl"


# ---------------------------------------
# Save Data
# ---------------------------------------

def save_data(manager):

    try:

        with open(DATA_FILE, "wb") as file:

            pickle.dump(manager, file)

    except Exception as e:

        print(f"\nFailed to save data : {e}")


# ---------------------------------------
# Load Data
# ---------------------------------------

def load_data():

    try:

        with open(DATA_FILE, "rb") as file:

            manager = pickle.load(file)

            # Restore IDs
            manager.ids = set(manager.users.keys())

            return manager

    except FileNotFoundError:

        return Manager()

    except Exception as e:

        print(f"\nError : {e}")

        return Manager()


# ---------------------------------------
# Async Save
# ---------------------------------------

def async_save(manager):

    executor.submit(save_data, manager)


# ---------------------------------------
# Integer Input
# ---------------------------------------

def get_int_input(prompt, minimum, maximum):

    while True:

        try:

            value = int(input(prompt))

            if minimum <= value <= maximum:

                return value

            print(
                f"Please enter a number between {minimum} and {maximum}"
            )

        except ValueError:

            print("Invalid Input.")


# ---------------------------------------
# Welcome Screen
# ---------------------------------------

def print_welcome():

    print("\n" * 3)

    print("=" * 65)

    print("           Welcome to Shubham's Bank Organization")

    print("=" * 65)

    print()

    print("[1] Register")

    print("[2] Login")


# ---------------------------------------
# User Information
# ---------------------------------------

def print_user_info(user):

    print("\nWelcome,", user.get_username())

    print(f"Balance : {user.get_balance():.2f}")

    print(f"Account ID : {user.get_id()}")


# ---------------------------------------
# Register User
# ---------------------------------------

def register_user(manager):

    global current_user_id

    username = input("\nEnter Username : ")

    while True:

        password = input("Enter Password : ")

        confirm = input("Confirm Password : ")

        if password == confirm:

            break

        print("\nPasswords did not match.\n")

    initial_balance = get_int_input(
        "Enter Initial Balance : ",
        0,
        999999999
    )

    print("\nRegistering user...")

    time.sleep(1)

    user = manager.register(
        username,
        password,
        initial_balance
    )

    if user is None:

        print("\nRegistration Failed.")

        return

    print("\nRegistration Successful!")

    current_user_id = user.get_id()

    print_user_info(user)

    user_controller(user, manager)


# ---------------------------------------
# Login User
# ---------------------------------------

def login_user(manager):

    global current_user_id

    trials = 0

    username = ""

    while trials < 3:

        temp = input("\nEnter Username : ")

        if manager.check_user_exists(temp):

            username = temp

            break

        print("Username does not exist.")

        trials += 1

    if username == "":

        return

    password = input("Enter Password : ")

    print("\nLogging in...")

    time.sleep(1)

    user = manager.login(
        username,
        password
    )

    if user is None:

        print("\nWrong username or password.")

        return

    print("\nLogin Successful!")

    current_user_id = user.get_id()

    print_user_info(user)

    user_controller(user, manager)


# ---------------------------------------
# User Menu
# ---------------------------------------

def print_user_menu():

    print("\n")

    print("[1] Check Balance")

    print("[2] Deposit")

    print("[3] Withdraw")

    print("[4] Show Transactions")

    print("[5] Account Details")

    print("[6] Transfer Money")

    print("[7] Exit")

    # ---------------------------------------
# Transfer Money
# ---------------------------------------

def transfer_money_feature(manager):

    global current_user_id

    receiver_id = get_int_input(
        "\nEnter Receiver's ID : ",
        0,
        99999
    )

    if not manager.check_user_id_exists(receiver_id):

        print("\nNo user found with the given ID.")

        return

    amount = get_int_input(
        "Enter Amount : ",
        1,
        999999999
    )

    success = manager.transfer_money(
        current_user_id,
        receiver_id,
        amount
    )

    if success:

        print("\nMoney transferred successfully.")

        async_save(manager)

    else:

        print("\nTransfer failed.")


# ---------------------------------------
# User Controller
# ---------------------------------------

def user_controller(user, manager):

    running = True

    while running:

        print_user_menu()

        choice = get_int_input(
            "\nEnter your choice : ",
            1,
            7
        )

        # -------------------------
        # Check Balance
        # -------------------------

        if choice == 1:

            print(
                f"\nCurrent Balance : {user.get_balance():.2f}"
            )

        # -------------------------
        # Deposit
        # -------------------------

        elif choice == 2:

            amount = get_int_input(
                "\nEnter Amount : ",
                1,
                999999999
            )

            if user.deposit(amount):

                print(
                    f"\n₹{amount} deposited successfully."
                )

                async_save(manager)

            else:

                print("\nDeposit Failed.")

        # -------------------------
        # Withdraw
        # -------------------------

        elif choice == 3:

            amount = get_int_input(
                "\nEnter Amount : ",
                1,
                999999999
            )

            if user.withdraw(amount):

                print(
                    f"\n₹{amount} withdrawn successfully."
                )

                async_save(manager)

            else:

                print("\nInsufficient Balance.")

        # -------------------------
        # Transactions
        # -------------------------

        elif choice == 4:

            history = user.get_transaction_history()

            if not history:

                print("\nNo Transactions Yet.")

            else:

                print("\nTransaction History\n")

                for transaction in history:

                    print(transaction)

        # -------------------------
        # Account Details
        # -------------------------

        elif choice == 5:

            print(user.print_details())

        # -------------------------
        # Transfer
        # -------------------------

        elif choice == 6:

            transfer_money_feature(manager)

        # -------------------------
        # Exit
        # -------------------------

        elif choice == 7:

            async_save(manager)

            print("\nSaving Data...")

            executor.shutdown(wait=True)

            print("Goodbye!")

            running = False


# ---------------------------------------
# Main Function
# ---------------------------------------

def main():

    manager = load_data()

    print_welcome()

    choice = get_int_input(
        "\nEnter Choice : ",
        1,
        2
    )

    if choice == 1:

        register_user(manager)

    else:

        login_user(manager)


# ---------------------------------------
# Program Starts Here
# ---------------------------------------

if __name__ == "__main__":

    main()