import time

from Library import Library
from storage import save_data, load_data


# ---------------------------------------
# Admin Credentials
# ---------------------------------------

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ---------------------------------------
# Integer Input Helper
# ---------------------------------------

def get_int_input(prompt, minimum, maximum):

    while True:

        try:

            value = int(input(prompt))

            if minimum <= value <= maximum:
                return value

            print(f"Please enter a number between {minimum} and {maximum}.")

        except ValueError:

            print("Invalid input. Please enter a number.")


# ---------------------------------------
# Welcome Screen
# ---------------------------------------

def print_welcome():

    print("\n" * 2)
    print("=" * 60)
    print("        Welcome to Shubham's Library Management System")
    print("=" * 60)
    print()
    print("[1] Register as Member")
    print("[2] Member Login")
    print("[3] Admin Login")
    print("[4] Exit")


# ---------------------------------------
# Display Books List
# ---------------------------------------

def display_books(books):

    if not books:
        print("\n  No books to display.")
        return

    print()
    for book in books:
        print(f"  {book}")


# =======================================
# Admin Panel
# =======================================

def admin_menu():

    print("\n")
    print("[1] Add Book")
    print("[2] Remove Book")
    print("[3] View All Books")
    print("[4] Logout")


def admin_controller(library):

    print("\nAdmin login successful.")

    running = True

    while running:

        admin_menu()

        choice = get_int_input("\nEnter choice : ", 1, 4)

        # ---------------------
        # Add Book
        # ---------------------

        if choice == 1:

            title  = input("\nEnter Book Title  : ").strip()
            author = input("Enter Author Name : ").strip()
            genre  = input("Enter Genre       : ").strip()

            if not title or not author or not genre:
                print("All fields are required.")
                continue

            book = library.add_book(title, author, genre)
            save_data(library)

            print(f"\nBook added successfully! Assigned ID : {book.get_id()}")

        # ---------------------
        # Remove Book
        # ---------------------

        elif choice == 2:

            display_books(library.get_all_books())

            book_id = get_int_input("\nEnter Book ID to remove : ", 1, 999999)

            success, msg = library.remove_book(book_id)

            if success:
                save_data(library)

            print(f"\n{msg}")

        # ---------------------
        # View All Books
        # ---------------------

        elif choice == 3:

            print("\n--- Available Books ---")
            display_books(library.get_available_books())

            print("\n--- Borrowed Books ---")
            display_books(library.get_borrowed_books())

        # ---------------------
        # Logout
        # ---------------------

        elif choice == 4:

            print("\nAdmin logged out.")
            running = False


# =======================================
# Member Panel
# =======================================

def member_menu():

    print("\n")
    print("[1] View All Books")
    print("[2] Search Books")
    print("[3] Borrow a Book")
    print("[4] Return a Book")
    print("[5] My Borrow History")
    print("[6] My Account Details")
    print("[7] Logout")


def view_books_menu(library):

    print("\n")
    print("[1] All Books")
    print("[2] Available Only")
    print("[3] Borrowed Only")

    choice = get_int_input("\nEnter choice : ", 1, 3)

    if choice == 1:
        display_books(library.get_all_books())

    elif choice == 2:
        display_books(library.get_available_books())

    elif choice == 3:
        display_books(library.get_borrowed_books())


def search_menu(library):

    print("\n")
    print("[1] Search by Title")
    print("[2] Search by Author")

    choice = get_int_input("\nEnter choice : ", 1, 2)

    query = input("Enter search query : ").strip()

    if not query:
        print("Search query cannot be empty.")
        return

    if choice == 1:
        results = library.search_by_title(query)
    else:
        results = library.search_by_author(query)

    print(f"\n{len(results)} result(s) found :")
    display_books(results)


def member_controller(member, library):

    print(f"\nWelcome, {member.get_username()}!")

    running = True

    while running:

        member_menu()

        choice = get_int_input("\nEnter choice : ", 1, 7)

        # ---------------------
        # View Books
        # ---------------------

        if choice == 1:

            view_books_menu(library)

        # ---------------------
        # Search
        # ---------------------

        elif choice == 2:

            search_menu(library)

        # ---------------------
        # Borrow
        # ---------------------

        elif choice == 3:

            display_books(library.get_available_books())

            if not library.get_available_books():
                continue

            book_id = get_int_input("\nEnter Book ID to borrow : ", 1, 999999)

            success, msg = library.borrow_book(member, book_id)

            if success:
                save_data(library)

            print(f"\n{msg}")

        # ---------------------
        # Return
        # ---------------------

        elif choice == 4:

            borrowed_ids = member.get_currently_borrowed()

            if not borrowed_ids:
                print("\nYou have no books to return.")
                continue

            print("\nYour currently borrowed books :")

            for bid in borrowed_ids:
                book = library.books.get(bid)
                if book:
                    print(f"  {book}")

            book_id = get_int_input("\nEnter Book ID to return : ", 1, 999999)

            success, fine, msg = library.return_book(member, book_id)

            if success:
                save_data(library)

            print(f"\n{msg}")

        # ---------------------
        # History
        # ---------------------

        elif choice == 5:

            history = member.get_history()

            if not history:
                print("\nNo transaction history yet.")

            else:

                print(f"\nTransaction History for {member.get_username()} :\n")

                for i, entry in enumerate(history, 1):
                    print(f"  {i}. {entry}")

        # ---------------------
        # Account Details
        # ---------------------

        elif choice == 6:

            print(f"\n{member.print_details()}")

        # ---------------------
        # Logout
        # ---------------------

        elif choice == 7:

            print(f"\nGoodbye, {member.get_username()}!")
            running = False


# =======================================
# Register
# =======================================

def register_member(library):

    print()

    username = input("Enter Username : ").strip()

    while True:

        password = input("Enter Password : ").strip()
        confirm  = input("Confirm Password : ").strip()

        if password == confirm:
            break

        print("\nPasswords did not match. Try again.\n")

    print("\nRegistering...")
    time.sleep(1)

    member, msg = library.register(username, password)

    print(f"\n{msg}")

    if member:
        save_data(library)
        member_controller(member, library)


# =======================================
# Login
# =======================================

def login_member(library):

    print()

    trials  = 0
    username = ""

    while trials < 3:

        temp = input("Enter Username : ").strip()

        if library.check_member_exists(temp):
            username = temp
            break

        print("Username does not exist.")
        trials += 1

    if not username:
        print("\nToo many failed attempts.")
        return

    password = input("Enter Password : ").strip()

    print("\nLogging in...")
    time.sleep(1)

    member, msg = library.login(username, password)

    print(f"\n{msg}")

    if member:
        member_controller(member, library)


def login_admin(library):

    print()

    username = input("Admin Username : ").strip()
    password = input("Admin Password : ").strip()

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        admin_controller(library)

    else:
        print("\nInvalid admin credentials.")


# =======================================
# Main
# =======================================

def main():

    library = Library()
    load_data(library)

    running = True

    while running:

        print_welcome()

        choice = get_int_input("\nEnter choice : ", 1, 4)

        if choice == 1:
            register_member(library)

        elif choice == 2:
            login_member(library)

        elif choice == 3:
            login_admin(library)

        elif choice == 4:
            print("\nThank you for using Shubham's Library System. Goodbye!\n")
            running = False


# =======================================
# Entry Point
# =======================================

if __name__ == "__main__":
    main()
