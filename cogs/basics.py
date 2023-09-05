import discord
import pytz
import datetime
from discord.ext import commands

class BasicsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Basics Cog loaded.')


    @commands.command()
    async def listcommands(self, ctx):
        message = '$age : Amount of days you have been in the server.\n'
        message += '$battlepass: Level and points for user.\n'
        message += '$points: Earn 10 points every hour.\n'
        message += '$tierup: Buy battlepass level with points.\n'
        message += '$register: Enter yourself into battlepass.\n'
        message += '$hello: Bot responds with hello.'
        
        await ctx.send(message)

    @commands.command()
    async def hello(self, ctx):
        '''Test command, replies hello!'''
        await ctx.send('Hello, I am your Discord bot!')


    @commands.command()
    async def age(self, ctx, user: discord.Member = None):
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


async def setup(bot):
    await bot.add_cog(BasicsCog(bot))