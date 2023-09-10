import discord
import datetime
from discord.ext import commands
from googletrans import Translator

class TranslateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print('Translate Cog loaded.')


    @commands.command()
    async def translate(self, ctx, target_lang='en', *, text):
        '''Translates text to target language.'''
        supported_langs = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'it': 'Italian',
            'pt': 'Portuguese',
            'nl': 'Dutch',
            'ru': 'Russian',
            'zh-CN': 'Chinese (Simplified)',
            'ja': 'Japanese',
            'ko': 'Korean',
            'ar': 'Arabic',
            'vi': 'Vietnamese',
            'el': 'Greek',
            'fi': 'Finnish'
        }

        # String for embed response
        formated_pairs = [f'{key} : {value}' for key, value in supported_langs.items()]
        pairs_string = '\n'.join(formated_pairs)

        translator = Translator()

        embed = discord.Embed(timestamp=datetime.datetime.now())
        embed.set_author(name=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar)
        embed.set_thumbnail(url='https://playstoretips.com/wp-content/uploads/2018/08/1200px-Google_Translate_logo.svg_.png')

        if target_lang.lower() not in supported_langs:
            embed.add_field(name='Target language missing.', value=pairs_string, inline=False)
            embed.add_field(name='Command format:', value='`$translate <target_language> <text_to_translate>`')
            await ctx.send(embed=embed)
            return
        
        try:
            translation = translator.translate(text, dest=target_lang)
            translated_text = translation.text
            embed.add_field(name='', value=translated_text, inline=False)
            embed.add_field(name='', value=text, inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'An error occured: {e}')

    
async def setup(bot):
    await bot.add_cog(TranslateCog(bot))
