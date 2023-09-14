import discord
import asyncio
import os
import datetime
import download_yt
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
    async def play(self, ctx, url):
        '''Plays the user submitted search terms in audio chat.'''
        if ctx.author.voice is None:
            await ctx.send('You must be in a voice channel to run this command.')
            return

        try:
            # Download URL and get info
            song_info = download_yt.download(url, ctx.author.name)
            song_path = os.path.join(os.path.dirname(__file__), '..', 'downloads', f'{song_info["song_name"]}.mp4')
            note_emoji = '\U0001F3B5'

            if len(queue) == 0:
                await ctx.send(f'{note_emoji}  Added **{song_info["song_name"]} (`{song_info["song_duration"]}`)** to begin playing.')
            else:
                await ctx.send(f'{note_emoji}  **{song_info["song_name"]}** added to the queue (`{song_info["song_duration"]}`) - at position {len(queue)}')
                queue.append(song_info)

            # Join voice channel
            voice_channel = ctx.author.voice.channel
            voice_client = await voice_channel.connect()

            # Play the audio stream
            voice_client.play(discord.FFmpegPCMAudio(song_path))

            # Wait for playback to finish
            while voice_client.is_playing():
                await asyncio.sleep(1)

            # Leave the voice channel
            await voice_client.disconnect()
        except Exception as ex:
            print(f'An error occurred: {str(ex)}')

    
    @commands.command()
    async def ding(self, ctx):
        '''Joins voice channel and plays ding noise.'''
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
        
            voice_channel = await channel.connect()

            mp4_path = os.path.join(os.path.dirname(__file__), '..', 'downloads', 'ТРИ ПОЛОСКИ  KOLM TRIIPU  THREE STRIPES.mp4')

            if os.path.exists(mp4_path):
                voice_channel.play(discord.FFmpegPCMAudio(mp4_path))

                while voice_channel.is_playing():
                    await asyncio.sleep(1)

                await voice_channel.disconnect()
            else:
                await ctx.send('File `Ding Sound Effect - No Copyright.mp4` not found.')
        else:
            await ctx.send('You need to be in a voice channel to use this command.')


async def setup(bot):
    await bot.add_cog(MusicCog(bot))
