import sqlite3
from tkinter import messagebox as alert

connection = sqlite3.connect('BookDB.db')
query = connection.cursor()
print("Connected Successfully! BookDB is now active!")

def create_book_table():
    with connection:
        query.execute("""CREATE TABLE IF NOT EXISTS BOOK_DETAILS (
                            BOOK_ID INTEGER PRIMARY KEY,
                            BOOK_TITLE VARCHAR(20),
                            BOOK_GENRE VARCHAR(20),
                            BOOK_PRICE FLOAT(20)
                            )""")
        alert.showinfo("CREATE TABLE", "Table Created!")

create_book_table()