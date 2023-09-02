import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

<<<<<<< HEAD
client.run(os.getenv('BOT_TOKEN'))
=======
        # Convert joined_at to the server's timezone
        joined_at = joined_at.astimezone(timezone)

        current_time = datetime.datetime.now(timezone)
        days_in_server = (current_time - joined_at).days

        await ctx.send(f'{user.display_name} has been in the server {days_in_server} days.')
    else:
        await ctx.send('This command is only applicable in a server (guild) context')


bot.run('BOT_TOKEN')
>>>>>>> 8caf7c1 (removed token)
