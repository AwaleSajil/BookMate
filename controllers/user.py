import bcrypt
import sqlite3
from base.base import BaseModel
from models.database import DBManager


class User(BaseModel):
    def __init__(self):
        self.user_id = None
        self.username = None
        self.password = None

    def save(self):
        conn = DBManager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (self.username, self.password),
        )
        conn.commit()

    def delete(self):
        raise NotImplementedError("Users cannot be deleted.")

    def login(self, username, password):
        user = DBManager.fetch_one(
            "SELECT user_id, username, password FROM users WHERE username = ?",
            (username,),
        )

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            self.user_id  = user[0]
            self.username = user[1]
            self.password = user[2]
            return username
        return None

    @classmethod
    def signup(cls, username, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        if DBManager.execute_query(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password),
        ):
                return True
        else:
            return False



