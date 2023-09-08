import datetime
import discord
from discord.ext import commands

class PicsCog(commands.Cog):
    '''Commands for receiving images from the bot.'''
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        '''Print statment to ensure cog loads properly.'''
        print('Pics Cog loaded.')

    
    @commands.command()
    async def troll_ed(self, ctx):
        '''Sends picture of troll Ed.'''
        embed = discord.Embed(title='Troll Ed', timestamp=datetime.datetime.now())
        embed.set_image(url='https://scontent-dfw5-2.xx.fbcdn.net/v/t39.30808-6/283356360_4381924898577272_6630664783584697009_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=a2f6c7&_nc_ohc=S7ZOaZFc_lwAX-N7ORZ&_nc_ht=scontent-dfw5-2.xx&oh=00_AfBjFI1ETNfWhmIspaSSCD1SzPH6mcm_Xl7NDxZ63vhv8w&oe=64FFECA8')
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(PicsCog(bot))
