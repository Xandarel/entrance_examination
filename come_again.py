import sqlite3


def newBuy():
    with sqlite3.connect('db2.sqlite') as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT count(shopping_cart.id), shopping_cart.user_id
            FROM shopping_cart
            WHERE shopping_cart.pay_status = 1
            GROUP BY shopping_cart.user_id
            HAVING count(shopping_cart.id) > 1
            ORDER BY count(shopping_cart.id) DESC
        """)
        ans = cursor.fetchall()
    return len(ans)
