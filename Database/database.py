import mysql.connector
from mysql.connector import Error

def connect():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Ka@787898",
            database="library_system"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
def register_user(username, password):
    conn = connect()
    if conn is None:
        print("Failed to connect to the database.")
        return
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO members (username, password,role) VALUES (%s, %s, %s)", (username, password, "user"))
        conn.commit()
    except Error as e:
        print(f"Error: '{e}'")
    finally:
        conn.close()
def authenticate_user(username, password):
    conn = connect()
    if conn is None:
        print("Failed to connect to the database.")
        return False, None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM members WHERE username=%s AND password=%s AND role=%s", (username, password, "user"))
        row = cur.fetchone()
        if row:
            return True, 'user'
        else:
            return False, None
    except Error as e:
        print(f"Error: '{e}'")
        return False, None
    finally:
        conn.close()
def authenticate_admin(username, password):
    conn = connect()
    if conn is None:
        print("Failed to connect to the database.")
        return False, None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM members WHERE username=%s AND password=%s AND role=%s", (username, password, "admin"))
        row = cur.fetchone()
        if row:
            return True, 'admin'
        else:
            return False, None
    except Error as e:
        print(f"Error: '{e}'")
        return False, None
    finally:
        conn.close()   
def check_isbn_exists(isbn):
    conn = connect()
    if conn is None:
        print("Failed to connect to the database.")
        return False
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM books WHERE isbn=%s", (isbn,))
        row = cur.fetchone()
        return row is not None
    except Error as e:
        print(f"Error: '{e}'")
        return False
    finally:
        conn.close()

def insert_book(title, author, year, isbn, quantity):
    conn = connect()
    if conn is None:
        print("Failed to connect to the database.")
        return
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO books (title, author, year, isbn, quantity) VALUES (%s, %s, %s, %s, %s)",(title, author, year, isbn, quantity))
        conn.commit()
    except Error as e:
        print(f"Error: '{e}'")
    finally:
        conn.close()

def view_books():
    conn = connect()
    if conn is None:
        print("Failed to connect to the database.")
        return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM books")
        rows = cur.fetchall()
        return rows
    except Error as e:
        print(f"Error: '{e}'")
        return []
    finally:
        conn.close()


def delete_book(id):
    conn = connect()
    if conn is None:
        print("Failed to connect to the database.")
        return
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM books WHERE id=%s", (id,))
        conn.commit()
    except Error as e:
        print(f"Error: '{e}'")
    finally:
        conn.close()

def update_book(book_id, title, author, year, isbn, quantity):
    conn = connect()
    if conn is None:
        print("Failed to connect to the database.")
        return
    try:
        cur = conn.cursor()
        cur.execute("UPDATE books SET title=%s, author=%s, year=%s, isbn=%s, quantity=%s WHERE id=%s",(title, author, year, isbn, quantity, book_id))
        conn.commit()
    except Error as e:
        print(f"Error: '{e}'")
    finally:
        conn.close()


def get_all_books():
    conn = connect()
    if conn is None:
        print("Failed to connect to the database.")
        return []

    query = "SELECT * FROM books"

    try:
        cur = conn.cursor()
        print(f"Executing query: {query}")  
        cur.execute(query)
        books = cur.fetchall()
        print(f"Books fetched: {books}")  
        return books
    except Error as e:
        print(f"Error: '{e}'")
        return []
    finally:
        conn.close()

def loan_book(book_id, loan_date, return_date):
    conn = connect()
    if conn is None:
        print("Failed to connect to the database.")
        return False

    try:
        cur = conn.cursor()
        cur.execute("SELECT quantity FROM books WHERE id=%s", (book_id,))
        book = cur.fetchone()
        if book and book[0] > 0:
            cur.execute("UPDATE books SET quantity = quantity - 1 WHERE id=%s", (book_id,))
            cur.execute("INSERT INTO loans (book_id, member_id, loan_date, return_date) VALUES (%s, %s, %s, %s)",
                        (book_id, 1, loan_date, return_date))  
            conn.commit()
            return True
        else:
            return False
    except Error as e:
        print(f"Error: '{e}'")
        return False
    finally:
        conn.close()

def get_all_loans():
    conn = connect()
    if conn is None:
        print("Failed to connect to the database.")
        return []

    query = """
    SELECT loans.id, books.title, members.username, loans.loan_date, loans.return_date
    FROM loans
    JOIN books ON loans.book_id = books.id
    JOIN members ON loans.member_id = members.id
    """

    try:
        cur = conn.cursor()
        cur.execute(query)
        loans = cur.fetchall()
        return loans
    except Error as e:
        print(f"Error: '{e}'")
        return []
    finally:
        conn.close()

def get_books_status():
    conn = connect()
    if conn is None:
        print("Failed to connect to the database.")
        return []

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM view_all_books_status")
        books = cur.fetchall()
        return books
    except Error as e:
        print(f"Error: '{e}'")
        return []
    finally:
        conn.close()