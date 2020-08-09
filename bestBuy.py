import sqlite3

def buy():
    main_dict = dict()
    with sqlite3.connect('db2.sqlite') as connection:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT product.id
        FROM product, category
        WHERE category.name = 'semi_manufactures' and category.id = category_id
        """)
        products = cursor.fetchall()
        for product in products:
            cursor.execute("""
                SELECT shopping_cart_id
                FROM product_list
                WHERE product_id = ? 
            """, (product[0],))
            shopping_carts = cursor.fetchall()

            for shopping_cart in shopping_carts:
                cursor.execute("""
                    SELECT product_list.product_id
                    FROM product_list
                    WHERE product_list.shopping_cart_id = ?
                    GROUP BY product_list.product_id
                """, (shopping_cart[0],))
                buy_products = cursor.fetchall()
                for buy_product in buy_products:
                    cursor.execute("""
                    SELECT product.category_id
                    FROM product
                    WHERE product.id = ?
                    """, (buy_product[0],))
                    categories = cursor.fetchall()
                    for category in categories:
                        if category[0] in main_dict.keys():
                            main_dict[category[0]] += 1
                        else:
                            main_dict[category[0]] = 1

    main_list = list(main_dict.items())
    main_list.sort(key=lambda i: i[1], reverse=True)
    with sqlite3.connect('db2.sqlite') as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT category.name
            FROM category
            WHERE category.id = ?
        """, (main_list[1][0],))
        ans = cursor.fetchone()
    return ans[0]


