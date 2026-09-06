import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCOED_TOKEN')

handler = logging.FileHandler(filename="bot.log",encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    print("Ready")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return 

    if "test" == message.content.lower():
        await message.channel.send(f"test")

    await bot.process_commands(message)



shells = []

shell_number = 0
@bot.command()
async def start(ctx):
    global shell_number
    global shells
    shell_number += 1
    channel_name = f"shell {shell_number}"
    channel = await ctx.guild.create_text_channel(name=channel_name)
    await ctx.send(f"{ctx.author.mention} - Shell {shell_number}: {channel.mention}")
    shells.append(channel.id)

@bot.command()
async def exit(ctx):
    if ctx.channel.id in shells:
        global shell_number
        shell_number -= 1
        await ctx.channel.delete()
    else:
        await ctx.send("You are not in a shell channel")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)