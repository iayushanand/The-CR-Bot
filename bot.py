import discord
from discord.ext import commands, tasks


import config
from mcrcon import MCRcon

import asyncio
from discord import Embed

from random import choice

bot = commands.Bot(
    command_prefix=',',
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions(
        everyone=False,
        roles=False
    ),
    case_insensitive=True
)

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


mcr = MCRcon(host=config.ip, port=config.port, password=config.password)
mcr.connect()

@bot.command(name='say', help='Sends a message from the server side')
@commands.has_role(config.mod)
async def say(ctx, *, message):
    res = mcr.command(f'say {message}')
    # print(res)
    res = embed_(ctx, "Server", f"Sent: `{message}` by {str(ctx.author)}", res)
    await ctx.add_reaction('✅')
    log_channel = await bot.fetch_channel(config.log)
    await log_channel.send(embed=res)
    

@bot.command(name='kick', help='Kicks a player from the server')
@commands.has_role(config.mod)
async def kick(ctx, player: str, *, reason: str = None):
    if not reason:
        reason = "mf kicked without reason"
    res = mcr.command(f'kick {player} {reason}')
    # print(res)
    embed = embed_(ctx, "Kick", f"Kicked: by {str(ctx.author)}", res)
    await ctx.reply(f'Kicked! `{player}`')
    log_channel = await bot.fetch_channel(config.log)
    await log_channel.send(embed=embed)

@bot.command(name='ban', help='Bans a player from the server')
@commands.has_role(config.mod)
async def ban(ctx, player: str, *, reason: str = None):
    if not reason:
        reason = "mf banned without reason"
    res = mcr.command(f'ban {player} {reason}')
    # print(res)
    embed = embed_(ctx, "Ban", f"Banned: by {str(ctx.author)}", res)
    await ctx.reply(f'Banned! `{player}`')
    log_channel = await bot.fetch_channel(config.log)
    await log_channel.send(embed=embed)


@bot.command(name='unban', help='Unbans a player from the server')
@commands.has_role(config.mod)
async def unban(ctx, player: str):
    res = mcr.command(f'pardon {player}')
    # print(res)
    embed = embed_(ctx, "Unban", f"Unbanned: by {str(ctx.author)}", res)
    await ctx.reply(f'Unbanned! `{player}`')
    log_channel = await bot.fetch_channel(config.log)
    await log_channel.send(embed=embed)

@bot.command(name='op', help='Gives a player operator status')
@commands.has_role(config.mod)
async def op(ctx, *, player: str):
    res = mcr.command(f'op {player}')
    # print(res)
    embed = embed_(ctx, "Op", f"Opped: by {str(ctx.author)}", res)
    await ctx.reply(f'Gave `{player}` operator status!')
    log_channel = await bot.fetch_channel(config.log)
    await log_channel.send(embed=embed)

@bot.command(name='deop', help='Takes a player operator status')
@commands.has_role(config.mod)
async def deop(ctx, *, player: str):
    res = mcr.command(f'deop {player}')
    # print(res)
    embed = embed_(ctx, "Deop", f"Deopped: by {str(ctx.author)}", res)
    await ctx.reply(f'Took `{player}` operator status!')
    log_channel = await bot.fetch_channel(config.log)
    await log_channel.send(embed=embed)


# flicko told won't work so I removed

# @bot.command(name='start', help='Starts the server')
# @commands.has_role(config.mod)
# async def start(ctx):
#     res = mcr.command('start')
#     await ctx.reply('Server starting...')
#     embed = embed_(ctx, "Start", f"Started: by {str(ctx.author)}", res)
#     log_channel = await bot.fetch_channel(config.log)
#     await log_channel.send(embed=embed)

@bot.command(name='stop', help='Stops the server')
@commands.has_role(config.mod)
async def stop(ctx):
    res = mcr.command('stop')
    # print(res)
    await ctx.reply('Server stopping...')
    embed = embed_(ctx, "Stop", f"Stopped: by {str(ctx.author)}", res)
    log_channel = await bot.fetch_channel(config.log)
    await log_channel.send(embed=embed)


# flicko told won't work so I removed

# @bot.command(name='restart', help='Restarts the server')
# @commands.has_role(config.mod)
# async def restart(ctx):
#     res = mcr.command('restart')
#     # print(res)
#     await ctx.reply('Server restarting...')
#     embed = embed_(ctx, "Restart", f"Restarted: by {str(ctx.author)}", res)
#     log_channel = await bot.fetch_channel(config.log)
#     await log_channel.send(embed=embed)


@bot.command(name='whitelist', help='Whitelists a player')
@commands.has_role(config.mod)
async def whitelist(ctx, *, player: str):
    res = mcr.command(f'whitelist add {player}')
    # print(res)
    await ctx.reply(f'Whitelisted `{player}`!')
    embed = embed_("Whitelist", f"Whitelisted: by {str(ctx.author)}", res)
    log_channel = await bot.fetch_channel(config.log)
    await log_channel.send(embed=embed)


@bot.command(name='unlist',help='Remove someone fron whitelist')
@commands.has_role(config.mod)
async def whitelist_(ctx, *, player: str):
    res = mcr.command(f'whitelist remove {player}')
    # print(res)
    await ctx.reply(f'Unlisted `{player}`!')
    embed = embed_("Whitelist", f"Unlisted: by {str(ctx.author)}", res)
    log_channel = await bot.fetch_channel(config.log)
    await log_channel.send(embed=embed)


@bot.command(name='custom', help='Runs a custom command')
@commands.has_role(config.mod)
async def custom(ctx, *, command: str):
    res = mcr.command(f'{command}')
    # print(res)
    await ctx.reply(f'Command ran: `{command}` check {log_channel.mention} for output.')
    embed = Embed(
        title="Terminal Output.",
        description=f"```\n{res}\n```",
        color=discord.Color.og_blurple()
    ).add_field(
        name=" ",
        value=f"[cmd msg]({ctx.message.jump_url})"
    )
    log_channel = await bot.fetch_channel(config.log)
    await log_channel.send(embed=embed)


@bot.command(name="ping", help="Returns bot latency")
async def ping(ctx):
    await ctx.reply(
        embed = discord.Embed(
            title = "🏓 Pong!",
            description= f"{round(bot.latency*1000)}ms",
            color=0xffffff
        )
    )

@tasks.loop(minutes=5)
async def status():
    statues = ["Minecraft", "Poopers pooping", "NLuziaf is a god", "myself", "Better than CBV6 😏", "join: tcr.mcserver.us", "The CR SMP",
            "Lava Walker", "Jesus Boots", "Lexionas74 vibing", "for Swas.py", "ports and boats", "Lexi killing Ghast", "Conch", "smp mods", "chunck claimers",
            "floating and goating", "Zombie", "deaths", "#JusticeForTCA", "v1.19.2", "myself simping for Bob", "Arthex without life", "Swas.py writing exams",
            "G.O.A.T. 🐐", "Pixel Pioneers on islands", "Saucee with hot sauce", "Shrines for magic", "Conch killing sheep", "goat horns", "TCR", "Skeleton",
            "Ghast", "weak Withers", "Lexionas74 stealing dragon egg", "[Acquire Hardware]", "[Ice-Bucket Challenge]", "you!", "Useless TCR staffs", "#admin-nsfw",
            "pooping in a sock", "resummon the dragon", "Dragon Egg(s)", "BobDotHot", "flicko afk-ing", "diamonds",
        ]
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=choice(statues)))

# Bob told to change to bot.run instead so I did

bot.run(config.token)