# **Book Management System: BookMate**

## **Overview**
BookMate is a simple console-based Book Management application designed to manage books and user interactions. The application is built using Python and SQLite as the database, focusing on clear separation of layers: front-end (console interface), middle application tier (business logic), and back-end (SQLite database). 

The system allows users to:
- Sign up and log in to the system.
- Add, search, and delete books.
- Request books from other users.
- View and manage incoming book requests (accept/reject).

The project demonstrates object-oriented principles like inheritance, encapsulation, and abstraction while emphasizing design patterns and robust error handling.

---

## **Features**

### **Authentication**
- **Signup**: Create a new account with a username and password.
- **Login**: Securely log in with credentials.
- **Logout**: End the current session.

### **Book Management**
- **Add Book**: Add a book to the system with its title, author, ISBN, and ownership.
- **Search Books**: Search for books by title, author, or ISBN (case-insensitive). Leave the search field empty to list all books.
- **Delete Book**: Remove a book owned by the logged-in user.

### **Requests**
- **Request Book**: Request a book owned by another user.
- **View Incoming Requests**: See all pending requests for your books, with information about the book and the requester.
- **Accept/Reject Requests**: Accepting a request transfers ownership of the book to the requester. Rejected requests remain in the system but are marked as rejected.

---
## **Project Structure**

```plaintext
BookMate/
├── README.md                   # Project documentation with setup, usage, and features.
├── book_management.db          # SQLite database file storing users, books, and requests.
├── requirements.txt            # Dependencies for the project.
├── main.py                     # Entry point of the application, manages app flow.
├── controllers/
│   ├── __init__.py             # Marks the `controllers` directory as a Python package.
│   ├── base.py                 # Contains the base class with common functionalities.
│   ├── book.py                 # Logic for managing books (add, delete, search).
│   ├── request.py              # Logic for handling book requests (create, view, update).
│   └── user.py                 # User operations like signup, login, logout.
├── models/
│   ├── __init__.py             # Marks the `models` directory as a Python package.
│   └── database.py             # Manages database connections and operations.
└── views/
    ├── __init__.py             # Marks the `views` directory as a Python package.
    └── console_ui.py           # Handles user interaction via the console.
```

## **Setup Instructions**

### **Prerequisites**

- Python 3.7+
- SQLite3 (comes pre-installed with Python)

### **Steps to Run**

1. Clone the repository:
    
    ```bash
    git clone https://github.com/AwaleSajil/BookMate.git
    cd BookMate
    ```

2. Install dependencies:
    
    ```bash
    pip install -r requirements.txt
    ```
    
3. Run the application:
    
    ```bash 
    python main.py
    ```

---

# **Usage**

## **Console Interaction**

The `ConsoleUI` class (in `views/console_ui.py`) provides a menu-driven, text-based interface for interacting with the BookMate system.

---

## **Menus**

### **Welcome Menu**
Displayed at startup, offering:
- **Login**: Enter username and password to access an account.  
- **Signup**: Create a new account with a unique username and password.  
- **Exit**: Quit the application.

```plaintext
=== Welcome to BookMate ===
1. Login
2. Signup
3. Exit
```

2. **Action Menu** (Post-login):
    - After logging in, users have access to the Action Menu where they can choose actions related to book management, requests, and account management:
    ```plaintext
    === Action Menus ===
    1. Logout
    2. Add Book
    3. Delete Book
    4. Search Book
    5. Request a Book
    6. View Requests for Your Books
    7. Exit
    ```

### **User Input and Display**

- **Getting User Input**: The system uses Python's built-in `input()` function to gather user input, including username, password, and book information. For sensitive inputs like passwords, `getpass.getpass()` is used to hide the input for security.
  
    Example of getting input:
    ```python
    username = ConsoleUI.get_user_input("Enter username: ")
    password = ConsoleUI.get_user_password("Enter password: ")
    ```

- **Displaying Messages**: The system provides user feedback and status messages in different colors (using ANSI escape codes). The `display_message()` method is used to print messages with color coding to make them stand out.

    Example of displaying a message:
    ```python
    ConsoleUI.display_message("Book added successfully!", "green")
    ```

- **Displaying Books**: The `display_books()` method displays the list of books in the system. If no books are found, a message in yellow will be displayed.

    Example output:
    ```plaintext
    Found 3 Books:
    ID: 1, Title: "Book Title", Author: "Book Author", ISBN: "123456789", OwnerName: "Username"
    ```

- **Interacting with Requests**: The `interact_requests()` method allows users to accept, reject, or skip incoming book requests. For each request, users can decide to accept (transfers book ownership), reject (marks request as rejected), or skip (move to next request).

    Example interaction:
    ```plaintext
    Request: (1 / 3) for Book (title: "Book Title", author: "Book Author") from User: "Requester" (Pending)
    Accept (a) / Reject (r) / Skip (s) / Exit (e): a
    ```



---

## **Example Usage**

1. **Signup**:
    
    - Enter a unique username and a secure password when prompted. This will create a new account for you in the system.

2. **Login**:
    
    - After signing up, you can log in using the username and password you registered with. Enter your credentials when prompted to access the system.

3. **Add a Book**:
    
    - Once logged in, you can add a book by entering the book's title, author, and ISBN. The book will then be added to the system and associated with your user account.

4. **Search for Books**:
    
    - You can search for books by entering keywords related to the book's title, author, or ISBN. If you leave the search field blank, the system will list all available books.

5. **Request a Book**:
    
    - If you find a book you're interested in, you can request it by entering the book's ID. The system will record your request, and the book's owner will be notified.

6. **Manage Requests**:
    
    - If you are the owner of a book and receive requests from other users, you can view these requests and choose to accept or reject them. You can also skip requests or exit the request management process.

---

## **Database Schema**

### **Users Table**

| Column     | Type    | Description           |
|------------|---------|-----------------------|
| user_id    | INTEGER | Primary key           |
| username   | TEXT    | Unique username       |
| password   | TEXT    | Hashed password       |

### **Books Table**

| Column     | Type    | Description           |
|------------|---------|-----------------------|
| book_id    | INTEGER | Primary key           |
| title      | TEXT    | Book title            |
| author     | TEXT    | Book author           |
| isbn       | TEXT    | Book ISBN             |
| owner_id   | INTEGER | References user_id    |

### **Requests Table**

| Column      | Type    | Description              |
|-------------|---------|--------------------------|
| request_id  | INTEGER | Primary key              |
| book_id     | INTEGER | References book_id       |
| requester_id| INTEGER | User requesting the book |
| owner_id    | INTEGER | Current owner of the book|
| status      | TEXT    | Request status ('pending', 'accepted', 'rejected') |

---


## **Design Principles**

1. **Separation of Concerns**:
    
    - The system follows the principle of separation of concerns by dividing the application into distinct modules, each responsible for a specific set of tasks. 
    - This includes separate modules for:
      - Database management (`models/database.py`)
      - User authentication and management (`controllers/user.py`)
      - Book management (`controllers/book.py`)
      - Request handling (`controllers/request.py`)
      - User interface (`views/console_ui.py`)
    
    This modular structure makes it easier to maintain and scale the application.

2. **Object-Oriented Design**:
    
    - The system uses object-oriented design principles like **encapsulation**, **inheritance**, and **abstraction**.
    - Classes like `User`, `Book`, and `Request` represent entities in the system and encapsulate related functionality.
    - The `DBManager` class handles all database interactions, making the codebase more organized and reusable.

3. **Robustness**:
    
    - The application is designed to handle errors gracefully. Extensive use of `try-except` blocks ensures that unexpected errors do not crash the program.
    - Validations are used to ensure data integrity. For instance, books can only be deleted by their owner, and book requests are properly handled based on their current status.
    
4. **SQL Injection Prevention**:
    
    - To prevent SQL injection attacks, the application uses **parameterized queries** for all database interactions. 
    - This ensures that user input is safely handled when executing SQL statements, protecting the system from malicious inputs.
    
5. **Maintainability**:
    
    - The system is built with maintainability in mind. Each class and method has a clear, single responsibility, which follows the **Single Responsibility Principle (SRP)**.
    - Code is modular, with business logic separated from the user interface and database operations. This makes it easier to extend or modify any part of the system without affecting other parts.


---

## **Future Improvements**

- **Pagination**: Add pagination for book searches and requests.
- **Graphical UI**: Webpage like graphical interface can be user-friendly
- **Notification System**: Notify users when their requests are accepted or rejected.
- **Testing**: Add unit and integration tests for better reliability.

---

## **Contributors**

- [Sajil Awale](https://github.com/AwaleSajil/)

---

## **License**

This project is licensed under the MIT License.