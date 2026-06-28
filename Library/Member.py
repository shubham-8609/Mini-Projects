from datetime import datetime


class Member:

    def __init__(self, username, password):

        self.username            = username
        self.password            = password
        self.borrow_history      = []   # list of strings (log entries)
        self.currently_borrowed  = []   # list of book_ids

    # ---------------------------------
    # Getters
    # ---------------------------------

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_history(self):
        return self.borrow_history.copy()

    def get_currently_borrowed(self):
        return self.currently_borrowed.copy()

    # ---------------------------------
    # Borrow / Return Tracking
    # ---------------------------------

    def add_borrow(self, book):

        self.currently_borrowed.append(book.get_id())

        entry = (
            f"BORROWED | Book ID : {book.get_id()} | "
            f"'{book.get_title()}' by {book.get_author()} | "
            f"On : {datetime.now().strftime('%d-%m-%Y %H:%M')}"
        )

        self.borrow_history.append(entry)

    def add_return(self, book, fine):

        if book.get_id() in self.currently_borrowed:
            self.currently_borrowed.remove(book.get_id())

        fine_str = f"Fine : ₹{fine:.2f}" if fine > 0 else "No fine"

        entry = (
            f"RETURNED | Book ID : {book.get_id()} | "
            f"'{book.get_title()}' by {book.get_author()} | "
            f"On : {datetime.now().strftime('%d-%m-%Y %H:%M')} | {fine_str}"
        )

        self.borrow_history.append(entry)

    # ---------------------------------
    # Details
    # ---------------------------------

    def print_details(self):

        return (
            f"Username : {self.username}\n"
            f"Books Currently Borrowed : {len(self.currently_borrowed)}\n"
            f"Total Transactions : {len(self.borrow_history)}"
        )
