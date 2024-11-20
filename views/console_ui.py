import getpass
from controllers.request import Request

"""
ConsoleUI class provides methods to interact with the user through the command-line interface (CLI).
It handles the display of menus, user inputs, and showing relevant information (e.g., books, requests).
The methods in this class are static, as they do not depend on any instance-specific data.
"""
class ConsoleUI:
    # Dictionary to store color codes for console output
    text_color = dict(
        red="\033[31m",  # Red color code
        green="\033[32m",  # Green color code
        yellow="\033[33m",  # Yellow color code
        reset="\033[0m"  # Reset to default color
    )

    @staticmethod
    def display_welcome_menu():
        """
        Displays the welcome menu with options for login, signup, or exit.
        """
        print("\n=== Welcome to BookMate ===")
        print("1. Login")
        print("2. Signup")
        print("3. Exit")

    @staticmethod
    def display_actions_menu():
        """
        Displays the actions menu for logged-in users with options to logout,
        add or delete books, search books, request books, view requests, or exit.
        """
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
        """
        Prompts the user for input with the given message.

        Args:
            prompt (str): The message to display to the user.

        Returns:
            str: The input provided by the user.
        """
        return input(prompt)

    @staticmethod
    def get_user_password(prompt):
        """
        Prompts the user for a password (hides input for security).

        Args:
            prompt (str): The message to display to the user.

        Returns:
            str: The password entered by the user.
        """
        return getpass.getpass(prompt)  # Hides the password input for security

    @staticmethod
    def display_message(message, c=None):
        """
        Displays a message to the user with optional color formatting.

        Args:
            message (str): The message to display.
            c (str, optional): The color code to format the message (e.g., 'red', 'green').
        """
        color = ConsoleUI.text_color.get(c)  # Fetch the color code
        if color:
            print(f"{color}{message}{ConsoleUI.text_color.get('reset')}")
        else:
            print(message)

    @staticmethod
    def display_books(books):
        """
        Displays a list of books in a formatted manner.

        Args:
            books (list): A list of books to display. Each book is represented as a tuple.
        """
        if not books:  # Check if no books are found
            print(f"{ConsoleUI.text_color.get('yellow')}No books found.{ConsoleUI.text_color.get('reset')}")
        else:
            print(f"\n{ConsoleUI.text_color.get('green')}Found {len(books)} Books:{ConsoleUI.text_color.get('reset')}")
            for book in books:  # Loop through the books and display their details
                print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, ISBN: {book[3]}, OwnerName: {book[4]}")

    @staticmethod
    def interact_requests(requests):
        """
        Allows the user to interact with requests for their books, enabling them
        to accept, reject, or skip the requests.

        Args:
            requests (list): A list of requests for the user's books. Each request is a tuple.
        """
        n = len(requests)  # Get the number of requests
        if n > 0:  # If there are requests to process
            for i, req in enumerate(requests):  # Loop through each request
                print(
                    f"{ConsoleUI.text_color.get('yellow')} Request: ({i + 1} / {n}) for Book (title: {req[2]}, author: {req[3]}) from User: {req[5]} ({req[4]}) {ConsoleUI.text_color.get('reset')}")

                # Ask the user what action to take on this request
                decision = input("Accept (a) / Reject (r) / Skip (s) / Exit (e): ")

                # Take action based on the user's input
                if decision == "a":
                    Request.update_request_status(req[0], "Accepted")
                elif decision == "r":
                    Request.update_request_status(req[0], "Rejected")
                elif decision == "s":
                    continue  # Skip to the next request
                else:
                    break  # Exit the loop
        else:
            print(
                f"{ConsoleUI.text_color.get('red')} No requests were made for your book {ConsoleUI.text_color.get('reset')}")
