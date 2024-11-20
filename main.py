from views.console_ui import ConsoleUI
from controllers.user import User
from controllers.book import Book
from controllers.request import Request
from models.database import DBManager

def main():
    DBManager.setup_database()
    ui = ConsoleUI()
    current_user = User()

    while True:
        if not current_user.user_id:
            ui.display_welcome_menu()
            choice = ui.get_user_input("Enter your choice: ")
            if choice == "1":
                # Login
                username = ui.get_user_input("Enter username: ")
                password = ui.get_user_password("Enter password: ")
                current_user.login(username, password)
                if current_user.user_id:
                    ui.display_message(f"\nWelcome, {username}! ({current_user.user_id})", c="green")
                else:
                    ui.display_message("\nInvalid credentials. Try again.", c="red")

            elif choice == "2":
                # Signup
                username = ui.get_user_input("Enter new username: ")
                password = ui.get_user_password("Enter new password: ")
                if User.signup(username, password):
                    ui.display_message("\nSignup successful. You can now log in.", c="green")
                else:
                    ui.display_message("\nSignup failed", c= "red")

            elif choice == "3":
                # Exit
                ui.display_message("\nExiting... Goodbye!", c="green")
                break
            else:
                ui.display_message("\nInvalid choice. Please try again.", c="red")
        else:
            ui.display_actions_menu()
            choice = ui.get_user_input("Enter your choice: ")
            if choice == "1":
                # Logout
                current_user.user_id = None
                ui.display_message("Logged out successfully.", c="green")
            elif choice == "2":
                # Add Book
                title = ui.get_user_input("Enter book title: ")
                author = ui.get_user_input("Enter author: ")
                isbn = ui.get_user_input("Enter ISBN: ")
                book = Book(title, author, isbn, current_user.user_id)
                if book.save():
                    ui.display_message("Book added successfully.", c="green")
                else:
                    ui.display_message("Failed to add book.", c="red")
            elif choice == "3":
                # Delete Book
                book_id = ui.get_user_input("Enter the ID of the book to delete: ")
                if Book.delete(book_id, current_user.user_id):
                    ui.display_message("Book deleted successfully.", c="green")
                else:
                    ui.display_message("Failed to remove book. Check the Book ID or your Ownership.", c="red")
            elif choice == "4":
                # Search Book
                keyword = ui.get_user_input("Enter keyword to search (Enter to list all): ")
                books = Book.search(keyword)
                ui.display_books(books)
            elif choice == "5":
                # Request a Book
                book_id = ui.get_user_input("Enter Book ID to request: ")
                req = Request(book_id, current_user.user_id)
                if req.save():
                    ui.display_message("Book request sent.", c="green")
                else:
                    ui.display_message("Book request failed.", c="red")
            elif choice == "6":
                # Respond to Book Request
                requests = Request.view_requests(current_user.user_id)
                ui.interact_requests(requests)

            elif choice == "7":
                ui.display_message("Exiting... Goodbye!", c="green")
                break
            else:
                ui.display_message("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()






