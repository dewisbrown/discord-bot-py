import sqlite3
import datetime
import os
import discord
from discord.ext import commands

db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'points.db')

def get_points_to_level(level):
    '''Helper function to let bot know how many points it cost to tier up.'''
    if level < 5:
        return 40
    if level < 15:
        return 50
    if level < 25:
        return 60
    if level < 35:
        return 75
    if level < 50:
        return 100


def get_points_for_command(level):
    '''Helper function to determine how many points to give user when running $points.'''
    if level < 5:
        return 10
    if level < 15:
        return 20
    if level < 25:
        return 30
    if level < 35:
        return 45
    if level < 50:
        return 50


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
        user_name = ctx.author.name
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
            cursor.execute('INSERT INTO points (user_id, points, last_awarded_at, level, user_name) VALUES (?, ?, ?, ?, ?)', (user_id, 100, registration_timestamp, 1, user_name))
            conn.commit()

            embed = discord.Embed(title='Battlepass Registration', timestamp=registration_timestamp)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            embed.set_thumbnail(url='http://media.comicbook.com/2018/05/battle-pass-icon-1111187.jpeg')
            embed.add_field(name='', value='You have received 100 points for registering.', inline=False)
            await ctx.send(embed=embed)
        
        conn.close()


    @commands.command()
    async def points(self, ctx):
        '''Allows user to get points every 15 minutes.'''
        user_id = ctx.author.id

        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check the last awarded timestamp for the user
        cursor.execute('SELECT last_awarded_at, level FROM points WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            last_awarded_at_str, level = result
            last_awarded_at = datetime.datetime.strptime(last_awarded_at_str, '%Y-%m-%d %H:%M:%S.%f')
            current_time = datetime.datetime.now()
            time_since_last_awarded = current_time - last_awarded_at
            next_redemption_time = (last_awarded_at + datetime.timedelta(minutes=15)).strftime('%Y-%m-%d %I:%M %p')

            # Check if it has been at least 15 minutes
            if time_since_last_awarded.total_seconds() >= 900: # 15 minutes
                points_to_increment = get_points_for_command(level)
                cursor.execute('UPDATE points SET points = points + ?, last_awarded_at = ? WHERE user_id = ?', (points_to_increment, current_time, user_id))
                conn.commit()

                embed = discord.Embed(title='Battlepass Points', timestamp=current_time)
                embed.set_author(name=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar)
                embed.set_thumbnail(url='https://cdn4.iconfinder.com/data/icons/stack-of-coins/100/coin-03-512.png')
                embed.add_field(name=f'You\'ve been awarded {points_to_increment} points!', value=f'Your next redemption time is: {(current_time + datetime.timedelta(minutes=15)).strftime("%Y-%m-%d %I:%M %p")}', inline=False)
                await ctx.send(embed=embed)

            else: 
                embed = discord.Embed(title='Battlepass Points', timestamp=current_time)
                embed.set_author(name=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar)
                embed.set_thumbnail(url='https://cdn4.iconfinder.com/data/icons/stack-of-coins/100/coin-03-512.png')
                embed.add_field(name='', value='Sorry, you can only claim points every 15 minutes.', inline=False)
                embed.add_field(name='', value=f'Your next redemption time is: {next_redemption_time}', inline=False)
                await ctx.send(embed=embed)
        else:
            await ctx.send('You\'re not registered in the points system yet. Use the `$register` command to get started.')

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
            points_to_level_up = get_points_to_level(current_level)
            embed = discord.Embed(title='Battlepass Tier Up', timestamp=datetime.datetime.now())
            embed.set_author(name=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar)

            if points >= points_to_level_up:
                cursor.execute('UPDATE points SET points = points - ?, level = level + 1 WHERE user_id = ?', (points_to_level_up, user_id,))
                conn.commit()

                embed.add_field(name=f'You leveled up to level: {current_level + 1}', value=f'Points after tier up: {points - points_to_level_up}', inline=False)
                await ctx.send(embed=embed)
            else:
                embed.add_field(name='', value=f'You need {points_to_level_up} points to level up.', inline=False)
                await ctx.send(embed=embed)
        else:
            await ctx.send('You\'re not registered in the database yet. Use `$register` to enter yourself.')
        
        conn.close()


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
            embed = discord.Embed(title='Battlepass Progress', timestamp=datetime.datetime.now())
            embed.set_author(name=ctx.author.name)
            embed.set_thumbnail(url=ctx.author.avatar)
            embed.add_field(name=f'Level: {level}', value=f'Points: {server_points}', inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send('You\'re not registered in the points system yet. Use the `$register` command to get started.')
        
        conn.close()


    @commands.command()
    async def top5(self, ctx):
        '''Returns the top 5 battlepass members.'''
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Checks top 5 users
        cursor.execute('SELECT user_name, level, points FROM points ORDER BY level DESC, points DESC LIMIT 5')
        results = cursor.fetchall()

        embed = discord.Embed(title='Top 5 Battlepass Members', description='Sorted by level and points.', timestamp=datetime.datetime.now())
        embed.set_thumbnail(url='https://ih1.redbubble.net/image.660900869.4748/pp,504x498-pad,600x600,f8f8f8.u8.jpg')
        
        for result in results:
            user_name, level, points = result
            embed.add_field(name=user_name, value=f'Level: {level} Points: {points}', inline=False)
        
        await ctx.send(embed=embed)
        conn.close()


async def setup(bot):
    await bot.add_cog(BattlepassCog(bot))