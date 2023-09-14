import discord
import asyncio
import os
import datetime
from discord.ext import commands
from discord.voice_client import VoiceClient
from pytube import YouTube

# List for song queue
queue = []

class MusicCog(commands.Cog):
    '''Commands that handle music playing in audio channel.'''
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        '''Print statment to ensure loads properly.'''
        print('Music Cog loaded.')

    
    # Update title to embed when queue is implemented
    @commands.command()
    async def queue(self, ctx):
        '''Displays the music queue.'''
        note_emoji = '\U0001F3B5'
        embed = discord.Embed(title=f'{note_emoji}  **Current Queue | {len(queue)} entries**', timestamp=datetime.datetime.now())
        message = ''

        for index, item in enumerate(queue):
            message += f'`{index + 1}` | (`{item["song_duration"]}`) **{item["song_name"]} -** {item["request_author"]}\n'
        
        embed.add_field(name='', value=message, inline=False)
        await ctx.send(embed=embed)


    @commands.command()
    async def play(self, ctx, *, url):
        '''Plays the user submitted search terms in audio chat.'''
    
        # pytube YouTube object with user submitted url
        yt = YouTube(url)
        song_name = yt.title
        song_duration = format_time(yt.length)
        thumbnail_url = yt.thumbnail_url
        note_emoji = '\U0001F3B5'

        # Add song to queue
        queue.append({'song_name': song_name, 'song_duration': song_duration, 'request_author': ctx.author.name, 'thumbnail_url': thumbnail_url})
        if len(queue) == 1:
            await ctx.send(f'{note_emoji}  Added **{song_name} (`{song_duration}`)** to begin playing.')
        else:
            await ctx.send(f'{note_emoji}  **{song_name}** added to the queue (`{song_duration}`) - at position {len(queue)}')


    
    @commands.command()
    async def ding(self, ctx):
        '''Joins voice channel and plays ding noise.'''
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
        
            voice_channel = await channel.connect()

            mp4_path = os.path.join(os.path.dirname(__file__), '..', 'downloads', 'Ding Sound Effect - No Copyright.mp4')

            if os.path.exists(mp4_path):
                voice_channel.play(discord.FFmpegPCMAudio(mp4_path))

                while voice_channel.is_playing():
                    await asyncio.sleep(1)

                await voice_channel.disconnect()
            else:
                await ctx.send('File `Ding Sound Effect - No Copyright.mp4` not found.')
        else:
            await ctx.send('You need to be in a voice channel to use this command.')
        
        

def format_time(seconds):
    '''Formats total seconds to %M:%S format.'''
    minutes, seconds = divmod(seconds, 60)
    return f'{minutes}:{seconds:02d}'


async def setup(bot):
    await bot.add_cog(MusicCog(bot))
