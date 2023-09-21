import logging
import discord
import datetime
import asyncio
from discord.ext import commands
from chatbot import chatbot_interface, add_new_answer


class ChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        '''Print statment to ensure loads properly.'''
        logging.info('Chat Cog loaded.')


    @commands.command()
    async def chat(self, ctx, *, prompt):
        '''Returns a response from chatGPT given a prompt.'''
        logging.info('Chat command submitted by [%s]', ctx.author.name)
        response = chatbot_interface(prompt)
        
        if response:
            await ctx.send(response)
            return
        else:
            await ctx.send('I don\'t know the response to that. Teach me? **"yes"** or **"no"**')
        
        # Wait for user response
        try:
            teach_message = await self.bot.wait_for(
                'message',
                check=lambda message: message.author == ctx.author and message.content.lower() in ['yes', 'no'],
                timeout=30
            )
        except asyncio.TimeoutError:
            await ctx.send('You took to long to respond. Chat input cancelled.')
            logging.error('Response timeout for [%s]', ctx.author.name)
            return
        
        if teach_message.content.lower() == 'yes':
            await ctx.send(f'Provide the response for:\n*{prompt}*')
        else:
            await ctx.send('No response learned \U0001F63F')
            return

        # Wait for user answer
        try:
            answer_message = await self.bot.wait_for(
                'message',
                check=lambda message: message.author == ctx.author,
                timeout=30
            )
        except asyncio.TimeoutError:
            await ctx.send('You took to long to respond. Chat input cancelled.')
            logging.error('Response timeout for [%s]', ctx.author.name)
            return
        
        answer = answer_message.content
        add_new_answer(prompt, answer)

        await ctx.send(f'New response learned:\nQ: **{prompt}**\nA: *{answer}*')

async def setup(bot):
    await bot.add_cog(ChatCog(bot))
