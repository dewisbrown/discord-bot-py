import sqlite3
import datetime
import os
from discord.ext import commands

db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'points.db')

shop = {
    'Spinning Top': 5,
    'Rusty Penny': 1,
    'Holographic Eddie Trading Card': 70,
    'Fuji Apple': 10,
    'Cool Shades': 20
}

class BattlepassCog(commands.Cog):
    '''Commands to register for battlepass, collect points, and increase tier level with points.'''
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        '''Print statment to ensure loads properly.'''
        print('Battlepass Cog loaded.')


    @commands.command()
    async def register(self, ctx):
        '''Enters user into battlepass database.'''
        user_id = ctx.author.id
        display_name = ctx.author.display_name
        registration_timestamp = datetime.datetime.now()

        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if the user is already registered
        cursor.execute('SELECT user_id FROM points WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            await ctx.send("You are already registered.")
        else:
            cursor.execute('INSERT INTO points (user_id, points, last_awarded_at, level, display_name) VALUES (?, ?, ?, ?, ?)', (user_id, 30, registration_timestamp, 1, display_name))
            conn.commit()

            message = f'Timestamp for registration: {registration_timestamp.strftime("%Y-%m-%d %I:%M %p")}\n'
            message += 'You have received 30 points for registering.'
            await ctx.send(message)
        
        conn.close()


    @commands.command()
    async def points(self, ctx):
        '''Allows user to get 10 points per hour.'''
        user_id = ctx.author.id

        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check the last awarded timestamp for the user
        cursor.execute('SELECT last_awarded_at FROM points WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            last_awarded_at_str = result[0]
            last_awarded_at = datetime.datetime.strptime(last_awarded_at_str, '%Y-%m-%d %H:%M:%S.%f')
            current_time = datetime.datetime.now()
            time_since_last_awarded = current_time - last_awarded_at
            next_redemption_time = (last_awarded_at + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %I:%M %p')

            # Check if it has been at least 24 hours
            if time_since_last_awarded.total_seconds() >= 3600: # 3600 seconds/hour
                cursor.execute('UPDATE points SET points = points + 10, last_awarded_at = ? WHERE user_id = ?', (current_time, user_id))
                conn.commit()

                await ctx.send('You\'ve been awarded 10 points!')
            else: 
                await ctx.send('Sorry, you can only claim points once an hour.\n')
            
            # Print next redemption time
            await ctx.send(f'Your next redemption time is: {next_redemption_time}')
        else:
            await ctx.send('You\'re not registered in the points system yet. Use the ```$register``` command to get started.')

        conn.close()


    @commands.command()
    async def tierup(self, ctx):
        '''Allows the user to spend points to level up.'''
        user_id = ctx.author.id

        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check the user's current level and points
        cursor.execute('SELECT level, points FROM points WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            current_level, points = result

            if points >= 40:
                cursor.execute('UPDATE points SET points = points - 40, level = level + 1 WHERE user_id = ?', (user_id,))
                conn.commit()

                await ctx.send(f'You leveled up to level: {current_level + 1}')
            else:
                await ctx.send('You need 40 points to level up.')
            
            await ctx.send(f'Your points: {points}')
        else:
            await ctx.send('You\'re not registered in the database yet. Use ```$register``` to enter yourself.')


    @commands.command()
    async def battlepass(self, ctx):
        '''Returns the users current level and points.'''
        user_id = ctx.author.id

        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check the user points
        cursor.execute('SELECT points, level FROM points WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            server_points, level = result
            await ctx.send(f'Level: {level}, Points: {server_points}.')
        else:
            await ctx.send('You\'re not registered in the points system yet. Use the ```$register``` command to get started.')


    @commands.command()
    async def top5(self, ctx):
        '''Returns the top 5 battlepass members.'''
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Checks top 5 users
        cursor.execute('SELECT display_name, level, points FROM points ORDER BY level DESC, points DESC LIMIT 5')
        results = cursor.fetchall()
        message = ''

        for result in results:
            display_name, level, points = result
            message += f'{display_name} - Level: {level} Points: {points}'
        
        await ctx.send(message)


    @commands.command()
    async def shop(self, ctx):
        '''Prints the shop items and values.'''
        message = ''
        for key, value in shop.items():
            message += f'{key} - {value} points.\n'
        await ctx.send(message)


    @commands.command()
    async def inventory(self, ctx):
        '''Lists the user's inventory.'''
        user_id = ctx.author.id

        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Return user inventory list
        cursor.execute('''SELECT item_name, value
                            FROM inventory
                            WHERE user_id = ?''', (user_id,))
        items = cursor.fetchall()

        if items:
            inventory_list = '\n'.join([f"{item[0]} - Value: {item[1]}" for item in items])
            await ctx.send(inventory_list)
        else:
            await ctx.send('Your inventory is empty.')

    @commands.command()
    async def buy(self, ctx, *, item):
        '''Purchase item from shop.'''
        user_id = ctx.author.id

        # Check if user has item already
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''SELECT item_name FROM inventory WHERE user_id = ?''', (user_id,))
        items = cursor.fetchall()

        if items:
            item_names = [item[0] for item in items]
            if item in item_names:
                await ctx.send('You already own this item.')
                return

        # Check if item is in shop
        if item in shop:
            item_value = shop[item]

            # Check if user has enough points to purchase
            cursor.execute('''SELECT points FROM points WHERE user_id = ?''', (user_id,))
            points = cursor.fetchone()

            if points:
                points = points[0]
                if points >= item_value:
                    # Deduct item value from user points
                    cursor.execute('''UPDATE points SET points = points - ? WHERE user_id = ?''', (item_value, user_id,))
                    
                    # Insert item into user inventory
                    purchase_date = datetime.datetime.now()
                    cursor.execute('''INSERT INTO inventory (user_id, item_name, value, purchase_date) VALUES (?, ?, ?, ?)''', (user_id, item, item_value, purchase_date,))

                    conn.commit()
                    conn.close()

                    await ctx.send(f'You purchased {item} for {item_value} points.')
                else:
                    await ctx.send(f'You do not have enough points to purchase this item.')
            else:
                await ctx.send('Register for the battlepass to earn points and purchase items by using the `$register` command.')
        else:
            await ctx.send(f'{item} is not in the shop. Use `$shop` to see items in the shop.')


async def setup(bot):
    await bot.add_cog(BattlepassCog(bot))