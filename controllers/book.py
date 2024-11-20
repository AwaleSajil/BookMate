import sqlite3
from base.base import BaseModel
from models.database import DBManager

class Book(BaseModel):
    def __init__(self, title, author, isbn, owner_id):
        self.book_id = None
        self.title = title
        self.author = author
        self.isbn = isbn
        self.owner_id = owner_id

    def save(self):
        if DBManager.execute_query(
                "INSERT INTO books (title, author, isbn, owner_id) VALUES (?, ?, ?, ?)",
                (self.title, self.author, self.isbn, self.owner_id),
        ):
            return True
        else:
            return False
    @staticmethod
    def delete(book_id, owner_id):
        cursor = DBManager.execute_query(
            "DELETE FROM books WHERE book_id = ? AND owner_id = ?",
            (book_id, owner_id),
        )
        if cursor:
            return cursor.rowcount > 0
        else:
            return False

    @staticmethod
    def search(keyword):
        """Search for books by title, author, or ISBN (case-insensitive) and include owner username."""
        return DBManager.fetch_all(
            """SELECT books.book_id, books.title, books.author, books.isbn, users.username
                        FROM books
                        LEFT JOIN users ON books.owner_id = users.user_id
                        WHERE LOWER(books.title) LIKE LOWER(?)
                           OR LOWER(books.author) LIKE LOWER(?)
                           OR LOWER(books.isbn) LIKE LOWER(?)
                    """,
            (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
        )

    @staticmethod
    def get_owner_id(book_id):
        """Retrieve the owner ID of a book based on the book ID."""
        result = DBManager.fetch_one(
            "SELECT owner_id FROM books WHERE book_id = ?",
            (book_id,)
        )
        if result:
            return result[0]  # Return the owner_id
        return None  # Return None if book_id is not found