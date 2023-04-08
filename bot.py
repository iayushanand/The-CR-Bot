import discord
from discord.ext import commands, tasks


import config
from mcrcon import MCRcon

import asyncio
from discord import Embed

import time
from random import choice

import datetime
import psutil

import os
import sys

from multicraftapi import MulticraftAPI
import datetime

bot = commands.Bot(
    command_prefix=',',
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions(
        everyone=False,
        roles=False
    ),
    case_insensitive=True
)

bot.start_time = int(time.time())

@bot.event
async def on_ready():
    print('Logged in as: {0.user.name} - {0.user.id}'.format(bot))
    print('Latency: {0}ms', format(round(bot.latency*1000)))
    print('------')
    status.start()

@bot.event
async def on_command_error(ctx,error):
    raise error


def embed_(context: commands.Context, action, logs, terminal):
    em = Embed(
        title=f'{action} Log:',
        description=f'{logs}',
        color=0x2F3136
    ).add_field(
        name="TERMINAL 💻:",
        value=f'```{terminal}```',
        inline=False
    ).add_field(
        name=" ",
        value=f"[cmd msg]({context.message.jump_url})",
        inline=False
    )
    return em

def connect() -> MCRcon:
    mcr = MCRcon(host=config.ip, port=config.port, password=config.password)
    try:
        mcr.connect()
        return mcr
    except:
        return None

################################################################################################################
#                                                                                                              #
#                                                                                                              #
#                                              USING THE                                                       #
#                                            MULTICRAFT API                                                    #
#                                         FOR START AND STOP                                                   #
#                            NOTE: I will recommend using rcon for all possible stuffs                         #
#                                                                                                              #
################################################################################################################

client = MulticraftAPI(url=config.api_url, username=config.api_user , api_key=config.api_key)



@bot.command(name="start",help="Starts the server")
@commands.has_role(config.mod)
async def start(ctx):
    response = client("startServer", config.server_id)
    if response['success'] == True:
        await ctx.reply("Server Started!")
    else:
        log_channel = await bot.fetch_channel(config.log)
        res = embed_(ctx, "Start", f"Failed to start server by {str(ctx.author)}", response)
        await log_channel.send(embed=res)
        await ctx.reply("Failed to start server! Check logs for more info")


@bot.command(name="stop",help="Stops the server")
@commands.has_role(config.mod)
async def stop(ctx):
    response = client("stopServer", config.server_id)
    if response['success'] == True:
        await ctx.reply("Server Stoped!")
    else:
        log_channel = await bot.fetch_channel(config.log)
        res = embed_(ctx, "Stop", f"Failed to stop server by {str(ctx.author)}", response)
        await log_channel.send(embed=res)
        await ctx.reply("Failed to stop server! Check logs for more info")
    
@bot.command(name="restart",help="Restart the server")
@commands.has_role(config.mod)
async def restart(ctx):
    response = client("restartServer", config.server_id)
    if response['success'] == True:
        await ctx.reply("Server Restarted!")
    else:
        log_channel = await bot.fetch_channel(config.log)
        res = embed_(ctx, "Retart", f"Failed to restart server by {str(ctx.author)}", response)
        await log_channel.send(embed=res)
        await ctx.reply("Failed to restart server! Check logs for more info")



################################################################################################################
#                                                                                                              #
#                                              USING THE                                                       #
#                                               MC RCON                                                        #
#                                        FOR EVERYTHING ELSE                                                   #
#                                                                                                              #
################################################################################################################



@bot.command(name='say', help='Sends a message from the server side')
@commands.has_role(config.mod)
async def say(ctx, *, message):
    mcr = connect()
    if not mcr: return await ctx.reply("Can't connect with Rcon!")
    res = mcr.command(f'say {message}')
    mcr.disconnect()
    
    res = embed_(ctx, "Server", f"Sent: `{message}` by {str(ctx.author)}", res)
    await ctx.add_reaction('✅')
    log_channel = await bot.fetch_channel(config.log)
    await log_channel.send(embed=res)
    


@bot.command(name='kick', help='Kicks a player from the server')
@commands.has_role(config.mod)
async def kick(ctx, player: str, *, reason: str = None):
    if not reason:
        reason = "mf kicked without reason"
    mcr = connect()
    if not mcr: return await ctx.reply("Can't connect with Rcon!")
    res = mcr.command(f'kick {player} {reason}')
    mcr.disconnect()
    
    embed = embed_(ctx, "Kick", f"Kicked: by {str(ctx.author)}", res)
    await ctx.reply(f'Kicked! `{player}`')
    log_channel = await bot.fetch_channel(config.log)
    await log_channel.send(embed=embed)

@bot.command(name='ban', help='Bans a player from the server')
@commands.has_role(config.mod)
async def ban(ctx, player: str, *, reason: str = None):
    mcr = connect()
    if not mcr: return await ctx.reply("Can't connect with Rcon!")
    if not reason:
        reason = "mf banned without reason"
    mcr.disconnect()
    res = mcr.command(f'ban {player} {reason}')
    
    embed = embed_(ctx, "Ban", f"Banned: by {str(ctx.author)}", res)
    await ctx.reply(f'Banned! `{player}`')
    log_channel = await bot.fetch_channel(config.log)
    await log_channel.send(embed=embed)


@bot.command(name='unban', help='Unbans a player from the server')
@commands.has_role(config.mod)
async def unban(ctx, player: str):
    mcr = connect()
    if not mcr: return await ctx.reply("Can't connect with Rcon!")
    res = mcr.command(f'pardon {player}')
    mcr.disconnect()
    
    embed = embed_(ctx, "Unban", f"Unbanned: by {str(ctx.author)}", res)
    await ctx.reply(f'Unbanned! `{player}`')
    log_channel = await bot.fetch_channel(config.log)
    await log_channel.send(embed=embed)

@bot.command(name='op', help='Gives a player operator status')
@commands.has_role(config.mod)
async def op(ctx, *, player: str):
    mcr = connect()
    if not mcr: return await ctx.reply("Can't connect with Rcon!")
    res = mcr.command(f'op {player}')
    mcr.disconnect()
    
    embed = embed_(ctx, "Op", f"Opped: by {str(ctx.author)}", res)
    await ctx.reply(f'Gave `{player}` operator status!')
    log_channel = await bot.fetch_channel(config.log)
    await log_channel.send(embed=embed)

@bot.command(name='deop', help='Takes a player operator status')
@commands.has_role(config.mod)
async def deop(ctx, *, player: str):
    mcr = connect()
    if not mcr: return await ctx.reply("Can't connect with Rcon!")
    res = mcr.command(f'deop {player}')
    mcr.disconnect()
    
    embed = embed_(ctx, "Deop", f"Deopped: by {str(ctx.author)}", res)
    await ctx.reply(f'Took `{player}` operator status!')
    log_channel = await bot.fetch_channel(config.log)
    await log_channel.send(embed=embed)



@bot.command(name='whitelist', help='Whitelists a player')
@commands.has_role(config.mod)
async def whitelist(ctx, *, player: str):
    mcr = connect()
    if not mcr: return await ctx.reply("Can't connect with Rcon!")
    res = mcr.command(f'whitelist add {player}')
    mcr.disconnect()
    
    await ctx.reply(f'Whitelisted `{player}`!')
    embed = embed_("Whitelist", f"Whitelisted: by {str(ctx.author)}", res)
    log_channel = await bot.fetch_channel(config.log)
    await log_channel.send(embed=embed)


@bot.command(name='unlist',help='Remove someone fron whitelist')
@commands.has_role(config.mod)
async def whitelist_(ctx, *, player: str):
    mcr = connect()
    if not mcr: return await ctx.reply("Can't connect with Rcon!")
    res = mcr.command(f'whitelist remove {player}')
    mcr.disconnect()
    
    await ctx.reply(f'Unlisted `{player}`!')
    embed = embed_("Whitelist", f"Unlisted: by {str(ctx.author)}", res)
    log_channel = await bot.fetch_channel(config.log)
    await log_channel.send(embed=embed)


@bot.command(name='custom', help='Runs a custom command', aliases=['cmd'])
@commands.has_role(config.mod)
async def custom(ctx, *, command: str):
    mcr = connect()
    if not mcr: return await ctx.reply("Can't connect with Rcon!")
    res = mcr.command(f'{command}')
    mcr.disconnect()
    log_channel = await bot.fetch_channel(config.log)
    
    await ctx.reply(f'Command ran: `{command}` check {log_channel.mention} for output.')
    embed = Embed(
        title="Terminal Output.",
        description=f"```\n{res}\n```",
        color=discord.Color.og_blurple()
    ).add_field(
        name=" ",
        value=f"[cmd msg]({ctx.message.jump_url})"
    )
    await log_channel.send(embed=embed)



################################################################################################################
#                                                                                                              #
#                                           GENERAL COMMANDS                                                   #
#                                                                                                              #
################################################################################################################


@bot.command(name="ping", help="Returns bot latency")
async def ping(ctx):
    await ctx.reply(
        embed = discord.Embed(
            title = "🏓 Pong!",
            description= f"{round(bot.latency*1000)}ms",
            color=0xffffff
        )
    )

@bot.command(name="uptime", help="Shows bot uptime")
async def uptime(ctx: commands.Context):
    uptime = datetime.timedelta(seconds=int(time.time() - bot.start_time))
    await ctx.reply(
        embed = discord.Embed(
            title = "🕒 Uptime",
            description = f"{uptime.days}days(s), {uptime.seconds//3600}hour(s), {(uptime.seconds//60)%60}minute(s), {uptime.seconds%60}second(s)",
            color=0xffffff
        )
    )


# get usage in gigabytes

@bot.command(name="status", help="Shows bot server status")
async def status(ctx: commands.Context):
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    disk_total = round(psutil.disk_usage('/').total / 1024 ** 3)
    disk_used  = round(psutil.disk_usage('/').used / 1024 ** 3)
    disk_free = round(psutil.disk_usage('/').free / 1024 ** 3)
    process  = len(psutil.pids())
    python_version = sys.version
    discord_version = discord.__version__
    uptime = datetime.timedelta(seconds=int(time.time() - bot.start_time))
    embed = discord.Embed(
        description="Server Status",
        color=0xffffff,
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(
        name="<:CPU:1016016795909488651> CPU",
        value=f"{cpu}%",
    )

    embed.add_field(
        name="<:memory:1016016586584363079> Memory",
        value=f"{ram}%",
    )

    embed.add_field(
        name="<a:disk:1094229488239378573> Disk",
        value=f"{disk_percent}%\nFree: {disk_free} Gib\nUsed: {disk_used} Gib\nTotal: {disk_total} Gib",
    )
    
    embed.add_field(
        name="<:python:1016025084789530714> Python Version",
        value=f"{python_version}",
    )

    embed.add_field(
        name="<:discord:1016027358731456582> Pycord Version",
        value=f"{discord_version}",
    )

    embed.add_field(
        name = "<a:uptime:1094230464690147440> Uptime",
        value = f"{uptime.days}days(s), {uptime.seconds//3600}hour(s), {(uptime.seconds//60)%60}minute(s), {uptime.seconds%60}second(s)",
    )

    await ctx.reply(embed=embed)


@tasks.loop(minutes=10)
async def status():
    statues = ["Minecraft", "Poopers pooping", "NLuziaf is a god", "myself", "Better than CBV6 😏", "join: tcr.mcserver.us", "The CR SMP",
            "Lava Walker", "Jesus Boots", "Lexionas74 vibing", "for Swas.py", "ports and boats", "Lexi killing Ghast", "Conch", "smp mods", "chunck claimers",
            "floating and goating", "Zombie", "deaths", "#JusticeForTCA", "v1.19.2", "myself simping for Bob", "Arthex without life", "Swas.py writing exams",
            "G.O.A.T. 🐐", "Pixel Pioneers on islands", "Saucee with hot sauce", "Shrines for magic", "Conch killing sheep", "goat horns", "TCR", "Skeleton",
            "Ghast", "weak Withers", "Lexionas74 stealing dragon egg", "[Acquire Hardware]", "[Ice-Bucket Challenge]", "you!", "Useless TCR staffs", "#admin-nsfw",
            "pooping in a sock", "resummon the dragon", "Dragon Egg(s)", "BobDotHot", "flicko afk-ing", "diamonds",
        ]
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=choice(statues)))


bot.run(config.token)
