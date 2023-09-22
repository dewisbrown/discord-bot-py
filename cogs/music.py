import datetime
import logging
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
        logging.info('Music Cog loaded.')


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
        
        logging.info('Queue command submitted by [%s]', ctx.author.name)


    @commands.command()
    async def play(self, ctx, url):
        '''Plays the user submitted search terms in audio chat.'''
        logging.info('Play command submitted by [%s]', ctx.author.name)
        
        if ctx.author.voice is None:
            await ctx.send('You must be in a voice channel to run this command.')
            logging.info('Play command failed: [%s] is not in voice channel.', ctx.author.name)
            return

        note_emoji = '\U0001F3B5'
        voice_client = self.bot.voice_clients

        if voice_client:
            try:
                # Download URL and get info, add to queue
                song_info = download_yt.download(url, ctx.author.name)
                queue.append(song_info)

                await ctx.reply(f'{note_emoji}  **{song_info["song_name"]}** added to the queue (`{song_info["song_duration"]}`) - at position {len(queue)}')
            except Exception as ex:
                logging.error('Failed to add song to queue: %s', str(ex))
        else:
            try:
                # Download URL and get info
                song_info = download_yt.download(url, ctx.author.name)
                queue.append(song_info)
                await ctx.reply(f'{note_emoji}  Added **{song_info["song_name"]} (`{song_info["song_duration"]}`)** to begin playing.')

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
                    embed.set_author(name=f'{ctx.guild.name} - Now playing', icon_url=ctx.guild.icon)
                    embed.set_thumbnail(url=next_song['thumbnail_url'])
                    embed.add_field(name=f'{note_emoji}  {next_song["song_name"]} - [`{next_song["song_duration"]}`]', value=f'*Requested by* {next_song["request_author"]}', inline=False)
                    await ctx.send(embed=embed)
                    
                    # Wait for playback to finish
                    while voice_client.is_playing():
                        await asyncio.sleep(1)

                    # Remove download from downloads directory
                    download_yt.delete(next_song['file_path'])
            except Exception as ex:
                 logging.error('Failed to play song: %s', str(ex))

            # Leave the voice channel
            await voice_client.disconnect()


    @commands.command()
    async def skip(self, ctx):
        '''Stops current song playing and plays next song in queue.'''
        logging.info('Skip command submitted by %s', ctx.author.name)
        
        note_emoji = '\U0001F3B5'
        cowboy_emoji = '\U0001F920'
        voice_client = ctx.voice_client
        global current_song
        skipped_song = current_song

        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await ctx.reply(f'{cowboy_emoji}  Skipped **{current_song["song_name"]}** ' /
                           f'- [`{current_song["song_duration"]}`]')

            if queue:
                next_song = queue.pop(0)
                current_song = next_song
                voice_client.play(discord.FFmpegPCMAudio(next_song['file_path']))

                embed = discord.Embed(title=f'Queue length: {len(queue)}', timestamp=datetime.datetime.now())
                embed.set_author(name=f'{ctx.guild.name} - Now playing', icon_url=ctx.guild.icon)
                embed.set_thumbnail(url=next_song['thumbnail_url'])
                embed.add_field(name=f'{note_emoji}  {next_song["song_name"]} - [`{next_song["song_duration"]}`]', value=f'*Requested by* {next_song["request_author"]}', inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send('No more songs in the queue.')
        else:
            await ctx.send('There is no song currently playing.')

        download_yt.delete(skipped_song['file_path'])


    @commands.command()
    async def stop(self, ctx):
        '''Disconnects bot from voice channel and clears queue.'''
        logging.info('Stop command submitted by [%s]', ctx.author.name)
        
        voice_client = ctx.voice_client

        if voice_client and voice_client.is_playing():
            await voice_client.stop()

            # delete current song
            download_yt.delete(current_song['file_path'])

            # delete songs in queue
            for song in queue:
                download_yt.delete(song["file_path"])
            queue.clear()
        else:
            await ctx.send('There is no song currently playing.')


    @commands.command()
    async def shuffle(self, ctx):
        '''Shuffles queue.'''
        logging.info('Shuffle command submitted by [%s]', ctx.author.name)

        if len(queue) > 0:
            random.shuffle(queue)
        else:
            await ctx.send('There is nothing in the queue.')


    @commands.command()
    async def move(self, ctx, index1, index2):
        '''Modifies queue order by moving a song to a target index in the queue.'''
        logging.info('Move command submitted by [%s]', ctx.author.name)
        
        index1 -= 1
        index2 -= 1

        if 0 <= index1 < len(queue) and 0 <= index2 < len(queue):
            queue[index1], queue[index2] = queue[index2], queue[index1]
            await ctx.send(f'Moved {queue[index1]["song_name"]} to position {index2} in queue.')
        else:
            await ctx.send('Invalid index input.')


async def setup(bot):
    await bot.add_cog(MusicCog(bot))
