import sqlite3

conn = sqlite3.connect('travel.db')
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(trips)")
columns = cursor.fetchall()
for col in columns:
    print(col)


