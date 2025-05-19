import pymysql


class LibraryManagementSystem:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def create_connection(self):
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="library_db",
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()
        print("Database connected successfully!")
    
    def add_book(self):
        try:
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            year = int(input("Enter year of publication: "))
            genre = input("Enter genre: ")

            query = "INSERT INTO books (title, author, year, genre) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (title, author, year, genre))
            self.connection.commit()
            print("Book added successfully!")
        except Exception as e:
            self.connection.rollback()
            print("Error occurred while adding book:", e)

    def view_books(self):
        try:
            query = "SELECT * FROM books"
            self.cursor.execute(query)
            books = self.cursor.fetchall()

            if not books:
                print("\nNo books available in the library.")
                return

            print("\nAll Books:")
            for book in books:
                print(f"ID: {book['id']} | Title: {book['title']} | Author: {book['author']} | Year: {book['year']} | Genre: {book['genre']}")
        except Exception as e:
            print("Error fetching books:", e)

    def search_book(self):
        try:
            search_term = input("Enter title or author to search: ")
            query = "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s"
            self.cursor.execute(query, ('%' + search_term + '%', '%' + search_term + '%'))
            books = self.cursor.fetchall()

            if books:
                print("\nSearch Results:")
                for book in books:
                    print(f"ID: {book['id']} | Title: {book['title']} | Author: {book['author']} | Year: {book['year']} | Genre: {book['genre']}")
            else:
                print("No books found.")
        except Exception as e:
            print("Error occurred while searching:", e)

    def update_book(self):
        try:
            book_id = int(input("Enter book ID to update: "))
            self.cursor.execute("SELECT * FROM books WHERE id=%s", (book_id,))
            book = self.cursor.fetchone()

            if book:
                print(f"Current title: {book['title']}")
                title = input("Enter new title: ") or book['title']
                print(f"Current author: {book['author']}")
                author = input("Enter new author: ") or book['author']
                print(f"Current year: {book['year']}")
                year = input("Enter new year: ") or book['year']
                print(f"Current genre: {book['genre']}")
                genre = input("Enter new genre: ") or book['genre']

                query = "UPDATE books SET title=%s, author=%s, year=%s, genre=%s WHERE id=%s"
                self.cursor.execute(query, (title, author, year, genre, book_id))
                self.connection.commit()
                print("Book updated successfully!")
            else:
                print("Book not found.")
        except Exception as e:
            print("Error occurred while updating:", e)

    def delete_book(self):
        try:
            book_id = int(input("Enter book ID to delete: "))
            query = "DELETE FROM books WHERE id=%s"
            self.cursor.execute(query, (book_id,))
            self.connection.commit()
            print("Book deleted successfully!")
        except Exception as e:
            print("Error occurred while deleting book:", e)

    def run(self):
        while True:
            try:
                print('''\n===== Library Management System =====
1. Add Book
2. View All Books
3. Search Book
4. Update Book
5. Delete Book
6. Exit
''')
                choice = input("Enter choice (1-6): ")

                if choice == '1':
                    self.add_book()
                elif choice == '2':
                    self.view_books()
                elif choice == '3':
                    self.search_book()
                elif choice == '4':
                    self.update_book()
                elif choice == '5':
                    self.delete_book()
                elif choice == '6':
                    print("Exiting the program...")
                    break
                else:
                    print("Invalid choice. Please try again.")

            except Exception as e:
                print("An error occurred:", e)


if __name__ == "__main__":
    system = LibraryManagementSystem()
    system.create_connection()
    system.run()
