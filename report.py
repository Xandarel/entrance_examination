import sqlite3

def frozen_fish_time():
    time_dict = {'night': 0, 'morning': 0, 'day': 0, 'evening': 0}
    night = 6 * 3600
    morning = 12 * 3600
    day = 18 * 3600


    with sqlite3.connect('db2.sqlite') as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT request.time-request.date as dayTime
            FROM request
            WHERE request.url like '%frozen_fish%'
        """)
        time_SQL = cursor.fetchall()
        for t in time_SQL:
            element = t[0]
            if element < night:
                time_dict['night'] += 1
            elif element < morning:
                time_dict['morning'] += 1
            elif element < day:
                time_dict['day'] += 1
            else:
                time_dict['evening'] += 1
        main_list = list(time_dict.items())
        main_list.sort(key=lambda i: i[1], reverse=True)
        return  main_list[0][0]




