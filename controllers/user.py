import bcrypt
from controllers.base import BaseModel
from models.database import DBManager


class User(BaseModel):
    """
    Represents a user in the system.

    Attributes:
        - user_id (int): Unique identifier for the user, fetched from the database.
        - username (str): Username chosen by the user.
        - password (str): User's password, stored in a hashed form.
    """

    def __init__(self):
        """
        Initialize a new `User` instance with default values for user attributes.

        Attributes are set to `None` initially and will be populated upon user login.
        """
        self.user_id = None
        self.username = None
        self.password = None

    def delete(self):
        """
        Attempting to delete a user raises a NotImplementedError, as user deletion is not allowed in this system.

        Raises:
            NotImplementedError: Users cannot be deleted in this system.
        """
        raise NotImplementedError("Users cannot be deleted.")  # Prevent deletion of users.

    def login(self, username, password):
        """
        Authenticate a user by checking the provided username and password.

        Args:
            username (str): The username entered by the user.
            password (str): The password entered by the user.

        Returns:
            str or None: Returns the username if login is successful, otherwise returns None.
        """
        # Fetch the user record from the database based on the username
        user = DBManager.fetch_one(
            "SELECT user_id, username, password FROM users WHERE username = ?",
            (username,)  # Search for the user by username
        )

        # Check if the user exists and the password matches the stored hashed password
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            self.user_id  = user[0]
            self.username = user[1]
            self.password = user[2]
            return username  # Return the username upon successful login
        return None  # Return None if login fails

    @classmethod
    def save(cls, username, password):
        """
        Create a new user account by hashing the password and storing the credentials in the database.

        Args:
            username (str): The desired username for the new user.
            password (str): The desired password for the new user.

        Returns:
            bool: True if the signup was successful, False otherwise.
        """
        # Hash the password using bcrypt before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert the username and hashed password into the database
        if DBManager.execute_query(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)  # Insert the credentials into the database
        ):
            return True  # Return True if the insertion was successful
        else:
            return False  # Return False if there was an error during insertion



