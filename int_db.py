import sqlite3

conn = sqlite3.connect('databass.db')

with open('db.sql') as f:
    conn.executescript(f.read())

# 创建一个执行句柄，用来执行后面的语句
cur = conn.cursor()

# 插入两条文字
cur.execute("INSERT INTO post (title, conten) VALUES (?, ?)"
            ('你好', 'world')
            )



conn.commit()
conn.close()