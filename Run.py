import os
import disnake
import logging

from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

description = """Bot for fun commands"""

intents = disnake.Intents.default()
intents.members = True

#Define the bot
bot = commands.Bot(
    command_prefix=os.getenv("PREFIX"), 
    intents=intents, 
    description=description,
    test_guilds = [491700910712684554],
    sync_commands = True)

#Load cogs into the bot
for c in os.listdir("cogs"):
    if c.endswith(".py"):
        bot.load_extension("cogs." + c[:-3])

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("-----------")

#Run the bot
bot.run(os.getenv('TOKEN'))