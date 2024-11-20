from controllers.base import BaseModel
from models.database import DBManager
from controllers.book import Book


class Request(BaseModel):
    """
    Represents a request for a book to transfer ownership.

    Attributes:
        - request_id (int): The unique identifier for the request.
        - book_id (int): The ID of the requested book.
        - requester_id (int): The ID of the user making the request.
        - owner_id (int): The ID of the user who currently owns the book.
        - status (str): The status of the request (e.g., "Pending", "Accepted").
    """

    def __init__(self, book_id, requester_id, owner_id=None):
        """
        Initializes a new request instance.

        Args:
            book_id (int): The ID of the requested book.
            requester_id (int): The ID of the user making the request.
            owner_id (int, optional): The ID of the current book owner. Defaults to None.
        """
        self.request_id = None
        self.book_id = book_id
        self.requester_id = requester_id
        self.owner_id = owner_id
        self.status = "Pending"  # Set default status to 'Pending'

    def save(self):
        """
        Save the request to the database, automatically setting the owner_id from the `books` table.

        This method performs the following steps:
        1. Fetches the owner_id for the given book from the `books` table.
        2. If the owner_id is found, inserts the request into the `requests` table.

        Returns:
            bool: True if the request was successfully saved, False otherwise.
        """
        # Step 1: Fetch the owner_id from the books table based on the book_id
        self.owner_id = Book.get_owner_id(self.book_id)

        # Step 2: If no owner_id is found, return False indicating that the request cannot be saved
        if self.owner_id is None:
            return False

        # Step 3: Insert the request into the requests table
        if DBManager.execute_query(
                "INSERT INTO requests (book_id, requester_id, owner_id) VALUES (?, ?, ?)",
                (self.book_id, self.requester_id, self.owner_id),
        ):
            return True  # Return True if insertion is successful
        else:
            return False  # Return False if insertion fails

    def delete(self):
        """
        Requests cannot be deleted, so this method raises a NotImplementedError.

        Raises:
            NotImplementedError: Deletion of requests is not supported.
        """
        raise NotImplementedError("Requests cannot be deleted.")

    @staticmethod
    def view_requests(owner_id):
        """
        View all pending requests for a specific owner.

        This method fetches a list of all requests for the given owner where the request status is 'Pending'.

        Args:
            owner_id (int): The ID of the owner whose requests are to be viewed.

        Returns:
            list: A list of dictionaries containing the details of each pending request.
        """
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
            (owner_id,)  # Filter by owner_id and only 'Pending' requests
        )

    @staticmethod
    def update_request_status(request_id, status):
        """
        Update the status of a request and, if the status is 'Accepted', update the book owner.

        This method performs the following steps:
        1. If the status is "Accepted", the book's owner is updated to the requester.
        2. The status of the request is updated in the `requests` table.

        Args:
            request_id (int): The ID of the request to be updated.
            status (str): The new status for the request (e.g., "Accepted", "Rejected").

        Returns:
            None
        """
        # Fetch the book_id and requester_id for the request to be updated
        request = DBManager.fetch_one(
            "SELECT book_id, requester_id FROM requests WHERE request_id = ?",
            (request_id,)  # Get details for the specific request_id
        )
        if request:
            book_id, requester_id = request

            # Step 2: If status is "Accepted", update the book owner in the books table
            if status == "Accepted":
                DBManager.execute_query(
                    "UPDATE books SET owner_id = ? WHERE book_id = ?",
                    (requester_id, book_id)  # Update book owner
                )

            # Step 3: Update the request status in the requests table
            DBManager.execute_query(
                "UPDATE requests SET status = ? WHERE request_id = ?",
                (status, request_id)  # Update the status of the request
            )