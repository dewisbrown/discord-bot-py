import os
import random
import sqlite3
import datetime
from discord.ext import commands, tasks

db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'points.db')
shop_path = os.path.join(os.path.dirname(__file__), '..', 'shop_items.txt')
shop = {}

class ShopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        refresh_shop.start()


    @commands.Cog.listener()
    async def on_ready(self):
        '''Print statment to ensure loads properly.'''
        print('Shop Cog loaded.')

    
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
                    await ctx.send('You do not have enough points to purchase this item.')
            else:
                await ctx.send('Register for the battlepass to earn points and purchase items by using the `$register` command.')
        else:
            await ctx.send(f'{item} is not in the shop. Use `$shop` to see items in the shop.')

    
    
@tasks.loop(hours=1)
async def refresh_shop():
    '''Updates shop with 5 new items every hour.'''
    global shop
    items_list = read_shop_file()
    random.shuffle(items_list)

    new_shop = {}

    while len(new_shop) < 5 and items_list:
        item_value_pair = items_list.pop(0).split(',')
        if len(item_value_pair) == 2:
            item, value = item_value_pair
            if item not in shop:
                new_shop[item] = int(value)

    shop = new_shop


def read_shop_file():
    '''Returns list of items and values from text file.'''
    with open(shop_path, 'r', encoding='utf-8') as file:
        items_list = [line.strip() for line in file]
    return items_list


async def setup(bot):
    '''Runs when bot.load_extension() is called.'''
    await bot.add_cog(ShopCog(bot))