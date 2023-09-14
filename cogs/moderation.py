import discord
import datetime
from discord.ext import commands

class ModerationCog(commands.Cog):
    '''Commands for discord moderation.'''
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        '''Prints when cog is loaded.'''
        print('Moderation Cog loaded.')

    
    @commands.command()
    async def help(self, ctx):
        '''Lists bot commands.'''
        embed = discord.Embed(timestamp=datetime.datetime.now())

        battlepass_commands = '''`$battlepass` - Displays level and points for user.\n
                    `$points` - Gain points every 15 minutes.\n
                    `$register` - Register for battlepass.\n
                    `$tierup` - Spend points to increase battlepass level.\n
                    `$top5` - Displays top 5 battlepass members.'''
        
        ed_commands = '''`$addquote <quote>` - Adds supplied quote to list of Ed quotes.\n
                    `$edquote` - Displays a random quote from the list of Ed quotes.\n
                    `$edrandom` - Displays a random picture of Ed.'''
        
        shop_commands = '''`$buy <item_name>` - Purchase item from item shop.\n
                    `$inventory` - Displays user inventory.\n
                    `$shop` - Displays shop items and values, refreshes every thirty minutes.'''
        
        translate_commands = '''`$translate <target_language> <text_to_translate>` - Translates text using Google Translate.'''
        
        music_commands = '''`$play <youtube_url>` - Plays supplied YouTube video audio in voice channel.\n
                    `$queue` - Displays the music queue.\n
                    `$stop` - Stops the music player and the bot exits the voice channel.\n
                    `$skip` - Skips the current song playing.\n
                    `$seek <time_stamp>` - Plays song at supplied time stamp.\n
                    `$shuffle` - Shuffles music queue.\n
                    `$move <target_song_index> <target_index>` - Moves song in queue to a different queue position.'''
        
        # All commands
        embed.add_field(name='Battlepass Commands', value=battlepass_commands, inline=False)
        embed.add_field(name='', value='', inline=False)
        embed.add_field(name='Ed Commands', value=ed_commands, inline=False)
        embed.add_field(name='', value='', inline=False)
        embed.add_field(name='Shop Commands', value=shop_commands, inline=False)
        embed.add_field(name='', value='', inline=False)
        embed.add_field(name='Translate Commands', value=translate_commands, inline=False)
        embed.add_field(name='', value='', inline=False)
        embed.add_field(name='Music Commands', value=music_commands, inline=False)
        embed.add_field(name='', value='', inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ModerationCog(bot))