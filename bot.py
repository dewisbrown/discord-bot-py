import os
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True
intents.presences = True

bot = commands.Bot(command_prefix='$', intents=intents)

# Remove default help command
bot.remove_command('help')

@bot.event
async def on_ready():
    '''Prints statment when bot is logged in.'''
    print(f'Success! Logged in as {bot.user.name}')


@bot.event
async def on_command_error(ctx, error):
    '''Sends error message to user when command is not found.'''
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command not found. Type `$help` for a list of commands.')


async def load():
    '''Loads cogs for bots.'''
    await bot.load_extension('cogs.battlepass')
    await bot.load_extension('cogs.basics')
    await bot.load_extension('cogs.chat')
    await bot.load_extension('cogs.shop')
    await bot.load_extension('cogs.ed')
    await bot.load_extension('cogs.translate')
    await bot.load_extension('cogs.music')
    await bot.load_extension('cogs.moderation')


async def main():
    '''Loads cogs and starts the bot login.'''
    async with bot:
        await load()
        await bot.start(os.getenv('BOT_TOKEN'))


asyncio.run(main())
