import sqlite3
import csv

# Connect to sqlite database (make new if doesn't exist)
conn = sqlite3.connect('data/points.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table to store user inventory
cursor.execute('''CREATE TABLE IF NOT EXISTS shop (
                    item_name TEXT,
                    value INTEGER,
                    rarity TEXT
                )''')

# Input all items from shop data into db
with open('./shop.csv', 'r', encoding='utf-8', newline='') as file:
    reader = csv.DictReader(file)

    for item in reader:
        item_name = item['item_name']
        rarity = item['rarity']
        value = item['value']

        cursor.execute('''INSERT INTO shop 
                       (item_name, value, rarity) 
                       VALUES (?, ?, ?)''',
                       (item_name, value, rarity,))

# Commit and close the connection
conn.commit()
conn.close()
