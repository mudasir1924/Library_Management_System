import pymysql
from datetime import datetime

# Connect to the database
def get_db_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="root123",
        database="library_db",
        cursorclass=pymysql.cursors.DictCursor  
    )
    return connection

# Add a new book to the library
def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    year = int(input("Enter year of publication: "))
    genre = input("Enter genre: ")

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO books (title, author, year, genre)
            VALUES (%s, %s, %s, %s)
        """, (title, author, year, genre))
        connection.commit()
    connection.close()
    print("Book added successfully!")

# View all books in the library
def view_books():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()

    connection.close()

    if not books:
        print("\nNo books available in the library.")
        return

    print("\nAll Books:")
    for book in books:
        print(f"ID: {book['id']} | Title: {book['title']} | Author: {book['author']} | Year: {book['year']} | Genre: {book['genre']}")

# Search a book by title or author
def search_book():
    search_term = input("Enter title or author to search: ")
    
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM books WHERE title LIKE %s OR author LIKE %s
        """, ('%' + search_term + '%', '%' + search_term + '%'))
        books = cursor.fetchall()

    if books:
        print("\nSearch Results:")
        for book in books:
            print(f"ID: {book['id']} | Title: {book['title']} | Author: {book['author']} | Year: {book['year']} | Genre: {book['genre']}")
    else:
        print("No books found.")
    
    connection.close()

# Update book details
def update_book():
    book_id = int(input("Enter book ID to update: "))
    
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM books WHERE id=%s", (book_id,))
        book = cursor.fetchone()

        if book:
            print(f"Current title: {book['title']}")
            title = input("Enter new title: ") or book['title']
            print(f"Current author: {book['author']}")
            author = input("Enter new author: ") or book['author']
            print(f"Current year: {book['year']}")
            year = input("Enter new year: ") or book['year']
            print(f"Current genre: {book['genre']}")
            genre = input("Enter new genre: ") or book['genre']

            cursor.execute("""
                UPDATE books SET title=%s, author=%s, year=%s, genre=%s WHERE id=%s
            """, (title, author, year, genre, book_id))
            connection.commit()
            print("Book updated successfully!")
        else:
            print("Book not found.")
    
    connection.close()

# Delete a book
def delete_book():
    book_id = int(input("Enter book ID to delete: "))
    
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
        connection.commit()
        print("Book deleted successfully!")

    connection.close()

# Display the main menu
def show_menu():
    while True:
        print("\n===== Library Management System =====")
        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Book")
        print("4. Update Book")
        print("5. Delete Book")
        print("6. Exit")
        
        choice = input("Enter choice (1-6): ")

        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
        elif choice == '3':
            search_book()
        elif choice == '4':
            update_book()
        elif choice == '5':
            delete_book()
        elif choice == '6':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    show_menu()
