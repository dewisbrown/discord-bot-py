'''Using to minimize re-written code in cog files. 
Provides a way to input and retreive data from database.'''

import sqlite3

def get_user_id(user_id):
    '''Checks if user is in points table already.'''
    # Connect to the database
    conn = sqlite3.connect('data/points.db')
    cursor = conn.cursor()

    # Check if the user is already registered
    cursor.execute('SELECT user_id FROM points WHERE user_id = ?', (user_id,))
    return cursor.fetchone()


def add_user(user_id, last_awarded_at, user_name):
    '''Adds user to points table.'''
    # Connect to the database
    conn = sqlite3.connect('data/points.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO points (
                   user_id, points, last_awarded_at, 
                   level, user_name) VALUES (?, ?, ?, ?, ?)''', 
                   (user_id, 100, last_awarded_at, 1, user_name))
    conn.commit()


def get_points(user_id):
    '''Returns the points of the user from the db.'''
    # Connect to the database
    conn = sqlite3.connect('data/points.db')
    cursor = conn.cursor()

    # Check the last awarded timestamp for the user
    cursor.execute('SELECT points FROM points WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return None


def get_last_awarded_at(user_id):
    '''Returns timestamp of last points redemption.'''
    # Connect to the database
    conn = sqlite3.connect('data/points.db')
    cursor = conn.cursor()

    # Check the last awarded timestamp for the user
    cursor.execute('SELECT last_awarded_at FROM points WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return None


def set_points(user_id, points, current_time):
    '''Updates user points in db.'''
    # Connect to the database
    conn = sqlite3.connect('data/points.db')
    cursor = conn.cursor()

    # Check the last awarded timestamp for the user
    cursor.execute('UPDATE points SET points = ?, last_awarded_at = ? WHERE user_id = ?', (points, current_time, user_id))
    conn.commit()
    conn.close()


def get_level(user_id):
    '''Returns user level from db.'''
    # Connect to the database
    conn = sqlite3.connect('data/points.db')
    cursor = conn.cursor()

    cursor.execute('SELECT level FROM points WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return None


def set_level(user_id, level):
    '''Sets user level in db.'''
    # Connect to the database
    conn = sqlite3.connect('data/points.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE points SET level = ? WHERE user_id = ?', (level, user_id,))
    conn.commit()
    conn.close()


def get_inventory(user_id):
    '''Returns user inventory from inventory db table.'''
    # Connect to the database
    conn = sqlite3.connect('data/points.db')
    cursor = conn.cursor()

    # Return user inventory list
    cursor.execute('''SELECT item_name, value, rarity
                        FROM inventory
                        WHERE user_id = ?''', (user_id,))
    # for item in items -> item_name = item[0], value = item[1], rarity = item[2]
    return cursor.fetchall()


def add_to_inventory(user_id, item, item_value, item_rarity, purchase_date):
    '''Addes item to user inventory.'''
    # Connect to the database
    conn = sqlite3.connect('data/points.db')
    cursor = conn.cursor()

    # Extract data from item_info and add to inventory
    cursor.execute('''INSERT INTO inventory
                   (user_id, item_name, value, rarity, purchase_date) 
                   VALUES (?, ?, ?, ?, ?)''',
                   (user_id, item, item_value, item_rarity, purchase_date))
    conn.commit()
    conn.close()
