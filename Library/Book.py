from datetime import datetime


class Book:

    def __init__(self, book_id, title, author, genre):

        self.book_id   = book_id
        self.title     = title
        self.author    = author
        self.genre     = genre

        self.is_available    = True
        self.borrowed_by     = None   # member username
        self.borrow_date     = None   # datetime object

    # ---------------------------------
    # Getters
    # ---------------------------------

    def get_id(self):
        return self.book_id

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_genre(self):
        return self.genre

    def get_status(self):
        return self.is_available

    def get_borrowed_by(self):
        return self.borrowed_by

    def get_borrow_date(self):
        return self.borrow_date

    # ---------------------------------
    # Borrow / Return
    # ---------------------------------

    def mark_borrowed(self, username):

        self.is_available = False
        self.borrowed_by  = username
        self.borrow_date  = datetime.now()

    def mark_returned(self):

        self.is_available = True
        self.borrowed_by  = None
        self.borrow_date  = None

    # ---------------------------------
    # String
    # ---------------------------------

    def __str__(self):

        status = "Available" if self.is_available else f"Borrowed by {self.borrowed_by}"

        return (
            f"[{self.book_id}] {self.title} — {self.author} "
            f"| Genre : {self.genre} | Status : {status}"
        )
