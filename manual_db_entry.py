import sqlite3
import datetime

conn = sqlite3.connect('data/points.db')
cursor = conn.cursor()

# input variables in execute function
cursor.execute('INSERT INTO points (user_id, points, last_awarded_at, level, user_name) VALUES (?, ?, ?, ?, ?)', ())
conn.commit()

conn.close()