import logging
import os
import random
import sqlite3
import datetime
import json
import discord
import pytz
from discord.ext import commands, tasks
import db_interface as db

db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'points.db')
shop_path = os.path.join(os.path.dirname(__file__), '..', 'shop.csv')
shop = []
refresh_time = datetime.datetime.now()

# Load categorized items from JSON file for item shop functions/commands
with open('./categorized_items.json', 'r', encoding='utf-8') as json_file:
        categorized_items = json.load(json_file)

class ShopCog(commands.Cog):
    '''Commands for viewing item shop, buying, and viewing own inventory.'''
    def __init__(self, bot):
        self.bot = bot
        refresh_shop.start()


    @commands.Cog.listener()
    async def on_ready(self):
        '''Print statment to ensure loads properly.'''
        logging.info('Shop Cog loaded.')

    
    @commands.command()
    async def shop(self, ctx):
        '''Prints the shop items and values.'''
        embed = discord.Embed(title='Item Shop', description=f'Refreshes at {refresh_time.strftime("%H:%M %Z")}', timestamp=datetime.datetime.now())
        embed.set_author(name=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar)
        embed.set_thumbnail(url='https://wallpapercave.com/wp/wp7879327.jpg')

        for item in shop:
            item_name, item_value, item_rarity = item
            embed.add_field(name=item_name, value=f'Points: {item_value} - Rarity: {item_rarity}', inline=False)
        
        await ctx.send(embed=embed)
    

    @commands.command()
    async def inventory(self, ctx):
        '''Lists the user's inventory.'''
        user_id = ctx.author.id

        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Return user inventory list
        cursor.execute('''SELECT item_name, value, rarity
                            FROM inventory
                            WHERE user_id = ?''', (user_id,))
        items = cursor.fetchall()

        if items:
            embed = discord.Embed(title='Inventory', timestamp=datetime.datetime.now())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            embed.set_thumbnail(url='https://www.kindpng.com/picc/m/172-1721685_image-png-international-file-dora-the-explorer-backpack.png')
            for item in items:
                embed.add_field(name=item[0], value=f'Value: {item[1]} - Rarity: {item[2]}', inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Your inventory is empty.')
        
        conn.close()


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
            item_value = int(shop[item]['value'])
            item_rarity = shop[item]['rarity']

            # Check if user has enough points to purchase
            cursor.execute('''SELECT points FROM points WHERE user_id = ?''', (user_id,))
            points = cursor.fetchone()

            if points:
                points = int(points[0])

                embed = discord.Embed(title='Item Purchase', timestamp=datetime.datetime.now())
                embed.set_author(name=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar)

                if points >= item_value:
                    # Deduct item value from user points
                    cursor.execute('''UPDATE points SET points = points - ? WHERE user_id = ?''', (item_value, user_id,))

                    # Insert item into user inventory
                    purchase_date = datetime.datetime.now()
                    cursor.execute('''INSERT INTO inventory (user_id, item_name, value, rarity, purchase_date) VALUES (?, ?, ?, ?, ?)''', (user_id, item, item_value, item_rarity, purchase_date,))

                    conn.commit()
                    conn.close()

                    embed.add_field(name=f'{item} has been added to your inventory', value='View your inventory by using `$inventory`.', inline=False)
                    embed.add_field(name='', value=f'Points after purchase: {points - item_value}', inline=False)
                    await ctx.send(embed=embed)
                else:
                    embed.add_field(name=f'You do not have enough points to purchase {item}.', value='', inline=False)
                    embed.add_field(name='', value=f'Your points: {points}', inline=False)
                    embed.add_field(name='', value=f'{item}: {item_value} points.', inline=False)
                    await ctx.send(embed=embed)
            else:
                await ctx.send('Register for the battlepass to earn points and purchase items by using the `$register` command.')
        else:
            await ctx.send(f'{item} is not in the shop. Use `$shop` to see items in the shop.')

    
@tasks.loop(minutes=30)
async def refresh_shop():
    '''Updates shop with five new items every thirty minutes.'''
    global shop
    shop = db.get_shop_items()

    current_time = datetime.datetime.now(pytz.timezone('US/Central'))
    set_shop_refresh_time(current_time + datetime.timedelta(minutes=30))


def set_shop_refresh_time(timestamp):
    '''Updates shop refresh time whenever refresh_shop task runs.'''
    global refresh_time
    refresh_time = timestamp


async def setup(bot):
    '''Runs when bot.load_extension() is called.'''
    await bot.add_cog(ShopCog(bot))
