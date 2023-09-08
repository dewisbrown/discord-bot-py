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
                    user_name TEXT
                )''')

# Create a table to store user inventory
cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                    user_id INTEGER,
                    item_name TEXT,
                    value INTEGER,
                    rarity TEXT,
                    purchase_date TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES points (user_id)
                )''')

# Commit and close the connection
conn.commit()
conn.close()