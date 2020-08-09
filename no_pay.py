import sqlite3

def noMoney():
    with sqlite3.connect('db2.sqlite') as connection:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT count(pay_status)
        FROM shopping_cart
        WHERE pay_status=0
        """)
        ans = cursor.fetchone()
    return ans[0]
