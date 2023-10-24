# Library management system
"""
Made by:  Rohit Kumar Yadav
Date: 24 oct 2023
"""

import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import security 

# ---------------------------------------------------------------- Main Program ----------------------------------------------------------------

# Function to retrieve and display all books
def view_all_books():
    # Connect to the SQLite database
    conn = sqlite3.connect('Database_collection.db')
    cursor = conn.cursor()

    # Execute an SQL query to select all data from the 'books' table
    cursor.execute("SELECT * FROM books")

    # Fetch all the data
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Create a new window to display the data
    display_window = Tk()
    display_window.title("List of Books")

    # Create a treeview widget to display the data in a table format
    tree = ttk.Treeview(display_window, columns=("S_No", "Book Name", "Author Name", "Quantity", "Date Added"), show="headings")
    tree.heading("S_No", text="S_No")
    tree.heading("Book Name", text="Book Name")
    tree.heading("Author Name", text="Author Name")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Date Added", text="Date Added")

    tree.pack()

    # Insert the data into the treeview
    for row in data:
        tree.insert("", "end", values=row)

# Create a connection to the database
conn = sqlite3.connect('Database_collection.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create the 'books' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        S_no INTEGER PRIMARY KEY AUTOINCREMENT,
        book_name TEXT NOT NULL,
        author_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        date_added DATE NOT NULL
    )
''')

# Create a 'book_issues' table to track book issuances
cursor.execute('''
    CREATE TABLE IF NOT EXISTS book_issues (
        issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER NOT NULL,
        user_name TEXT NOT NULL,
        roll_no TEXT NOT NULL,
        email TEXT NOT NULL,
        issue_date DATE NOT NULL,
        FOREIGN KEY (book_id) REFERENCES books(S_no)
    )
''')

# Create a GUI window
window = Tk()
window.title("Digital Library")
window.iconbitmap("book.ico")

# Set the window size to full screen
window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")

# Set the background color
window.configure(bg="lightblue")

# Create a style object
style = ttk.Style()

# Function to get the next S_no for a new book
def get_next_sno():
    cursor.execute('SELECT MAX(S_no) FROM books')
    last_sno = cursor.fetchone()[0]
    return 1 if last_sno is None else last_sno + 1

# Function to add a book to the database
def add_book():
    # Get the values entered in the entry boxes and date widget
    book_name = book_name_entry.get()
    author_name = author_name_entry.get()
    quantity = quantity_entry.get()
    date_added = date_added_entry.get()
    sno = get_next_sno()

    # Insert the book into the database
    cursor.execute('''
        INSERT INTO books (S_no, book_name, author_name, quantity, date_added)
        VALUES (?, ?, ?, ?, ?)''', (sno, book_name, author_name, quantity, date_added))

    # Commit the changes to the database
    conn.commit()

    # Clear the entry boxes and reset the DateEntry widget
    book_name_entry.delete(0, END)
    author_name_entry.delete(0, END)
    quantity_entry.delete(0, END)
    date_added_entry.delete(0, END)

    # Display a success message
    success_label.config(text="Book successfully added!")

# Function to issue a book
def issue_book():
    # Get the values entered for book issuance
    selected_book = book_combobox.get()
    user_name = user_name_entry.get()
    roll_no = roll_no_entry.get()
    email = email_entry.get()
    issue_date = issue_date_entry.get()

    # Get the book_id (S_no) from the selected book name
    cursor.execute("SELECT S_no FROM books WHERE book_name = ?", (selected_book,))
    book_id = cursor.fetchone()[0]

    # Insert the book issuance into the 'book_issues' table
    cursor.execute('''
        INSERT INTO book_issues (book_id, user_name, roll_no, email, issue_date)
        VALUES (?, ?, ?, ?, ?)''', (book_id, user_name, roll_no, email, issue_date))

    # Commit the changes to the database
    conn.commit()

    # Clear the entry boxes and reset the DateEntry widget
    user_name_entry.delete(0, END)
    roll_no_entry.delete(0, END)
    email_entry.delete(0, END)
    issue_date_entry.delete(0, END)

    # Display a success message
    success_label.config(text="Book issued successfully!")

# Function to delete a book
def delete_book():
    # Get the book name to be deleted
    selected_book = delete_book_combobox.get()

    if not selected_book:
        success_label.config(text="Please select a book to delete.")
        return

    # Get the S_no (book_id) from the selected book name
    cursor.execute("SELECT S_no FROM books WHERE book_name = ?", (selected_book,))
    book_row = cursor.fetchone()

    if book_row is None:
        success_label.config(text="Book not found. Please select a valid book.")
        return

    book_id = book_row[0]

    # Delete the book from the 'books' table
    cursor.execute("DELETE FROM books WHERE S_no = ?", (book_id))
    
    # Commit the changes to the database
    conn.commit()

    # Clear the delete book combobox and display a success message
    delete_book_combobox.set("")
    success_label.config(text="Book successfully deleted!")

# Function to view book issuance history
def view_issuance_history():
    history_window = Tk()
    history_window.title("Issuance History")
    
    # Create a treeview widget to display the data in a table format
    tree = ttk.Treeview(history_window, columns=("Issue ID", "Book Name", "User Name", "Roll No", "Email", "Issue Date"), show="headings")
    tree.heading("Issue ID", text="Issue ID")
    tree.heading("Book Name", text="Book Name")
    tree.heading("User Name", text="User Name")
    tree.heading("Roll No", text="Roll No")
    tree.heading("Email", text="Email")
    tree.heading("Issue Date", text="Issue Date")

    tree.pack()
    
    # Fetch and display book issuance history
    cursor.execute('''
        SELECT book_issues.issue_id, books.book_name, book_issues.user_name, book_issues.roll_no, book_issues.email, book_issues.issue_date
        FROM book_issues
        INNER JOIN books ON book_issues.book_id = books.S_no
    ''')
    data = cursor.fetchall()
    
    for row in data:
        tree.insert("", "end", values=row)

# Create labels and entry boxes for adding a book
add_book_label = Label(window, text="Add a Book", font=("Helvetica", 16), bg="lightblue")
add_book_label.grid(row=0, column=0, padx=10, pady=10)

book_name_label = Label(window, text="Book Name", font=("Helvetica", 12), bg="lightblue")
book_name_label.grid(row=1, column=0, padx=10, pady=10)
book_name_entry = Entry(window)
book_name_entry.grid(row=1, column=1, padx=10, pady=10)

author_name_label = Label(window, text="Author Name", font=("Helvetica", 12), bg="lightblue")
author_name_label.grid(row=2, column=0, padx=10, pady=10)
author_name_entry = Entry(window)
author_name_entry.grid(row=2, column=1, padx=10, pady=10)

quantity_label = Label(window, text="Quantity", font=("Helvetica", 12), bg="lightblue")
quantity_label.grid(row=3, column=0, padx=10, pady=10)
quantity_entry = Entry(window)
quantity_entry.grid(row=3, column=1, padx=10, pady=10)

date_added_label = Label(window, text="Date Added", font=("Helvetica", 12), bg="lightblue")
date_added_label.grid(row=4, column=0, padx=10, pady=10)
date_added_entry = DateEntry(window)
date_added_entry.grid(row=4, column=1, padx=10, pady=10)

# Create a button to add a book
add_button = Button(window, text="Add Book", command=add_book, font=("Helvetica", 12), bg="lightgreen", padx=10)
add_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Create a label to display the success message
success_label = Label(window, text="")
success_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Create labels and entry boxes for issuing a book
issue_book_label = Label(window, text="Issue a Book", font=("Helvetica", 16), bg="lightblue")
issue_book_label.grid(row=0, column=2, padx=10, pady=10)

book_label = Label(window, text="Select Book", font=("Helvetica", 12), bg="lightblue")
book_label.grid(row=1, column=2, padx=10, pady=10)
books = [row[1] for row in cursor.execute("SELECT * FROM books").fetchall()]
book_combobox = ttk.Combobox(window, values=books)
book_combobox.grid(row=1, column=3, padx=10, pady=10)

user_name_label = Label(window, text="User Name", font=("Helvetica", 12), bg="lightblue")
user_name_label.grid(row=2, column=2, padx=10, pady=10)
user_name_entry = Entry(window)
user_name_entry.grid(row=2, column=3, padx=10, pady=10)

roll_no_label = Label(window, text="Roll No", font=("Helvetica", 12), bg="lightblue")
roll_no_label.grid(row=3, column=2, padx=10, pady=10)
roll_no_entry = Entry(window)
roll_no_entry.grid(row=3, column=3, padx=10, pady=10)

email_label = Label(window, text="Email", font=("Helvetica", 12), bg="lightblue")
email_label.grid(row=4, column=2, padx=10, pady=10)
email_entry = Entry(window)
email_entry.grid(row=4, column=3, padx=10, pady=10)

issue_date_label = Label(window, text="Date of Issue", font=("Helvetica", 12), bg="lightblue")
issue_date_label.grid(row=5, column=2, padx=10, pady=10)
issue_date_entry = DateEntry(window)
issue_date_entry.grid(row=5, column=3, padx=10, pady=10)

# Create a button to issue a book
issue_button = Button(window, text="Issue Book", command=issue_book, font=("Helvetica", 12), bg="lightgreen", padx=10)
issue_button.grid(row=6, column=2, columnspan=2, padx=10, pady=10)

# Create a button to view book issuance history
history_button = Button(window, text="View Issuance History", command=view_issuance_history, font=("Helvetica", 12), bg="pink", padx=10)
history_button.grid(row=7, column=0, columnspan=4, padx=10, pady=10)

# Create a button to view all books
view_all_books_button = Button(window, text="View All Books", command=view_all_books , font=("Helvetica", 12), bg="pink", padx=10)
view_all_books_button.grid(row=7, column=3, columnspan=4, padx=10, pady=10)

# Create labels and a button for deleting a book
delete_book_label = Label(window, text="Delete a Book")
delete_book_label.grid(row=15, column=1, padx=10, pady=10)

delete_book_label = Label(window, text="Select Book")
delete_book_label.grid(row=16, column=0, padx=10, pady=10)
delete_book_combobox = ttk.Combobox(window, values=books)
delete_book_combobox.grid(row=16, column=1, padx=10, pady=10)
delete_button = Button(window, text="Delete Book", command=delete_book , font=("Helvetica", 12), bg="red", padx=10)
delete_button.grid(row=17, column=1, padx=10, pady=10)

# Start the main GUI loop
window.mainloop()

# Close the connection
conn.close()
