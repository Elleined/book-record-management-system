from tkinter import *
import sqlite3
from tkinter import messagebox as alert

connection = sqlite3.connect('BookDB.db')
query = connection.cursor()
print("Connected Successfully! BookDB is now active!")

with connection:
    query.execute("""CREATE TABLE IF NOT EXISTS BOOK_DETAILS (
                        BOOK_ID INTEGER PRIMARY KEY,
                        BOOK_TITLE VARCHAR(20),
                        BOOK_GENRE VARCHAR(20),
                        BOOK_PRICE FLOAT(20)
                        )""")
    alert.showinfo("CREATE TABLE", "Table Created!")

def hide_button():
    insert_book_button.place_forget()
    delete_book_button.place_forget()
    read_book_button.place_forget()
    update_book_button.place_forget()


def show_button():
    insert_book_button.place(y=170, x=35, width=100, height=30)
    update_book_button.place(y=170, x=150, width=100, height=30)
    read_book_button.place(y=210, x=35, width=100, height=30)
    delete_book_button.place(y=210, x=150, width=100, height=30)
    id_entry.focus_set()


def enable_buttons():
    title_entry.config(state="normal")
    genre_entry.config(state="normal")
    price_entry.config(state="normal")
    insert_book_button.config(state="normal")
    update_book_button.config(state="normal")
    read_book_button.config(state="normal")
    delete_book_button.config(state="normal")


def disable_fields():
    id_entry.config(state="disabled")
    title_entry.config(state="disabled")
    genre_entry.config(state="disabled")
    price_entry.config(state="disabled")


def clear_fields():
    id_entry.delete(0, END)
    title_entry.delete(0, END)
    genre_entry.delete(0, END)
    price_entry.delete(0, END)
    id_entry.focus_set()


def is_blank_entry(book_title, book_genre):
    isEmptyField = bool(len(book_title) != 0 and len(book_genre) != 0)
    if isEmptyField:
        return True
    else:
        alert.showerror("UPDATE", "All fields cannot be empty")
        return False


def is_bookId_already_exist(book_id):
    query.execute("SELECT BOOK_ID FROM BOOK_DETAILS")
    bookId_column = query.fetchall()
    for existing_id in bookId_column:
        if book_id in existing_id:
            return True

def gui_closing():
    connection.close()
    print("Connection to BookDB Closed!")
    gui.destroy()

def read_book_data():
    query.execute("SELECT * FROM BOOK_DETAILS")
    book_data = query.fetchall()
    for row in book_data:
        print(row)


def update_book_data():
    def on_closing_selection_window():
        id_entry.config(state="normal")
        show_button()
        enable_buttons()
        clear_fields()
        update_selection_window.destroy()

    def update_book_entry():
        execute_update_button.place(y=170, x=100, width=100, height=30)
        id_entry.config(state="normal")
        unChecked = 0
        title_entry.config(state="disabled") if title_variable.get() == unChecked \
            else title_entry.config(state="normal")
        genre_entry.config(state="disabled") if genre_variable.get() == unChecked \
            else genre_entry.config(state="normal")
        price_entry.config(state="disabled") if price_variable.get() == unChecked \
            else price_entry.config(state="normal")
        update_selection_window.destroy()

    hide_button()
    disable_fields()

    update_selection_window = Toplevel(gui)
    update_selection_window.title("UPDATE")
    update_selection_window.geometry("200x180")
    update_selection_window.config(bg="peach puff")

    update_text_label = Label(update_selection_window, text="Select entry to update: ", bg="peach puff")
    title_variable = IntVar()
    genre_variable = IntVar()
    price_variable = IntVar()
    title_check_button = Checkbutton(update_selection_window, text="Book Title", variable=title_variable,
                                     bg="peach puff")
    genre_check_button = Checkbutton(update_selection_window, text="Book Genre", variable=genre_variable,
                                     bg="peach puff")
    brand_check_button = Checkbutton(update_selection_window, text="Book Price", variable=price_variable,
                                     bg="peach puff")
    update_button = Button(update_selection_window, text="Update Selected", command=update_book_entry,
                           bg="DodgerBlue", fg="ivory")

    update_text_label.place(y=10, x=30, width=150, height=20)
    title_check_button.place(y=40, x=10, width=150, height=20)
    genre_check_button.place(y=70, x=13, width=150, height=20)
    brand_check_button.place(y=100, x=10, width=150, height=20)
    update_button.place(y=130, x=40, width=100, height=35)
    update_selection_window.protocol("WM_DELETE_WINDOW", on_closing_selection_window)


def execute_book_update():
    show_button()
    book_id = int(id_entry.get())
    if not is_bookId_already_exist(book_id):
        execute_update_button.place_forget()
        clear_fields()
        enable_buttons()
        id_entry.config(state="normal")
        alert.showerror("UPDATE", "ProductId didn't exist!")
        return

    book_title = str(title_entry.get()).strip()
    book_genre = str(genre_entry.get()).strip()
    book_price = str(price_entry.get()).strip()

    query.execute("SELECT * FROM BOOK_DETAILS WHERE BOOK_ID=?", (book_id,))
    selectedEntry = query.fetchone()
    blank = 0
    if len(book_title) == blank:
        book_title = selectedEntry[1]  # Book Title
    if len(book_genre) == blank:
        book_genre = selectedEntry[2]  # Book Genre
    if len(book_price) == blank:
        book_price = selectedEntry[3]  # Book Price
    try:
        with connection:
            query.execute("""UPDATE BOOK_DETAILS SET
                        BOOK_TITLE=?,
                        BOOK_GENRE=?,
                        BOOK_PRICE=? WHERE BOOK_ID=?""", (book_title, book_genre, book_price, book_id))
            execute_update_button.place_forget()
            clear_fields()
            enable_buttons()
            id_entry.config(state="normal")
            alert.showinfo("UPDATE", "Updated Successfully")
    except sqlite3.DatabaseError:
        print(sqlite3.DatabaseError)


def delete_book_data():
    hide_button()
    title_entry.config(state="disabled")
    genre_entry.config(state="disabled")
    price_entry.config(state="disabled")
    execute_delete_button.place(y=170, x=100, width=100, height=30)


def execute_book_delete():
    try:
        book_id = int(id_entry.get())
        if not is_bookId_already_exist(book_id):
            clear_fields()
            execute_delete_button.place_forget()
            enable_buttons()
            show_button()
            alert.showerror("DELETE", "BookId didn't exist!")
            return
        with connection:
            query.execute("DELETE FROM BOOK_DETAILS WHERE BOOK_ID=?", (book_id,))
            clear_fields()
            execute_delete_button.place_forget()
            enable_buttons()
            show_button()
            alert.showinfo("DELETE", "Deleted Successfully!")
    except ValueError:
        print("Error Catch! Dont Worry")


def insert_book_data():
    book_title = str(title_entry.get()).strip()
    book_genre = str(genre_entry.get()).strip()
    try:
        book_id = int(id_entry.get())
        book_price = float(price_entry.get())
        if not is_blank_entry(book_title, book_genre):
            return
        if is_bookId_already_exist(book_id):
            alert.showerror("INSERT", "BookId already exist!")
            clear_fields()
            return
        with connection:
            query.execute("""INSERT INTO BOOK_DETAILS VALUES (?, ?, ?, ?)""",
                          (book_id, book_title, book_genre, book_price))
            clear_fields()
            alert.showinfo("SAVE", "Inserted Successfully")
    except ValueError:
        alert.showerror("INSERT", "Book Id or Price must be a number!")
        clear_fields()


gui = Tk()
gui.title("GUI with Database")
gui.geometry("300x250")
gui.resizable(False, False)
gui.config(bg="peach puff")

book_label = Label(gui, text="Book Information", bg="peach puff")
id_label = Label(gui, text="Book Id", bg="peach puff")
id_entry = Entry(gui, borderwidth=3)
title_label = Label(gui, text="Book Title", bg="peach puff")
title_entry = Entry(gui, borderwidth=3)
genre_label = Label(gui, text="Book Genre", bg="peach puff")
genre_entry = Entry(gui, borderwidth=3)
price_label = Label(gui, text="Book Price", bg="peach puff")
price_entry = Entry(gui, borderwidth=3)
read_book_button = Button(gui, text="READ", command=read_book_data, bg="purple1", fg="ivory")
update_book_button = Button(gui, text="UPDATE", command=update_book_data, bg="DodgerBlue", fg="ivory")
delete_book_button = Button(gui, text="DELETE", command=delete_book_data, bg="red3", fg="ivory")
insert_book_button = Button(gui, text="INSERT", command=insert_book_data, bg="gray31", fg="ivory")
execute_update_button = Button(gui, text="UPDATE", command=execute_book_update, bg="DodgerBlue", fg="ivory")
execute_delete_button = Button(gui, text="DELETE", command=execute_book_delete, bg="red3", fg="ivory")

book_label.place(y=10, x=100, width=100, height=30)
id_label.place(y=40, x=30, width=60, height=20)
id_entry.place(y=40, x=130, width=120, height=20)
title_label.place(y=70, x=35, width=60, height=20)
title_entry.place(y=70, x=130, width=120, height=20)
genre_label.place(y=100, x=37, width=60, height=20)
genre_entry.place(y=100, x=130, width=120, height=20)
price_label.place(y=130, x=35, width=60, height=20)
price_entry.place(y=130, x=130, width=120, height=20)

insert_book_button.place(y=170, x=35, width=100, height=30)
update_book_button.place(y=170, x=150, width=100, height=30)
read_book_button.place(y=210, x=35, width=100, height=30)
delete_book_button.place(y=210, x=150, width=100, height=30)

gui.protocol("WM_DELETE_WINDOW", gui_closing)
gui.mainloop()
