import datetime
import random
import asyncio
import discord
from discord.ext import commands
import download_yt

# List for song queue
queue = []
current_song = None

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
        if len(queue) == 0:
            await ctx.send('The queue is empty.')
        else:
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

        note_emoji = '\U0001F3B5'
        voice_client = self.bot.voice_clients

        if voice_client:
            try:
                # Download URL and get info, add to queue
                song_info = download_yt.download(url, ctx.author.name)
                queue.append(song_info)

                await ctx.send(f'{note_emoji}  **{song_info["song_name"]}** added to the queue (`{song_info["song_duration"]}`) - at position {len(queue)}')
            except Exception as e:
                print(f'An error occured when adding a song to the queue: {str(e)}')
        else:
            try:
                # Download URL and get info
                song_info = download_yt.download(url, ctx.author.name)
                queue.append(song_info)
                await ctx.send(f'{note_emoji}  Added **{song_info["song_name"]} (`{song_info["song_duration"]}`)** to begin playing.')

                # Join voice channel
                voice_channel = ctx.author.voice.channel
                voice_client = await voice_channel.connect()

                while len(queue) > 0:
                    next_song = queue.pop(0)
                    
                    global current_song
                    current_song = next_song

                    # Play the audio stream
                    voice_client.play(discord.FFmpegPCMAudio(next_song['file_path']))

                    embed = discord.Embed(title=f'Queue length: {len(queue)}', timestamp=datetime.datetime.now())
                    embed.set_author(name=f'{ctx.guild.name} - Now playing')
                    embed.set_thumbnail(url=next_song['thumbnail_url'])
                    embed.add_field(name=f'{note_emoji}  {next_song["song_name"]} - [`{next_song["song_duration"]}`]', value=f'*Requested by* {next_song["request_author"]}', inline=False)
                    await ctx.send(embed=embed)
                    
                    # Wait for playback to finish
                    while voice_client.is_playing():
                        await asyncio.sleep(1)

                    # Remove download from downloads directory
                    download_yt.delete(next_song['file_path'])
            except Exception as ex:
                print(f'An error occurred trying to play song: {str(ex)}')

            # Leave the voice channel
            await voice_client.disconnect()
    

    @commands.command()
    async def skip(self, ctx):
        '''Stops current song playing and plays next song in queue.'''
        if self.bot.voice_clients and current_song:
            await ctx.send(f'Skipping {current_song["song_name"]}')
            
            # Remove download from downloads directory
            download_yt.delete(current_song['file_path'])
            
            # add skipping logic here
        else:
            await ctx.send('There is no song currently playing.')

    
    @commands.command()
    async def stop(self, ctx):
        '''Disconnects bot from voice channel and clears queue.'''
        if self.bot.voice_clients:
            self.bot.voice_clients.disconnect()
            queue.clear()
        else:
            await ctx.send('There is no song currently playing.')

    
    @commands.command()
    async def shuffle(self, ctx):
        '''Shuffles queue.'''
        if len(queue) > 0:
            random.shuffle(queue)
        else:
            await ctx.send('There is nothing in the queue.')


async def setup(bot):
    await bot.add_cog(MusicCog(bot))
