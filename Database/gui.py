import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import database

def login():
    def authenticate():
        username = entry_username.get()
        password = entry_password.get()
        if var_role.get() == "user":
            is_authenticated, role = database.authenticate_user(username, password)
        else:
            is_authenticated, role = database.authenticate_admin(username, password)
        if is_authenticated:
            login_window.destroy()
            if role == 'admin':
                main_window_admin()
            else:
                main_window_user()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    login_window = tk.Tk()
    login_window.title("Login")
    window_width = 300
    window_height = 200

    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    login_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


    label_username = tk.Label(login_window, text="Username")
    label_username.grid(row=0, column=0 ,padx=10, pady=10)
    entry_username = tk.Entry(login_window,width=35)
    entry_username.grid(row=0, column=1)

    label_password = tk.Label(login_window, text="Password")
    label_password.grid(row=1, column=0 ,padx=10, pady=10)
    entry_password = tk.Entry(login_window, show='*' ,width=35)
    entry_password.grid(row=1, column=1)

    var_role = tk.StringVar(value="user")
    radio_user = tk.Radiobutton(login_window, text="User", variable=var_role, value="user")
    radio_user.grid(row=2, column=0)
    radio_admin = tk.Radiobutton(login_window, text="Admin", variable=var_role, value="admin")
    radio_admin.grid(row=2, column=1, columnspan=2)

    button_login = tk.Button(login_window, text="Login",  command=authenticate ,width=15)
    button_login.grid(row=3, column=0,columnspan=2, pady=10)

    button_register = tk.Button(login_window, text="Register", command=register ,width=15) 
    button_register.grid(row=4, column=0, columnspan=2,pady=10)

    login_window.mainloop()

def register():
    def register_new_user():
        username = entry_username.get()
        password = entry_password.get()
        confirm_password = entry_confirm_password.get()
        if password == confirm_password:
            database.register_user(username, password)
            messagebox.showinfo("Registration Successful", "You can now log in")
            register_window.destroy()
        else:
            messagebox.showerror("Error", "Passwords do not match")

    register_window = tk.Tk()
    register_window.title("Register")
    window_width = 300
    window_height = 200

    screen_width = register_window.winfo_screenwidth()
    screen_height = register_window.winfo_screenheight()

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    register_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    label_username = tk.Label(register_window, text="Username")
    label_username.grid(row=0, column=0 ,padx=5, pady=10)
    entry_username = tk.Entry(register_window ,width=28)
    entry_username.grid(row=0, column=1 )

    label_password = tk.Label(register_window, text="Password")
    label_password.grid(row=1, column=0 ,padx=5, pady=10)
    entry_password = tk.Entry(register_window, show='*',width=28)
    entry_password.grid(row=1, column=1)

    label_confirm_password = tk.Label(register_window, text="Confirm Password")
    label_confirm_password.grid(row=2, column=0 ,padx=5, pady=10)
    entry_confirm_password = tk.Entry(register_window, show='*',width=28)
    entry_confirm_password.grid(row=2, column=1)

    button_register = tk.Button(register_window, text="Register", command=register_new_user ,width=15)
    button_register.grid(row=3, column=0 ,columnspan=2,pady=10)

    register_window.mainloop()

def main_window_user():
    def list_all_books():
        listbox.delete(0, tk.END)  
        books = database.get_all_books()  
        for book in books:
            listbox.insert(tk.END, (book[0], f"{book[1]} by {book[2]} (ISBN: {book[4]})"))

    def loan_book():
        if not listbox.curselection():
            messagebox.showerror("Error", "Please select a book to loan")
            return
        selected_tuple = listbox.get(listbox.curselection())
        book_id = selected_tuple[0]
        loan_date = loan_date_entry.get_date()
        return_date = return_date_entry.get_date()
        result = database.loan_book(book_id, loan_date, return_date)
        if result:
            messagebox.showinfo("Success", "Book loaned successfully")
        else:
            messagebox.showerror("Error", "Failed to loan the book or no copies available")
        list_all_books() 

    window = tk.Tk()
    window.title("User - Library System")
    window_width = 450
    window_height = 400

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    listbox = tk.Listbox(window, height=15, width=70)
    listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    label_loan_date = tk.Label(window, text="Loan Date")
    label_loan_date.grid(row=2, column=0, padx=10, pady=5)
    loan_date_entry = DateEntry(window, width=12, background='darkblue', foreground='white', borderwidth=2)
    loan_date_entry.grid(row=2, column=1, padx=10, pady=5)

    label_return_date = tk.Label(window, text="Return Date")
    label_return_date.grid(row=3, column=0, padx=10, pady=5)
    return_date_entry = DateEntry(window, width=12, background='darkblue', foreground='white', borderwidth=2)
    return_date_entry.grid(row=3, column=1, padx=10, pady=5)

    button_loan = tk.Button(window, text="Loan Book", command=loan_book)
    button_loan.grid(row=4, column=0, columnspan=2, pady=10)

    list_all_books()  

    window.mainloop()


def main_window_admin():
    def open_add_book_page():
        add_book_page()

    def open_remove_book_page():
        remove_book_page()

    def open_update_book_page():
        update_book_page()

    def open_view_all_books_page():
        view_all_books_page()

    def generate_report():
        report_window = tk.Toplevel(window)
        report_window.title("Generate Report")
        report_window_width = 570
        report_window_height = 400

        screen_width = report_window.winfo_screenwidth()
        screen_height = report_window.winfo_screenheight()

        center_x = int(screen_width / 2 - report_window_width / 2)
        center_y = int(screen_height / 2 - report_window_height / 2)

        report_window.geometry(f'{report_window_width}x{report_window_height}+{center_x}+{center_y}')

        label_report_title = tk.Label(report_window, text="Books Status Report")
        label_report_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        listbox = tk.Listbox(report_window, height=15, width=90)
        listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        data = database.get_books_status()
        for row in data:
            listbox.insert(tk.END, f"Book ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Year: {row[3]}, ISBN: {row[4]}, Quantity: {row[5]}, Loans Count: {row[6]}")

    def view_loans():
        loan_window = tk.Toplevel(window)
        loan_window.title("Loaned Books")
        loan_window_width = 500
        loan_window_height = 300

        screen_width = loan_window.winfo_screenwidth()
        screen_height = loan_window.winfo_screenheight()

        center_x = int(screen_width / 2 - loan_window_width / 2)
        center_y = int(screen_height / 2 - loan_window_height / 2)

        loan_window.geometry(f'{loan_window_width}x{loan_window_height}+{center_x}+{center_y}')

        listbox = tk.Listbox(loan_window, height=15, width=100)
        listbox.grid(row=0, column=0, padx=10, pady=10)

        loans = database.get_all_loans()
        for loan in loans:
            listbox.insert(tk.END, f"Book: {loan[1]}, User: {loan[2]}, Loan Date: {loan[3]}, Return Date: {loan[4]}")

    window = tk.Tk()
    window.title("Admin - Library System")
    window_width = 300
    window_height = 400

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    button_add_book = tk.Button(window, text="Add Book", command=open_add_book_page, width=18)
    button_add_book.grid(row=0, column=0, padx=20, pady=20, sticky='we')

    button_remove_book = tk.Button(window, text="Remove Book", command=open_remove_book_page, width=18)
    button_remove_book.grid(row=1, column=0, padx=20, pady=20, sticky='we')

    button_update_book = tk.Button(window, text="Update Book", command=open_update_book_page, width=18)
    button_update_book.grid(row=2, column=0, padx=20, pady=20, sticky='we')

    button_view_all_books = tk.Button(window, text="View All Books", command=open_view_all_books_page, width=18)
    button_view_all_books.grid(row=3, column=0, padx=20, pady=20, sticky='we')

    button_generate_report = tk.Button(window, text="Generate Report", command=generate_report, width=18)
    button_generate_report.grid(row=4, column=0, padx=20, pady=20, sticky='we')

    button_view_loans = tk.Button(window, text="View Loans", command=view_loans, width=18)
    button_view_loans.grid(row=5, column=0, padx=20, pady=20, sticky='we')

    window.grid_columnconfigure(0, weight=1)

    window.mainloop()



def add_book_page():
    def add_book():
            title = entry_title.get().strip()
            author = entry_author.get().strip()
            year = entry_year.get().strip()
            isbn = entry_isbn.get().strip()
            quantity = entry_quantity.get().strip()

            if not title or not author or not year or not isbn or not quantity:
                messagebox.showerror("Error", "All fields must be filled")
                return

            try:
                year = int(year)
                quantity = int(quantity)
            except ValueError:
                messagebox.showerror("Error", "Year and quantity must be integers")
                return

            if database.check_isbn_exists(isbn):
                messagebox.showerror("Error", "A book with this ISBN already exists")
                return

            database.insert_book(title, author, year, isbn, quantity)
            messagebox.showinfo("Success", "Book added successfully")

    window = tk.Tk()
    window.title("Add Book")
    window_width = 300
    window_height = 300

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    label_title = tk.Label(window, text="Title")
    label_title.grid(row=0, column=0, padx=10, pady=10)
    entry_title = tk.Entry(window, width=35)
    entry_title.grid(row=0, column=1)

    label_author = tk.Label(window, text="Author")
    label_author.grid(row=1, column=0, padx=10, pady=10)
    entry_author = tk.Entry(window, width=35)
    entry_author.grid(row=1, column=1)

    label_year = tk.Label(window, text="Year")
    label_year.grid(row=2, column=0, padx=10, pady=10)
    entry_year = tk.Entry(window, width=35)
    entry_year.grid(row=2, column=1)

    label_isbn = tk.Label(window, text="ISBN")
    label_isbn.grid(row=3, column=0, padx=10, pady=10)
    entry_isbn = tk.Entry(window, width=35)
    entry_isbn.grid(row=3, column=1)
    label_quantity = tk.Label(window, text="Quantity")
    label_quantity.grid(row=4, column=0, padx=10, pady=10)
    entry_quantity = tk.Entry(window, width=35)
    entry_quantity.grid(row=4, column=1)

    button_add = tk.Button(window, text="Add Book", command=add_book, width=15)
    button_add.grid(row=5, column=1, padx=20, pady=20, sticky='we')

    window.mainloop()

def remove_book_page():
    global selected_tuple
    selected_tuple = None

    def remove_book():
        if not selected_tuple:
            messagebox.showerror("Error", "Please select a book to remove")
            return
        book_id = selected_tuple[0]
        database.delete_book(book_id)
        messagebox.showinfo("Success", "Book removed successfully")
        view_all_books()

    def view_all_books():
        listbox.delete(0, tk.END)
        for book in database.view_books():
            listbox.insert(tk.END, (book[0], f"{book[1]} by {book[2]} (ISBN: {book[4]})"))

    def on_select(event):
        global selected_tuple
        if listbox.curselection():
            index = listbox.curselection()[0]
            selected_tuple = listbox.get(index)
    
    window = tk.Tk()
    window.title("Remove Book")
    window_width = 300
    window_height = 200

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    listbox = tk.Listbox(window, height=10, width=50)
    listbox.grid(row=0, column=0, columnspan=2)
    listbox.bind('<<ListboxSelect>>', on_select)

    button_remove = tk.Button(window, text="Remove Book", command=remove_book)
    button_remove.grid(row=1, columnspan=2)

    view_all_books()

    window.mainloop()

def update_book_page():
    global selected_tuple
    selected_tuple = None

    def update_book():
        if not selected_tuple:
            messagebox.showerror("Error", "Please select a book to update")
            return
        book_id = selected_tuple[0]
        title = entry_title.get().strip()
        author = entry_author.get().strip()
        year = entry_year.get().strip()
        isbn = entry_isbn.get().strip()
        quantity = entry_quantity.get().strip()

        if not title or not author or not year or not isbn or not quantity:
            messagebox.showerror("Error", "All fields must be filled")
            return

        try:
            year = int(year)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Year and quantity must be integers")
            return

        database.update_book(book_id, title, author, year, isbn, quantity)
        messagebox.showinfo("Success", "Book updated successfully")
        view_all_books()

    def view_all_books():
        listbox.delete(0, tk.END)
        for book in database.view_books():
            listbox.insert(tk.END, (book[0], f"{book[1]} by {book[2]} (Year: {book[3]}, ISBN: {book[4]}, Quantity: {book[5]})"))

    def on_select(event):
        global selected_tuple
        if listbox.curselection():
            index = listbox.curselection()[0]
            selected_tuple = listbox.get(index)
            entry_title.delete(0, tk.END)
            entry_title.insert(tk.END, selected_tuple[1].split(" by ")[0])
            entry_author.delete(0, tk.END)
            entry_author.insert(tk.END, selected_tuple[1].split(" by ")[1].split(" (Year: ")[0])
            entry_year.delete(0, tk.END)
            entry_year.insert(tk.END, selected_tuple[1].split(" (Year: ")[1].split(", ISBN: ")[0])
            entry_isbn.delete(0, tk.END)
            entry_isbn.insert(tk.END, selected_tuple[1].split(", ISBN: ")[1].split(", Quantity: ")[0])
            entry_quantity.delete(0, tk.END)
            entry_quantity.insert(tk.END, selected_tuple[1].split(", Quantity: ")[1][:-1])

    window = tk.Tk()
    window.title("Update Book")
    window_width = 330
    window_height = 400

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    listbox = tk.Listbox(window, height=10, width=50)
    listbox.grid(row=0, column=0, columnspan=2,padx=10,pady=20)
    listbox.bind('<<ListboxSelect>>', on_select)

    label_title = tk.Label(window, text="Title")
    label_title.grid(row=1, column=0)
    entry_title = tk.Entry(window, width=35)
    entry_title.grid(row=1, column=1,pady=5)

    label_author = tk.Label(window, text="Author")
    label_author.grid(row=2, column=0)
    entry_author = tk.Entry(window, width=35)
    entry_author.grid(row=2, column=1,pady=5)

    label_year = tk.Label(window, text="Year")
    label_year.grid(row=3, column=0)
    entry_year = tk.Entry(window, width=35)
    entry_year.grid(row=3, column=1,pady=5)

    label_isbn = tk.Label(window, text="ISBN")
    label_isbn.grid(row=4, column=0)
    entry_isbn = tk.Entry(window, width=35)
    entry_isbn.grid(row=4, column=1,pady=5)

    label_quantity = tk.Label(window, text="Quantity")
    label_quantity.grid(row=5, column=0)
    entry_quantity = tk.Entry(window, width=35)
    entry_quantity.grid(row=5, column=1,pady=5)

    button_update = tk.Button(window, text="Update Book", command=update_book)
    button_update.grid(row=6, columnspan=2,pady=10)

    view_all_books()

    window.mainloop()



def view_all_books_page():
    def view_all_books():
        listbox.delete(0, tk.END)
        for book in database.view_books():
            listbox.insert(tk.END, f"{book[1]} by {book[2]} (ISBN: {book[4]})")

    window = tk.Tk()
    window.title("View All Books")
    window_width = 300
    window_height = 200

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    listbox = tk.Listbox(window, height=10, width=50)
    listbox.grid(row=0, column=0, columnspan=2)

    view_all_books()

    window.mainloop()

if __name__ == "__main__":
    login()