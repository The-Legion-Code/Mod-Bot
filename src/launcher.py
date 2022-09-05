import os
import discord
from bot import ModBot

bot = ModBot(token=os.environ['TOKEN'],
             intents=discord.Intents.all(),
             help_command=None)

bot.starter()
