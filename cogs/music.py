import discord
import youtube_dl
import asyncio
import os
import datetime
from discord.ext import commands
from discord.voice_client import VoiceClient

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
        embed = discord.Embed(title=f'Current Queue | {len(queue)}', timestamp=datetime.datetime.now())
        for index, item in enumerate(queue):
            embed.add_field(name=f'{index + 1} | (`{item["song_duration"]}`) {item["song_name"]} - {item["request_author"]}', value='', inline=False)
        await ctx.send(embed=embed)



    @commands.command()
    async def play(self, ctx, *, search_terms):
        '''Plays the user submitted search terms in audio chat.'''
        # Check if the user is in a voice channel
        if ctx.author.voice is None:
            await ctx.send("You need to be in a voice channel to use this command.")
            return

        # Join the user's voice channel
        channel = ctx.author.voice.channel

        print(channel)

        voice_client = await channel.connect()

        # Create a YouTube search URL based on user-supplied search terms
        youtube_url = f"https://www.youtube.com/results?search_query={search_terms}"

        # Set up the options for youtube_dl
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'audio_cache/%(title)s.%(ext)s',  # Cache audio files
        }

        # Use youtube_dl to fetch the audio URL
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            url2play = info['entries'][0]['url']
            song_name = info['entries'][0]['title']
            song_duration = info['entries'][0]['duration']
            thumbnail_url = info['entries'][0]['thumbnail']

        # Add song to queue
        add_to_queue(song_name, song_duration, ctx.author.name, thumbnail_url)

        # Play the audio
        voice_client.play(discord.FFmpegPCMAudio(url2play))

        # Adjust embed title when queue is implemented
        embed = discord.Embed(timestamp=datetime.datetime.now())
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.add_field(name=f'Now Playing: {song_name} - [`{song_duration}`]', value=f'Requested by - {ctx.author.name}', inline=False)
        embed.set_thumbnail(url=thumbnail_url)

        await ctx.send(embed=embed)

        # Wait until the audio is finished playing, then disconnect from the voice channel
        while voice_client.is_playing():
            await asyncio.sleep(1)
        await voice_client.disconnect()

        # Clean up cached audio files
        os.remove(f'audio_cache/{info["title"]}.mp3')


def add_to_queue(song_name, song_duration, request_author, thumbnail_url):
    '''Adds songs to queue.'''
    queue.append({'song_name': song_name, 'song_duration': song_duration, 'request_author': request_author, 'thumbnail_url': thumbnail_url})


async def setup(bot):
    await bot.add_cog(MusicCog(bot))
