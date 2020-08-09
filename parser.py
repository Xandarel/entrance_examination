import sqlite3
from geoip import geolite2
import datetime
import time as t


with open('logs.txt') as logs:
    none = 0
    for s in logs:
        text = s.split()

        ip = text[6]
        match = geolite2.lookup(text[6])
        if match is not None:
            country = match.country
            if country is None:
                country = 'NaN'

        url = text[-1]
        url_path = url.replace('https://all_to_the_bottom.com/', '')
        url_main = url_path.split('/')

        cart_id = None
        category_name = None
        product_name = None
        add_dict = None
        pay_dict = None

        if len(url_main) == 2:  # Только категория или сообщение об успешной оплате
            if 'success_pay' in url_main[0]:
                cart_id = int(url_main[0].replace('success_pay_', ''))
            else:
                category_name = url_main[0]
        elif len(url_main) == 3:  # Пользоватеь зашел в продукт
            category_name = url_main[0]
            product_name = url_main[1]
        elif len(url_main) == 1:  # Или он добавил в карзину, или оплачивает
            # Добавляет в карзину
            if 'cart?' in url_main[0]:
                add_cart = url_main[0].replace('cart?', '')
                add_dict = {sub.split("=")[0]: int(sub.split("=")[1]) for sub in add_cart[:].split('&')}
            elif 'pay?' in url_main[0]:  # оплачивает
                pay_cart = url_main[0].replace('pay?', '')
                pay_dict = {sub.split("=")[0]: int(sub.split("=")[1]) for sub in add_cart[:-1].split('&')}

        time = text[3]
        date = t.mktime(datetime.datetime.strptime(text[2], "%Y-%m-%d").timetuple())
        h, m, s = map(int, time.split(':'))
        totalSeconds = (int(h) * 3600 + int(m) * 60 + int(s)) + date

        with sqlite3.connect('db2.sqlite') as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id
                FROM users
                WHERE ip = ?
            """, (ip,))
            user_id = cursor.fetchone()

            if user_id:
                user_id = int(user_id[0])

            if user_id is None:
                cursor.execute("""
                    INSERT INTO users 
                        (ip, country)
                    VALUES (?, ?)
                """, (ip, country))
                connection.commit()
                user_id = cursor.lastrowid

            if category_name is not None:
                cursor.execute(""" 
                    SELECT id
                    FROM category
                    WHERE name = ?
                """, (category_name,))

                category_id = cursor.fetchone()

                if category_id:
                    category_id = int(category_id[0])

                if category_id is None:
                    cursor.execute("""
                        INSERT INTO category 
                            (name)
                        VALUES (?)
                    """, (category_name,))

                    connection.commit()
                    category_id = cursor.lastrowid

                if product_name:
                    cursor.execute(""" 
                        SELECT id
                        FROM product
                        WHERE name = ?
                    """, (product_name,))
                    product_id = cursor.fetchone()

                    if product_id:
                        product_id = int(product_id[0])

                    if not product_id:
                        cursor.execute("""
                            INSERT INTO product
                                (name, category_id)
                            VALUES (?,?)
                        """, (product_name, category_id))
                        connection.commit()
                        product_id = cursor.lastrowid

            if add_dict:
                cursor.execute("""
                    SELECT id
                    FROM shopping_cart
                    WHERE user_id = ? AND cart_id = ?
                """, (user_id, add_dict['cart_id']))

                sql_cart_id = cursor.fetchone()
                if sql_cart_id:
                    sql_cart_id = int(sql_cart_id[0])

                if not sql_cart_id:
                    cursor.execute("""
                        INSERT INTO shopping_cart
                            (user_id, cart_id, pay_status)
                        VALUES (?, ?, ?)
                    """, (user_id, add_dict['cart_id'], 0))
                    connection.commit()
                    sql_cart_id = cursor.lastrowid

                cursor.execute("""
                    SELECT url, request.time
                    FROM request, users, shopping_cart
                    WHERE shopping_cart.cart_id = ? 
                        AND shopping_cart.user_id = users.id 
                        AND users.id = request.user_id
                    ORDER BY request.time DESC
                """, (add_dict['cart_id'],))

                product_url = cursor.fetchone()
                print(product_url)
                product_url_split = product_url[0].split('/')
                product_name = product_url_split[-2]
                print(product_name)
                cursor.execute("""
                    SELECT id 
                    FROM product
                    WHERE name =?
                """, (product_name,))

                product_id = int(cursor.fetchone()[0])
                print(product_id)
                cursor.execute("""
                    INSERT INTO product_list
                        (product_id, shopping_cart_id, amount)
                    VALUES (?, ?, ?)
                """, (product_id, add_dict['cart_id'], add_dict['amount']))

            if cart_id:
                cursor.execute("""
                    SELECT id
                    FROM shopping_cart
                    WHERE cart_id = ? 
                """, (cart_id,))
                update_cart_id = cursor.fetchone()

                if update_cart_id:
                    update_cart_id = int(update_cart_id[0])
                    cursor.execute("""
                        UPDATE shopping_cart
                        SET pay_status = 1
                        WHERE id = ?
                    """, (update_cart_id,))
                    connection.commit()

            if not 'success_pay_' in url:
                cursor.execute("""
                    INSERT INTO request
                        (url, date, time, user_id)
                    VALUES (?, ?, ?, ?)
                """, (url, date, totalSeconds, user_id))
                connection.commit()

            cart_id = None
            category_name = None
            buf_product_name = product_name
            add_dict = None
            pay_dict = None

