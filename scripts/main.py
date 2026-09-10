import discord
from discord.ext import commands
from command_functions import run_command, create_shell, find_shell_type
import subprocess
import logging
from load_env import get_token, get_perm_role_id, get_non_role_view
from make_bot import make_bot
import sys

token = get_token()
perm_role_id = get_perm_role_id()
non_role_view = get_non_role_view()

bot , handler = make_bot()

shell_path = find_shell_type()

shells = {}
commands_list = ["!start","!exit","!stop"]

@bot.event
async def on_ready():
    print("Ready")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return 

    if message.channel.id in shells and message.content not in commands_list:
        await run_command(message, message.channel.id, shells)

    await bot.process_commands(message)


@bot.command()
async def start(ctx):
    if await check_role(ctx):

        if ctx.channel.id in shells:
            await ctx.send("This command cannot be executed in a shell channel")
            return
        
        overwrites = {}
        if non_role_view == False:
            perm_role_obj = ctx.guild.get_role(int(perm_role_id))
            overwrites = { ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                            perm_role_obj: discord.PermissionOverwrite(view_channel=True, send_messages=True)}
            
        channel = await ctx.guild.create_text_channel(name="shell", overwrites=overwrites)
        await ctx.send(f"{ctx.author.mention} - New shell: {channel.mention}")

        print(shell_path)
        shells[channel.id] = create_shell(shell_path)

@bot.command()
async def exit(ctx):
    if await check_role(ctx):
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
    if await check_role(ctx):
        if ctx.channel.id in shells:
            await ctx.channel.send("This command cannot be executed in a shell channel")
        else:
            await ctx.channel.send("Stopping Exdis")
            sys.exit(0)

async def check_role(message):
    for role in message.author.roles:
        if(str(role.id) == str(perm_role_id)):
            return True
    await message.channel.send(f"{message.author.mention} You do not have permission to use Exdis")
    return False


bot.run(token, log_handler=handler, log_level=logging.DEBUG)

