import sqlite3

with sqlite3.connect('db2.sqlite') as connection:
    cursor = connection.cursor()
    cursor.executescript("""
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS users (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    ip      TEXT NOT NULL,
    country TEXT NOT NULL
    );
    
    CREATE TABLE request (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    url     TEXT NOT NULL,
    date    INTEGER NOT NULL,
    time    INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
    );
    
    CREATE TABLE category (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL
    );
    
    CREATE TABLE product (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE
    );
    
    CREATE TABLE shopping_cart (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    cart_id     INTEGER NOT NULL,
    pay_status  INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
    );
    
    CREATE TABLE product_list (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id       INTEGER NOT NULL,
    shopping_cart_id INTEGER NOT NULL,
    amount           INTEGER NOT NULL,
    FOREIGN KEY (shopping_cart_id) REFERENCES shopping_cart(cart_id),
    FOREIGN KEY (product_id) REFERENCES product(id) 
    );
    """)
