from datetime import datetime
from Book import Book
from Member import Member


BORROW_DAYS  = 7
FINE_PER_DAY = 5   # ₹5 per extra day


class Library:

    def __init__(self):

        self.books   = {}   # {book_id : Book}
        self.members = {}   # {username : Member}
        self.next_id = 1

    # =================================
    # Book Management
    # =================================

    def add_book(self, title, author, genre):

        book = Book(self.next_id, title, author, genre)
        self.books[self.next_id] = book
        self.next_id += 1

        return book

    def remove_book(self, book_id):

        book = self.books.get(book_id)

        if book is None:
            return False, "Book not found."

        if not book.get_status():
            return False, "Book is currently borrowed and cannot be removed."

        del self.books[book_id]

        return True, "Book removed successfully."

    # =================================
    # Member Management
    # =================================

    def register(self, username, password):

        if not username or not password:
            return None, "Username and password cannot be empty."

        if username.lower() in [u.lower() for u in self.members]:
            return None, "Username already exists."

        member = Member(username, password)
        self.members[username] = member

        return member, "Registration successful."

    def login(self, username, password):

        member = self.members.get(username)

        if member is None:
            return None, "Username not found."

        if member.get_password() != password:
            return None, "Wrong password."

        return member, "Login successful."

    def check_member_exists(self, username):

        return username in self.members

    # =================================
    # Borrow & Return
    # =================================

    def borrow_book(self, member, book_id):

        book = self.books.get(book_id)

        if book is None:
            return False, "Book not found."

        if not book.get_status():
            return False, f"'{book.get_title()}' is currently not available."

        if book_id in member.get_currently_borrowed():
            return False, "You have already borrowed this book."

        book.mark_borrowed(member.get_username())
        member.add_borrow(book)

        return True, f"'{book.get_title()}' borrowed successfully. Return by {BORROW_DAYS} days."

    def return_book(self, member, book_id):

        book = self.books.get(book_id)

        if book is None:
            return False, 0, "Book not found."

        if book_id not in member.get_currently_borrowed():
            return False, 0, "You have not borrowed this book."

        # Calculate fine
        borrow_date = book.get_borrow_date()
        days_held   = (datetime.now() - borrow_date).days
        extra_days  = max(0, days_held - BORROW_DAYS)
        fine        = extra_days * FINE_PER_DAY

        book.mark_returned()
        member.add_return(book, fine)

        msg = f"'{book.get_title()}' returned."

        if fine > 0:
            msg += f" Late by {extra_days} day(s). Fine : ₹{fine:.2f}"

        return True, fine, msg

    # =================================
    # Search
    # =================================

    def search_by_title(self, query):

        query = query.lower()

        return [
            book for book in self.books.values()
            if query in book.get_title().lower()
        ]

    def search_by_author(self, query):

        query = query.lower()

        return [
            book for book in self.books.values()
            if query in book.get_author().lower()
        ]

    # =================================
    # View Books
    # =================================

    def get_all_books(self):
        return list(self.books.values())

    def get_available_books(self):
        return [b for b in self.books.values() if b.get_status()]

    def get_borrowed_books(self):
        return [b for b in self.books.values() if not b.get_status()]
