import logging
import os
import requests
from dotenv import load_dotenv
from discord.ext import commands

class ChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        load_dotenv()


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Chat Cog loaded.')


    @commands.command()
    async def gpt(self, ctx, *, prompt):
        '''Returns a response from chatGPT given a prompt.'''
        
         # Define the API endpoint
        api_url = 'https://api.openai.com/v1/chat/completions'

        # Set your OpenAI API key
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.getenv("OPEN_AI_API_KEY")}'
        }

        # Construct the request payload
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        try:
            # Make the API request
            response = requests.post(api_url, headers=headers, json=payload)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                data = response.json()

                # Extract the generated message from the response
                if 'choices' in data and data['choices'][0]['message']:
                    generated_message = data['choices'][0]['message']
                    await ctx.send(f'Response from ChatGPT: {generated_message}')
                else:
                    await ctx.send('No response received from ChatGPT.')
            else:
                print(f'Error: {response.status_code} - {response.text}')
        except Exception as e:
            print(f'Error: {str(e)}')


async def setup(bot):
    await bot.add_cog(ChatCog(bot))