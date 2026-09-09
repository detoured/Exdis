import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import subprocess
import sys

shells = {}

async def run_command(message, id):
        command = message.content + "\necho __EXDIS_COMMAND_DONE__\n"

        shells[id].stdin.write(command.encode())
        shells[id].stdin.flush()

        output = []

        while True:
            line = shells[id].stdout.readline()

            if not line:
                break

            if line.strip() == b"__EXDIS_COMMAND_DONE__":
                break

            output.append(line)

        result = b"".join(output)
        if result:
            await message.channel.send(f"```{result.decode('utf-8')}```")
        else:
            await message.add_reaction("✅")

def create_shell():
    shell = subprocess.Popen(
    ["/bin/bash"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    shell=True
    )
    
    return shell


load_dotenv()
token = os.getenv('DISCOED_TOKEN')

handler = logging.FileHandler(filename="bot.log",encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    print("Ready")



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return 

    if message.channel.id in shells and message.content[0] != "!":
        await run_command(message, message.channel.id)

    await bot.process_commands(message)


@bot.command()
async def start(ctx):
    if ctx.channel.id in shells:
        await ctx.send("This command cannot be executed in a shell channel")
        return
    channel = await ctx.guild.create_text_channel(name="shell")
    await ctx.send(f"{ctx.author.mention} - New shell: {channel.mention}")
    shells[channel.id] = create_shell()

@bot.command()
async def exit(ctx):
    if ctx.channel.id in shells:
        shells[ctx.channel.id].terminate()
        
        try:
            shells[ctx.channel.id].wait(timeout=3)
        except subprocess.TimeoutExpired:
            shells[ctx.channel.id].kill()
            
        del shells[ctx.channel.id]
        await ctx.channel.delete()

      
    else:
        await ctx.send("This command cannot be executed outside of a shell channel")

@bot.command()
async def stop(ctx):
    if ctx.channel.id in shells:
        await ctx.channel.send("This command cannot be executed in a shell channel")
    else:
        await ctx.channel.send("Stopping Exdis")
        sys.exit(0)



       


bot.run(token, log_handler=handler, log_level=logging.DEBUG)