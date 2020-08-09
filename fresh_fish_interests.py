import sqlite3


def fish_interests():
    main_dict = dict()
    with sqlite3.connect('db2.sqlite') as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT request.user_id, count(request.user_id)
            FROM request
            WHERE request.url like '%fresh_fish%'
            GROUP BY request.user_id
        """)
        users_data = cursor.fetchall()
        for user_data in users_data:
            cursor.execute("""
            SELECT users.country
            FROM users
            WHERE users.id = ?
            """, (user_data[0],))
            country = cursor.fetchone()
            if country[0] in main_dict.keys():
                main_dict[country[0]] += user_data[1]
            else:
                main_dict[country[0]] = user_data[1]

    main_list = list(main_dict.items())
    main_list.sort(key=lambda i: i[1], reverse=True)
    return main_list[:6]
