"""
CSV-based persistence for the Library Management System.

Files created:
  books.csv    — all book records
  members.csv  — all member records (username, password, history, borrowed)
"""

import csv
import os
from datetime import datetime

from Book import Book
from Member import Member


BOOKS_FILE   = "books.csv"
MEMBERS_FILE = "members.csv"

DATE_FMT = "%Y-%m-%d %H:%M:%S"


# =================================
# Save
# =================================

def save_data(library):

    _save_books(library)
    _save_members(library)


def _save_books(library):

    with open(BOOKS_FILE, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            "book_id", "title", "author", "genre",
            "is_available", "borrowed_by", "borrow_date", "next_id"
        ])

        for book in library.books.values():

            borrow_date_str = (
                book.get_borrow_date().strftime(DATE_FMT)
                if book.get_borrow_date()
                else ""
            )

            writer.writerow([
                book.get_id(),
                book.get_title(),
                book.get_author(),
                book.get_genre(),
                book.get_status(),
                book.get_borrowed_by() or "",
                borrow_date_str,
                library.next_id
            ])


def _save_members(library):

    with open(MEMBERS_FILE, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            "username", "password",
            "currently_borrowed",   # semicolon-separated book IDs
            "history"               # pipe-separated log entries
        ])

        for member in library.members.values():

            borrowed_str = ";".join(
                str(bid) for bid in member.get_currently_borrowed()
            )

            history_str = "|".join(member.get_history())

            writer.writerow([
                member.get_username(),
                member.get_password(),
                borrowed_str,
                history_str
            ])


# =================================
# Load
# =================================

def load_data(library):

    _load_books(library)
    _load_members(library)


def _load_books(library):

    if not os.path.exists(BOOKS_FILE):
        return

    with open(BOOKS_FILE, newline="", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:

            book_id = int(row["book_id"])

            book = Book(
                book_id,
                row["title"],
                row["author"],
                row["genre"]
            )

            book.is_available = row["is_available"] == "True"

            book.borrowed_by = row["borrowed_by"] or None

            if row["borrow_date"]:
                book.borrow_date = datetime.strptime(
                    row["borrow_date"], DATE_FMT
                )

            library.books[book_id] = book
            library.next_id = int(row["next_id"])


def _load_members(library):

    if not os.path.exists(MEMBERS_FILE):
        return

    with open(MEMBERS_FILE, newline="", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:

            member = Member(row["username"], row["password"])

            if row["currently_borrowed"]:
                member.currently_borrowed = [
                    int(bid)
                    for bid in row["currently_borrowed"].split(";")
                    if bid
                ]

            if row["history"]:
                member.borrow_history = row["history"].split("|")

            library.members[row["username"]] = member
