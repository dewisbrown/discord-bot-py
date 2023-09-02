import discord
import random
from discord.ext import commands
import datetime
import pytz

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def hello(ctx):
    await ctx.send('Hello, I am your Discord bot!')


@bot.command()
async def age(ctx, user: discord.Member = None):
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


bot.run('BOT_TOKEN')