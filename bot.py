import os
import sqlite3
import datetime
import random
import discord
import pytz
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def hello(ctx):
    '''Test command, replies hello!'''
    await ctx.send('Hello, I am your Discord bot!')


@bot.command()
async def age(ctx, user: discord.Member = None):
    '''Returns days since joining server.'''
    if user is None:
        user = ctx.author
    
    if ctx.guild:
        joined_at = user.joined_at
        timezone = pytz.timezone('America/Chicago')

        # Convert joined_at to the server's timezone
        joined_at = joined_at.astimezone(timezone)

        current_time = datetime.datetime.now(timezone)
        days_in_server = (current_time - joined_at).days

        await ctx.send(f'{user.display_name} has been in the server {days_in_server} days.')
    else:
        await ctx.send('This command is only applicable in a server (guild) context')


@bot.command()
async def register(ctx):
    user_id = ctx.author.id
    registration_timestamp = datetime.datetime.now()

    # Connect to the database
    conn = sqlite3.connect('data/points.db')
    cursor = conn.cursor()

    # Check if the user is already registered
    cursor.execute('SELECT user_id FROM points WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        await ctx.send("You are already registered.")
    else:
        cursor.execute('INSERT INTO points (user_id, points, last_awarded_at) VALUES (?, ?, ?)', (user_id, 10, registration_timestamp))
        conn.commit()
        await ctx.send('You have been registered with 10 points.')
    
    conn.close()

# TODO: Also print how long until next points redemption
@bot.command()
async def points(ctx):
    user_id = ctx.author.id

    # Connect to the database
    conn = sqlite3.connect('data/points.db')
    cursor = conn.cursor()

    # Check the last awarded timestamp for the user
    cursor.execute('SELECT last_awarded_at FROM points WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        last_awarded_at_str = result[0]
        last_awarded_at = datetime.datetime.strptime(last_awarded_at_str, '%Y-%m-%d %H:%M:%S.%f')
        current_time = datetime.datetime.now()
        time_since_last_awarded = current_time - last_awarded_at

        # Check if it has been at least 24 hours
        if time_since_last_awarded.total_seconds() >= 3600: # 3600 seconds/hour
            cursor.execute('UPDATE points SET points = points + 10, last_awarded_at = ? WHERE user_id = ?', (current_time, user_id))
            conn.commit()

            await ctx.send("You've been awarded 10 points!")
        else:       # Tell user not right time, print their current points
            cursor.execute('SELECT points FROM points WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            server_points = result[0]
            message = 'Sorry, you can only claim points once an hour.\n'
            message += f'You have {server_points} points.'
            await ctx.send(message)
    else:
        await ctx.send('You\'re not registered in the points system yet. Use the ```$register``` command to get started.')

    conn.close()


load_dotenv()
bot.run(os.getenv('BOT_TOKEN'))
