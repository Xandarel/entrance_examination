import sqlite3

end_day = 59 * 60 + 59
reserve = end_day
print(end_day)
min_list = list()
with sqlite3.connect('db2.sqlite') as connection:
    cursor = connection.cursor()
    cursor.execute("""
        SELECT request.date, (request.time - request.date) as astronomics
        FROM request
        ORDER BY request.date
     """)
    time = cursor.fetchall()
    count = 0
    day = time[0][0]
    for t in time:
        if t[0] != day:
            day = t[0]
            end_day = reserve
            min_list.append(count)
            count = 0
        if t[1] > end_day:
            min_list.append(count)
            count = 0
            end_day += t[1]
        if t[1] < end_day:
            count += 1
print(max(min_list))

