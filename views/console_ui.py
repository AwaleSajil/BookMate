import getpass
from controllers.request import Request

class ConsoleUI:
    text_color = dict(
        red="\033[31m",
        green = "\033[32m",
        yellow = "\033[33m",
        reset = "\033[0m"  # Reset to default color
    )


    @staticmethod
    def display_welcome_menu():
        print("\n=== Welcome to BookMate ===")
        print("1. Login")
        print("2. Signup")
        print("3. Exit")

    @staticmethod
    def display_actions_menu():
        print("\n=== Action Menus ===")
        print("1. Logout")
        print("2. Add Book")
        print("3. Delete Book")
        print("4. Search Book")
        print("5. Request a Book")
        print("6. View Requests for Your Books")
        print("7. Exit")

    @staticmethod
    def get_user_input(prompt):
        return input(prompt)

    @staticmethod
    def get_user_password(prompt):
        return getpass.getpass(prompt)

    @staticmethod
    def display_message(message,c=None):
        color =  ConsoleUI.text_color.get(c)
        if color:
            print(f"{color}{message}{ConsoleUI.text_color.get('reset')}")
        else:
            print(message)

    @staticmethod
    def display_books(books):
        if not books:
            print(f"{ConsoleUI.text_color.get('yellow')}No books found.{ConsoleUI.text_color.get('reset')}")
        else:
            print(f"\n{ConsoleUI.text_color.get('green')}Found {len(books)} Books:{ConsoleUI.text_color.get('reset')}")
            for book in books:
                print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, ISBN: {book[3]}, OwnerName: {book[4]}")

    @staticmethod
    def interact_requests(requests):
        n = len(requests)
        if n > 0:
            for i, req in enumerate(requests):
                print(f"{ConsoleUI.text_color.get('yellow')} Request: ({i+1} / {n}) for Book (title: {req[2]}, author: {req[3]}) from User: {req[5]} ({req[4]}) {ConsoleUI.text_color.get('reset')}")
                decision = input("Accept (a) / Reject (r) / Skip (s) / Exit (e): ")
                if decision == "a":
                    Request.update_request_status(req[0], "Accepted")
                elif decision == "r":
                    Request.update_request_status(req[0], "Rejected")
                elif decision == "s":
                    continue
                else:
                    break
        else:
            print(f"{ConsoleUI.text_color.get('red')} No requests were made for your book {ConsoleUI.text_color.get('reset')}")