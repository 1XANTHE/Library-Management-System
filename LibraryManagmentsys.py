import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3

# DATABSE 
class Library:
        #CONNECTING SQLITE
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS LibraryData (book_name TEXT, borrower TEXT)")
        self.conn.commit()
        #BOOKS LIST 
        self.books = ['To Kill a Mockingbird', 'Harry Potter and the Philosopher\'s Stone', 'The Lord of the Rings', 'The Great Gatsby', 'Pride and Prejudice', 'The Diary of Anne Frank', 'The Catcher in the Rye', 'The Hobbit', 'Fahrenheit 451']

        #ADDING A BOOKS
    def add_book(self, book_name, window):
        self.books.append(book_name)
        messagebox.showinfo("Success", "The book has been added successfully.")
        window.destroy()

        #REMOVING A BOOK
    def remove_book(self, book_number, window):
        if book_number <= len(self.books):
            self.books.pop(book_number - 1)
            messagebox.showinfo("Success", "The book has been removed successfully.")
            window.destroy()
        else:
            messagebox.showerror("Error", "Sorry, the book number you entered is not valid.")

        #DISPLAYING THE AVAILABLE BOOKS
    def display_books(self):
        list_window = tk.Toplevel(root)
        list_window.title("Available Books")

        listbox = tk.Listbox(list_window, font=("Arial", 14))
        for i, book in enumerate(self.books, 1):
            listbox.insert(tk.END, f"{i}. {book}")
        listbox.pack(pady=10)

        ok_button = tk.Button(list_window, text="OK", command=list_window.destroy, font=("Arial", 14))
        ok_button.pack(pady=10)

        #BORROWING THE BOOK
    def lend_book(self, requested_book_number, borrower, window):
        if requested_book_number <= len(self.books):
            requested_book = self.books.pop(requested_book_number - 1)
            self.cursor.execute("INSERT INTO LibraryData VALUES (?, ?)", (requested_book, borrower))
            self.conn.commit()
            messagebox.showinfo("Success", "You have now borrowed the book.")
            window.destroy()
        else:
            messagebox.showerror("Error", "Sorry, the book is not available in our library.")

        #RETURN THE BOOK
    def return_book(self, returned_book, window):
        self.cursor.execute("SELECT * FROM LibraryData WHERE book_name=?", (returned_book,))
        result = self.cursor.fetchone()
        if result is not None:
            self.books.append(returned_book)
            self.cursor.execute("DELETE FROM LibraryData WHERE book_name=?", (returned_book,))
            self.conn.commit()
            messagebox.showinfo("Success", "You have returned the book. Thank you!")
            window.destroy()
        else:
            messagebox.showerror("Error", "Sorry, we don't recognize this book. Please try again.")


        #DISPLAY THE NAME OF THE USER AND THE BOOK NAME WHICH USER HAS BORROWED
    def display_borrowed_books(self):
        borrowed_books_window = tk.Toplevel(root)
        borrowed_books_window.title("Borrowed Books")

        listbox = tk.Listbox(borrowed_books_window, font=("Arial", 14))
        self.cursor.execute("SELECT * FROM LibraryData")
        for row in self.cursor.fetchall():
            listbox.insert(tk.END, f"Book: {row[0]}, Borrower: {row[1]}")
        listbox.pack(pady=10)

        ok_button = tk.Button(borrowed_books_window, text="OK", command=borrowed_books_window.destroy, font=("Arial", 14))
        ok_button.pack(pady=10)

library = Library('libraryDatabasemain.db')


#CENTERING THE OPTION BOX WHICH APPEARS 
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# TO MAKE ALL THE OPTIONS OF EQUAL SIZE 
button_texts = ["Issue a book", "Return a book", "List available books", "Exit"]
max_length = max(len(text) for text in button_texts)


#ALL THE OPTIONS AVAILABLE FOR THE STUDENTS AND THEIR STYLING
def student():
    
    student_window = tk.Toplevel(root)
    student_window.title("Student Options")
    option_label = tk.Label(student_window, text="What would you like to do today?", font=("Pacifico", 16))
    option_label.pack(pady=15)
    
    issue_button = tk.Button(student_window, text="Issue a book", command=issue_book, font=("Courier", 14), width=max_length)
    issue_button.pack(pady=15)

    return_button = tk.Button(student_window, text="Return a book", command=return_book, font=("Courier", 14), width=max_length)
    return_button.pack(pady=15)

    list_button = tk.Button(student_window, text="List available books", command=library.display_books, font=("Courier", 14), width=max_length)
    list_button.pack(pady=15)

    exit_button = tk.Button(student_window, text="Exit", command=root.destroy, font=("Courier", 14), width=max_length)
    exit_button.pack(pady=15)

    student_window.update_idletasks() 
    center_window(student_window) 


#ALL THE OPTIONS AVAILABLE FOR THE TEACHER AND THEIR STYLING
def teacher():
    password = simpledialog.askstring("Password", "Please enter your password:", show='*')
    if password != 'TECHTITANS':
        messagebox.showerror("Error", "Sorry, that's not the correct password. ")
        return

    teacher_window = tk.Toplevel(root)
    teacher_window.title("Teacher Options")
    option_label = tk.Label(teacher_window, text="Greetings! What would you like to do today?", font=("Pacifico", 16))
    option_label.pack(pady=20)


    add_button = tk.Button(teacher_window, text="Add a book", command=add_book, font=("Courier", 14), width=max_length)
    add_button.pack(pady=15)

    remove_button = tk.Button(teacher_window, text="Remove a book", command=remove_book, font=("Courier", 14), width=max_length)
    remove_button.pack(pady=15)

    view_button = tk.Button(teacher_window, text="View issued books", command=view_issued_books, font=("Courier", 14), width=max_length)
    view_button.pack(pady=15)

    issue_button = tk.Button(teacher_window, text="Issue a book", command=issue_book, font=("Courier", 14), width=max_length)
    issue_button.pack(pady=15)

    return_button = tk.Button(teacher_window, text="Return a book", command=return_book, font=("Courier", 14), width=max_length)
    return_button.pack(pady=15)

    list_button = tk.Button(teacher_window, text="List available books", command=library.display_books, font=("Courier", 14), width=max_length)
    list_button.pack(pady=15)

    exit_button = tk.Button(teacher_window, text="Exit", command=root.destroy, font=("Courier", 14), width=max_length)
    exit_button.pack(pady=15)

    teacher_window.update_idletasks() 
    center_window(teacher_window)  

def issue_book():
    issue_window = tk.Toplevel(root)
    issue_window.title("Issue a Book")

    listbox = tk.Listbox(issue_window, font=("Arial", 14))
    for book in library.books:
        listbox.insert(tk.END, book)
    listbox.pack(pady=10)

    issue_button = tk.Button(issue_window, text="Issue Selected Book", command=lambda: library.lend_book(listbox.curselection()[0] + 1, simpledialog.askstring("Issue Book", "Enter your name:"), issue_window), font=("Courier", 14), width=max_length)
    issue_button.pack(pady=10)

def return_book():
    return_window = tk.Toplevel(root)
    return_window.title("Return a Book")

    book_name_entry = tk.Entry(return_window, font=("Arial", 14))
    book_name_entry.pack(pady=10)

    return_button = tk.Button(return_window, text="Return Entered Book", command=lambda: library.return_book(book_name_entry.get(), return_window), font=("Courier", 14), width=max_length)
    return_button.pack(pady=10)

    cancel_button = tk.Button(return_window, text="Cancel", command=return_window.destroy, font=("Courier", 14), width=max_length)
    cancel_button.pack(pady=10)

def add_book():
    add_window = tk.Toplevel(root)
    add_window.title("Add a Book")

    book_name_entry = tk.Entry(add_window, font=("Arial", 14))
    book_name_entry.pack(pady=10)

    add_button = tk.Button(add_window, text="Add Entered Book", command=lambda: library.add_book(book_name_entry.get(), add_window), font=("Courier", 14), width=max_length)
    add_button.pack(pady=10)

    cancel_button = tk.Button(add_window, text="Cancel", command=add_window.destroy, font=("Courier", 14), width=max_length)
    cancel_button.pack(pady=10)

def remove_book():
    remove_window = tk.Toplevel(root)
    remove_window.title("Remove a Book")

    listbox = tk.Listbox(remove_window, font=("Arial", 14))
    for i, book in enumerate(library.books, 1):
        listbox.insert(tk.END, f"{i}. {book}")
    listbox.pack(pady=10)

    remove_button = tk.Button(remove_window, text="Remove Selected Book", command=lambda: library.remove_book(listbox.curselection()[0] + 1, remove_window), font=("Courier", 14), width=max_length)
    remove_button.pack(pady=10)

    cancel_button = tk.Button(remove_window, text="Cancel", command=remove_window.destroy, font=("Courier", 14), width=max_length)
    cancel_button.pack(pady=10)

def view_issued_books():
    library.display_borrowed_books()


# MAIN PAGE LAYOUT CODE
root = tk.Tk()
root.title("Library Management System")

welcome_label = tk.Label(root, text="WELCOME TO OUR LIBRARY MANAGEMENT SYSTEM", font=("Helvetica CE Cond", 40))

welcome_label.pack(pady=30)

user_type_label = tk.Label(root, text="Are you a student or a teacher?", font=("Kaushan Script", 22))
user_type_label.pack(pady=50)


button_frame = tk.Frame(root)
button_frame.pack(pady=10)

student_button = tk.Button(button_frame, text="STUDENT", command=student, font=("Courier", 14), width=max_length)
student_button.pack(side="left", padx=20)

teacher_button = tk.Button(button_frame, text="TEACHER", command=teacher, font=("Courier", 14), width=max_length)
teacher_button.pack(side="right", padx=10)

description_label = tk.Label(root, text="Welcome to our Library Management System! This system allows students and teachers to issue and return books,view available books, and manage the library database. \n Hope you like it !!", wraplength=400,  font=("Amatic SC", 20))
description_label.pack(pady=120)


root.mainloop()
