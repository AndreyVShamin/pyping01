#!/usr/bin/python3

"""
Add to crontab as root: */1 * * * * /home/andrey/pythonping/pyping.py

"""




from pythonping import ping
import sqlite3
import time

db = '/home/andrey/pythonping/pyping.db'
num = 15
timeout = 2000
addr=('1.2.3.4',
    'ash.ru.net',
    'ya.ru',
    'www.ru',)
naddr = len (addr)

conn = sqlite3.connect(db)
cursor = conn.cursor()


sql = """CREATE TABLE IF NOT EXISTS ping
                     (id  integer primary key,
                     addr text not null,
                     success integer not null,
                     percent integer not null,
                     minms integer not null,
                     maxms integer not null,
                     unixtime integer)
"""
cursor.execute(sql)



for a in addr:
    rl = ping (a, size=40, count=num, verbose=False)
    s = 0
    success = False
    for r in rl:
        if r.success:
            s += 1
            success = True
    percent = int(100*s/num)
    success = int(success)
    minms = int(rl.rtt_min_ms)
    maxms = int(rl.rtt_max_ms)
    ut = int(time.time())
    sql = f"INSERT INTO ping (addr,success,percent,minms,maxms,unixtime) VALUES ('{a}',{success},{percent},{minms},{maxms},{ut})"
    cursor.execute(sql)
    print (sql)
conn.commit() 


sql = f"SELECT * FROM ping ORDER BY id DESC LIMIT {naddr}"
cursor.execute(sql)
print(cursor.fetchall())

conn.close()
