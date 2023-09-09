import os
import random
import discord
import datetime
from discord.ext import commands

ed_path = os.path.join(os.path.dirname(__file__), '..', 'ed_sayings.txt')

class EdCog(commands.Cog):
    '''Commands for Ed quotes and pictures.'''
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        '''Prints statement when loaded.'''
        print('Ed Cog loaded.')


    @commands.command()
    async def addquote(self, ctx, *, quote):
        '''Inputs a quote to the ed quote text file.'''
        embed = discord.Embed(title='Ed Quote Submission', timestamp=datetime.datetime.now())
        
        if quote:
            with open(ed_path, 'a', encoding='utf-8') as file:
                file.write(f'{quote}\n')
            
            embed.set_author(name=f'Submitted by {ctx.author.name}', icon_url=ctx.author.avatar)
            embed.add_field(name='Submitted Quote:', value=quote, inline=False)
        else:
            embed.add_field(name='No quote was submitted...', value='Use this format to submit a quote: `$addEdQuote <quote>`.')

        await ctx.send(embed=embed)


    @commands.command()
    async def edquote(self, ctx):
        '''Retrievs quote from Ed quote text file.'''
        embed = discord.Embed(title='Quote from Sir Edward Skunks', timestamp=datetime.datetime.now())
        embed.set_thumbnail(url='https://scontent-dfw5-2.xx.fbcdn.net/v/t39.30808-6/283356360_4381924898577272_6630664783584697009_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=a2f6c7&_nc_ohc=S7ZOaZFc_lwAX-N7ORZ&_nc_ht=scontent-dfw5-2.xx&oh=00_AfBjFI1ETNfWhmIspaSSCD1SzPH6mcm_Xl7NDxZ63vhv8w&oe=64FFECA8')
        embed.set_author(name=f'Requested by {ctx.author.name}')

        with open(ed_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            if lines:
                random_line = random.choice(lines)
                embed.add_field(name='', value=random_line, inline=False)
            else:
                embed.add_field(name='', value='No quotes exist.', inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def edtroll(self, ctx):
        '''Sends picture of troll Ed.'''
        embed = discord.Embed(title='Troll Ed', timestamp=datetime.datetime.now())
        embed.set_image(url='https://scontent-dfw5-2.xx.fbcdn.net/v/t39.30808-6/283356360_4381924898577272_6630664783584697009_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=a2f6c7&_nc_ohc=S7ZOaZFc_lwAX-N7ORZ&_nc_ht=scontent-dfw5-2.xx&oh=00_AfBjFI1ETNfWhmIspaSSCD1SzPH6mcm_Xl7NDxZ63vhv8w&oe=64FFECA8')
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(EdCog(bot))