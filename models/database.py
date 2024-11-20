import sqlite3

class DBManager:
    """Singleton class for managing SQLite database connection."""
    _connection = None  # Static variable to hold the database connection

    @classmethod
    def get_connection(cls):
        """
        Returns the current database connection. If no connection exists, it creates one.

        Returns:
            sqlite3.Connection: The SQLite connection object.
        """
        if cls._connection is None:
            cls._connection = sqlite3.connect("book_management.db")  # Creates a new connection if none exists
        return cls._connection

    @classmethod
    def __del__(cls):
        """
        Destructor method to close the database connection when the DBManager object is deleted.
        """
        if cls._connection:
            cls._connection.close()  # Close the connection
            cls._connection = None  # Set the connection to None

    @classmethod
    def setup_database(cls):
        """
        Sets up the SQLite database with the necessary tables (users, books, and requests).

        This method is used to initialize the database schema, creating tables if they do not already exist.
        """
        conn = cls.get_connection()
        cursor = conn.cursor()

        # Users Table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
            """
        )

        # Books Table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                owner_id INTEGER NOT NULL,
                FOREIGN KEY(owner_id) REFERENCES users(user_id)
            )
            """
        )

        # Requests Table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS requests (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                requester_id INTEGER NOT NULL,
                owner_id INTEGER NOT NULL,
                status TEXT CHECK(status IN ('Pending', 'Accepted', 'Rejected')) DEFAULT 'Pending',
                FOREIGN KEY(book_id) REFERENCES books(book_id),
                FOREIGN KEY(requester_id) REFERENCES users(user_id),
                FOREIGN KEY(owner_id) REFERENCES users(user_id)
            )
            """
        )

        conn.commit()  # Commit the changes to the database

    @classmethod
    def execute_query(cls, query, params=()):
        """
        Executes a write query (INSERT, UPDATE, DELETE) on the database.

        Args:
            query (str): The SQL query string to be executed.
            params (tuple): The parameters to be passed into the SQL query.

        Returns:
            sqlite3.Cursor: The cursor object if the query is executed successfully.
        """
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)  # Execute the query with the provided parameters
            conn.commit()  # Commit the changes
            return cursor  # Return the cursor for further use if needed (e.g., for debugging)
        except Exception as e:
            print(f"Error executing query: {query} with params: {params}")
            print(f"Exception: {str(e)}")
            conn.rollback()  # Rollback in case of an error

    @classmethod
    def fetch_all(cls, query, params=()):
        """
        Executes a read query (SELECT) and fetches all results.

        Args:
            query (str): The SQL query string to be executed.
            params (tuple): The parameters to be passed into the SQL query.

        Returns:
            list: A list of tuples containing the query results.
        """
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)  # Execute the query with the provided parameters
            return cursor.fetchall()  # Return all rows as a list of tuples
        except Exception as e:
            print(f"Error fetching all results for query: {query} with params: {params}")
            print(f"Exception: {str(e)}")
            return []  # Return an empty list in case of an error

    @classmethod
    def fetch_one(cls, query, params=()):
        """
        Executes a read query (SELECT) and fetches one result.

        Args:
            query (str): The SQL query string to be executed.
            params (tuple): The parameters to be passed into the SQL query.

        Returns:
            tuple or None: The first row of the query result, or None if no result is found.
        """
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)  # Execute the query with the provided parameters
            return cursor.fetchone()  # Return the first result (or None if not found)
        except Exception as e:
            print(f"Error fetching one result for query: {query} with params: {params}")
            print(f"Exception: {str(e)}")
            return None  # Return None if an error occurs