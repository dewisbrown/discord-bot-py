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
    print('Success! Bot is connected to Discord.')


async def load():
    await bot.load_extension('cogs.battlepass')
    await bot.load_extension('cogs.basics')
    await bot.load_extension('cogs.chat')


async def main():
    async with bot:
        await load()
        await bot.start(os.getenv('BOT_TOKEN'))


asyncio.run(main())
