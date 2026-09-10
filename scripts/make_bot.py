import discord
from discord.ext import commands
import logging

def make_bot():
    handler = logging.FileHandler(filename="bot.log",encoding='utf-8',mode='w')

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='!',intents=intents)

    return bot, handler

    