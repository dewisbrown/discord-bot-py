import os
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Success! Logged in as {bot.user.name}')


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return


@bot.event
async def on_command_error(ctx, error):
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


async def main():
    async with bot:
        await load()
        await bot.start(os.getenv('BOT_TOKEN'))


asyncio.run(main())
