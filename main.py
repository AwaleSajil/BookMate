"""
Name: Sajil Awale
Date: 2024-11-21
Environment: Python 3.9.6, Pycharm IDE
Course: CS521

Description:
This Python program serves as the main entry point for the `BookMate` application, which is
a book management system designed to allow users to manage books and requests books.

The application uses an SQLite database to store information about books, users, and their interactions.
Users can perform actions such as logging in, signing up, adding books, searching for books, requesting books,
and responding to pending requests. The console-based interface allows for seamless interaction with the system.

Key features include:
- User authentication (login and signup)
- Book management (add, delete, search)
- Book request system (send and respond to requests)

This program demonstrates object-oriented programming concepts, including the use of models,
controllers, and views, organized into a clean and modular structure.
"""

# Import necessary modules
from views.console_ui import ConsoleUI  # Handles user interactions
from controllers.user import User       # Manages user authentication and actions
from controllers.book import Book       # Manages book-related operations
from controllers.request import Request # Handles book request functionality
from models.database import DBManager   # Manages database connections and setup

def main():
    """
    The main function initializes the database and starts the application loop.
    Users can log in, sign up, and perform various book-related actions based on their authentication state.
    """
    # Initialize the database
    DBManager.setup_database()

    # Create instances for user interaction and tracking the current user
    ui = ConsoleUI()
    current_user = User()

    while True:
        if not current_user.user_id:
            # Display the welcome menu for unauthenticated users
            ui.display_welcome_menu()
            choice = ui.get_user_input("Enter your choice: ")

            if choice == "1":
                # Handle user login
                username = ui.get_user_input("Enter username: ")
                password = ui.get_user_password("Enter password: ")
                current_user.login(username, password)
                if current_user.user_id:
                    ui.display_message(f"\nWelcome, {username}! ({current_user.user_id})", c="green")
                else:
                    ui.display_message("\nInvalid credentials. Try again.", c="red")

            elif choice == "2":
                # Handle user signup
                username = ui.get_user_input("Enter new username: ")
                password = ui.get_user_password("Enter new password: ")
                if User.save(username, password):
                    ui.display_message("\nSignup successful. You can now log in.", c="green")
                else:
                    ui.display_message("\nSignup failed", c="red")

            elif choice == "3":
                # Exit the application
                ui.display_message("\nExiting... Goodbye!", c="green")
                break

            else:
                ui.display_message("\nInvalid choice. Please try again.", c="red")

        else:
            # Display the actions menu for authenticated users
            ui.display_actions_menu()
            choice = ui.get_user_input("Enter your choice: ")

            if choice == "1":
                # Logout the current user
                current_user.user_id = None
                ui.display_message("Logged out successfully.", c="green")

            elif choice == "2":
                # Add a new book
                title = ui.get_user_input("Enter book title: ")
                author = ui.get_user_input("Enter author: ")
                isbn = ui.get_user_input("Enter ISBN: ")
                book = Book(title, author, isbn, current_user.user_id)
                if book.save():
                    ui.display_message("Book added successfully.", c="green")
                else:
                    ui.display_message("Failed to add book.", c="red")

            elif choice == "3":
                # Delete an existing book
                book_id = ui.get_user_input("Enter the ID of the book to delete: ")
                if Book.delete(book_id, current_user.user_id):
                    ui.display_message("Book deleted successfully.", c="green")
                else:
                    ui.display_message("Failed to remove book. Check the Book ID or your Ownership.", c="red")

            elif choice == "4":
                # Search for books
                keyword = ui.get_user_input("Enter keyword to search (Enter to list all): ")
                books = Book.search(keyword)
                ui.display_books(books)

            elif choice == "5":
                # Request a book
                book_id = ui.get_user_input("Enter Book ID to request: ")
                req = Request(book_id, current_user.user_id)
                if req.save():
                    ui.display_message("Book request sent.", c="green")
                else:
                    ui.display_message("Book request failed.", c="red")

            elif choice == "6":
                # Respond to pending book requests
                requests = Request.view_requests(current_user.user_id)
                ui.interact_requests(requests)

            elif choice == "7":
                # Exit the application
                ui.display_message("Exiting... Goodbye!", c="green")
                break

            else:
                ui.display_message("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
