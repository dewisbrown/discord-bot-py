import sqlite3

# Connect to sqlite database (make new if doesn't exist)
conn = sqlite3.connect('data/points.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table to store member points
cursor.execute('''CREATE TABLE IF NOT EXISTS points (
                    user_id INTEGER PRIMARY KEY,
                    points INTEGER DEFAULT 0,
                    last_awarded_at TIMESTAMP,
                    level INTEGER DEFAULT 1,
                    display_name TEXT
                )''')

# Commit and close the connection
conn.commit()
conn.close()