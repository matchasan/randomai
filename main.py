import discord
import os
import random
import func
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

# with open("./env.txt", "r", encoding='utf-8') as f:
#     token_list = [s.strip() for s in f.readlines()]
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNELID = int(os.getenv("CHANNEL"))

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if not message.author.bot:
        #オウム
        channel = client.get_channel(CHANNELID)
        # await channel.send(message.content)
        # print(message.content)

        # if message.content == "random":
        #     text = func.randomWheel()
        #     await channel.send(text)
        #     print(text)
        t = func.createResponse(message.content)
        await channel.send(t)
        print(t)

client.run(TOKEN)

