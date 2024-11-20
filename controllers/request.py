import sqlite3
from base.base import BaseModel
from models.database import DBManager
from controllers.book import Book

class Request(BaseModel):
    def __init__(self, book_id, requester_id, owner_id=None):
        self.request_id = None
        self.book_id = book_id
        self.requester_id = requester_id
        self.owner_id = owner_id
        self.status = "Pending"

    def save(self):
        """Save the request, automatically setting the owner_id from the books table."""
        # Step 1: Fetch the owner_id from the books table based on the book_id using Book.get_owner_id
        self.owner_id = Book.get_owner_id(self.book_id)

        if self.owner_id is None:
            return False  # If the book doesn't exist, return False

        # Step 2: Insert the request into the requests table
        if DBManager.execute_query(
            "INSERT INTO requests (book_id, requester_id, owner_id) VALUES (?, ?, ?)",
            (self.book_id, self.requester_id, self.owner_id),
        ):
            return True
        else:
            return False

    def delete(self):
        raise NotImplementedError("Requests cannot be deleted.")

    @staticmethod
    def view_requests(owner_id):
        return DBManager.fetch_all(
            """SELECT
                            requests.request_id,
                            books.book_id, books.title, books.author,
                            users.user_id, users.username,
                            requests.status
                        FROM requests
                        LEFT JOIN books ON requests.book_id = books.book_id
                        LEFT JOIN users ON requests.requester_id = users.user_id
                        WHERE requests.owner_id = ? AND requests.status = 'Pending'
                        ORDER BY requests.request_id DESC
                        """,
            (owner_id,)
        )

    @staticmethod
    def update_request_status(request_id, status):
        request = DBManager.fetch_one(
            "SELECT book_id, requester_id FROM requests WHERE request_id = ?",
            (request_id,)
        )
        if request:
            book_id, requester_id = request
            # Step 2: If status is "Accepted", update the book owner in the books table
            if status == "Accepted":
                DBManager.execute_query(
                    "UPDATE books SET owner_id = ? WHERE book_id = ?",
                    (requester_id, book_id)
                )
            # Step 3: Update the request status in the requests table
            DBManager.execute_query(
                "UPDATE requests SET status = ? WHERE request_id = ?",
                (status, request_id),
            )

