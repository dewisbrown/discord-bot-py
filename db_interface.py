import sqlite3

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
