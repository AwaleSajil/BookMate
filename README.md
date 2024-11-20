# **Book Management System**

## **Overview**
The Book Management System is a simple console-based application designed to manage books and user interactions. The application is built using Python and SQLite as the database, focusing on clear separation of layers: front-end (console interface), middle application tier (business logic), and back-end (SQLite database). 

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
BookManagementSystem/
├── app.py                # Main entry point for the application
├── db_manager.py         # Manages all database operations
├── user.py               # Handles user-related functionalities
├── book.py               # Handles book-related functionalities
├── request.py            # Handles request-related functionalities
├── console_ui.py         # Manages user interaction through the console
├── requirements.txt      # Python dependencies
├── README.md             # Documentation for the project
└── database/
    └── book_management.db # SQLite database file
```

## **Setup Instructions**

### **Prerequisites**

- Python 3.7+
- SQLite3 (comes pre-installed with Python)

### **Steps to Run**

1. Clone the repository:
    
    ```bash
    git clone https://github.com/AwaleSajil/BookMate.git
    cd book-management-system
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

## **Usage**

### **Main Menu**

```plaintext
1. Login 
2. Signup 
2. 3. Exit
```


### **Logged-In / Action Menu**

```plaintext
1. Logout
2. Add Book
3. Delete Book
4. Search Book
5. Request a Book
6. View Requests for Your Books
7. Exit
```



---

## **Example Usage**

1. **Signup**:
    
    - Enter a unique username and a secure password.
2. **Login**:
    
    - Enter your credentials to access the system.
3. **Add a Book**:
    
    - Enter the title, author, and ISBN of the book.
4. **Search for Books**:
    
    - Search for books by keyword or leave blank to list all books.
5. **Request a Book**:
    
    - Enter the ID of the book you want to request.
6. **Manage Requests**:
    
    - View incoming requests, and accept or reject them.

---

## **Database Schema**

### **Users Table**

|Column|Type|Description|
|---|---|---|
|user_id|INTEGER|Primary key|
|username|TEXT|Unique username|
|password|TEXT|Hashed password|

### **Books Table**

|Column|Type|Description|
|---|---|---|
|book_id|INTEGER|Primary key|
|title|TEXT|Book title|
|author|TEXT|Book author|
|isbn|TEXT|Book ISBN|
|owner_id|INTEGER|References user_id|

### **Requests Table**

|Column|Type|Description|
|---|---|---|
|request_id|INTEGER|Primary key|
|book_id|INTEGER|References book_id|
|requester_id|INTEGER|User requesting the book|
|owner_id|INTEGER|Current owner of the book|
|status|TEXT|Request status ('pending', 'accepted', 'rejected')|

---

## **Design Principles**

1. **Separation of Concerns**:
    
    - The system is divided into modules for database operations, user management, book management, and request handling.
2. **Object-Oriented Design**:
    
    - Classes like `User`, `Book`, and `Request` encapsulate related functionality.
    - The `DBManager` class handles all database interactions.
3. **Robustness**:
    
    - Extensive use of `try-except` blocks to handle errors gracefully.
    - Validations ensure data integrity (e.g., books can only be deleted by their owner).
4. **SQL Injection Prevention**:
    
    - Parameterized queries are used to prevent SQL injection attacks.

---

## **Future Improvements**

- **Enhanced Security**: Implement password salting and more secure hashing algorithms.
- **Pagination**: Add pagination for book searches and requests.
- **Notification System**: Notify users when their requests are accepted or rejected.
- **Testing**: Add unit and integration tests for better reliability.

---

## **Contributors**

- [Sajil Awale](https://github.com/AwaleSajil/)

---

## **License**

This project is licensed under the MIT License.