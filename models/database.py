import sqlite3

class DBManager:
    """Singleton class for managing SQLite database connection."""
    _connection = None

    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            cls._connection = sqlite3.connect("book_management.db")
        return cls._connection

    @classmethod
    def __del__(cls):
        if cls._connection:
            cls._connection.close()
            cls._connection = None

    @classmethod
    def setup_database(cls):
        """Sets up the SQLite database with the necessary tables."""
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

        conn.commit()

    @classmethod
    def execute_query(cls, query, params=()):
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor  # Return the cursor for further use if needed (e.g., for debugging)
        except Exception as e:
            print(f"Error executing query: {query} with params: {params}")
            print(f"Exception: {str(e)}")
            conn.rollback()  # Rollback in case of error

    @classmethod
    def fetch_all(cls, query, params=()):
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching all results for query: {query} with params: {params}")
            print(f"Exception: {str(e)}")
            return []  # Return an empty list in case of error

    @classmethod
    def fetch_one(cls, query, params=()):
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching one result for query: {query} with params: {params}")
            print(f"Exception: {str(e)}")
            return None  # Return None if an error occurs