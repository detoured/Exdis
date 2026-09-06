import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import subprocess
import sys

async def run_command(message):
    command = subprocess.run(message.content.split(" "), capture_output=True)
    if command.returncode == 0:
        if command.stdout:
            await message.channel.send(f"```{(command.stdout).decode("utf-8")}```")
        else:
            await message.add_reaction("✅")
    if command.returncode == 1:
        await message.channel.send(f"```{(command.stderr).decode("utf-8")}```")

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


shells = []

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return 

    if message.channel.id in shells and message.content != "!exit":
        await run_command(message)

    if "test" == message.content.lower():
        await message.channel.send(f"test")

    await bot.process_commands(message)


@bot.command()
async def start(ctx):
    global shells
    channel = await ctx.guild.create_text_channel(name="shell")
    await ctx.send(f"{ctx.author.mention} - New shell: {channel.mention}")
    shells.append(channel.id)

@bot.command()
async def exit(ctx):
    if ctx.channel.id in shells:
        shells.remove(ctx.channel.id)
        await ctx.channel.delete()
    else:
        await ctx.send("You are not in a shell channel")

async def stop(ctx):
    if ctx.channel.id in shells:
        await ctx.channel.send("You cannot use the stop command in a shell channel")
    else:
        sys.exit(0)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)

