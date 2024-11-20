from controllers.base import BaseModel
from models.database import DBManager

class Book(BaseModel):
    """
    Model representing a book in the database.

    Attributes:
        - book_id (int): Unique identifier for the book (assigned automatically).
        - title (str): Title of the book.
        - author (str): Author of the book.
        - isbn (str): ISBN of the book.
        - owner_id (int): ID of the user who owns the book.
    """

    def __init__(self, title, author, isbn, owner_id):
        """
        Initialize a new `Book` instance.

        Args:
            title (str): Title of the book.
            author (str): Author of the book.
            isbn (str): ISBN of the book.
            owner_id (int): ID of the user who owns the book.
        """
        self.book_id = None  # Will be assigned by the database.
        self.title = title
        self.author = author
        self.isbn = isbn
        self.owner_id = owner_id

    def save(self):
        """
        Save the book to the database.

        Inserts a new book record into the `books` table.
        Returns:
            bool: True if the book was saved successfully, False otherwise.
        """
        if DBManager.execute_query(
                "INSERT INTO books (title, author, isbn, owner_id) VALUES (?, ?, ?, ?)",
                (self.title, self.author, self.isbn, self.owner_id),
        ):
            return True
        else:
            return False

    @staticmethod
    def delete(book_id, owner_id):
        """
        Delete a book from the database.

        Args:
            book_id (int): ID of the book to delete.
            owner_id (int): ID of the user attempting to delete the book.

        Returns:
            bool: True if the book was deleted successfully, False otherwise.
        """
        cursor = DBManager.execute_query(
            "DELETE FROM books WHERE book_id = ? AND owner_id = ?",
            (book_id, owner_id),
        )
        if cursor:
            return cursor.rowcount > 0  # True if rows were affected.
        else:
            return False

    @staticmethod
    def search(keyword):
        """
        Search for books in the database.

        Args:
            keyword (str): The keyword to search for in the title, author, or ISBN.

        Returns:
            list: A list of books matching the search criteria. Each book includes:
                  - book_id
                  - title
                  - author
                  - isbn
                  - username of the owner.
        """
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
        """
        Retrieve the owner ID of a specific book.

        Args:
            book_id (int): ID of the book to lookup.

        Returns:
            int or None: The owner ID if found, None otherwise.
        """
        result = DBManager.fetch_one(
            "SELECT owner_id FROM books WHERE book_id = ?",
            (book_id,)
        )
        if result:
            return result[0]  # Return the owner_id if the query succeeds.
        return None  # Return None if no matching record is found.