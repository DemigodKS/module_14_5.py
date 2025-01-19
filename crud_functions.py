import sqlite3

def initiate_db():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute(" DROP TABLE IF EXISTS Products")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL
    );
    ''')
    i = 1
    #ЗАПОЛНЯЕМ 10-Ю ЗАПИСЯМИ
    for i in range(1, 5):
        cursor.execute(" INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
            (f"Продукт {i}", f"Описание {i}", f"{i*100}"))

    connection.commit()
    connection.close()
initiate_db()

def get_all_products():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    product = cursor.fetchall()
    connection.commit()
    connection.close()
    return product


def initiate_db_2():
    con = sqlite3.connect("users.db")
    cursor1 = con.cursor()

    cursor1.execute("DROP TABLE IF EXISTS Users")
    cursor1.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    );
    ''')

    con.commit()
    con.close()
initiate_db_2()
def add_user(username, email, age):
    con = sqlite3.connect("users.db")
    cursor1 = con.cursor()
    cursor1.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (username, email, age, 1000))

    con.commit()

def is_included(username):
    con = sqlite3.connect("users.db")
    cursor1 = con.cursor()
    cursor1.execute('SELECT * FROM Users')
    all_users = cursor1.fetchall()
    for user in all_users:
        if username == user[1]:
            return True
    return False






