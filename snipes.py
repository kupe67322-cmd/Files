import discord
from discord.ext import commands
import asyncio
import string
import itertools
from datetime import datetime
import os # Necessary for Railway environment variables

# --- SETTINGS ---
# Use Railway's environment variables for security
TOKEN = os.getenv('DISCORD_TOKEN')
TARGET_CHANNEL = 'snipe' 
PREFIX = '!'
BATCH_SIZE = 5 
# ----------------

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
searching = False

async def check_name(name):
    try:
        await bot.fetch_user(name)
        return {"name": name, "status": "nawh", "color": 0xe74c3c}
    except discord.NotFound:
        return {"name": name, "status": "available", "color": 0x2ecc71}
    except discord.HTTPException as e:
        if e.status == 429:
            return "RETRY"
        return {"name": name, "status": "error", "color": 0x95a5a6}

async def start_spammer(ctx, length):
    global searching
    searching = True
    
    channel = discord.utils.get(ctx.guild.text_channels, name=TARGET_CHANNEL)
    if not channel:
        await ctx.send(f"⚠️ Channel `{TARGET_CHANNEL}` not found.")
        return

    init = discord.Embed(
        title="🛰️ Scan Started",
        description=f"Checking **{length}** char combos.",
        color=0x3498db
    )
    await channel.send(embed=init)
    
    chars = string.ascii_lowercase + string.digits
    combo_gen = itertools.product(chars, repeat=length)
    
    while searching:
        batch = []
        for _ in range(BATCH_SIZE):
            try:
                combo = next(combo_gen)
                batch.append("".join(combo))
            except StopIteration:
                searching = False
                break
        
        if not batch: break

        tasks = [check_name(name) for name in batch]
        results = await asyncio.gather(*tasks)

        for res in results:
            if res == "RETRY":
                await asyncio.sleep(5) # Longer sleep for Railway stability
                continue
          
            embed = discord.Embed(
                title=f"Target: {res['name']}",
                color=res['color'],
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="Result", value=f"**{res['status']}**")
            
            try:
                await channel.send(embed=embed)
            except:
                await asyncio.sleep(1)

        await asyncio.sleep(1.2) # Keeping it chill for the host

@bot.command()
async def check3(ctx):
    if not searching: await start_spammer(ctx, 3)

@bot.command()
async def check4(ctx):
    if not searching: await start_spammer(ctx, 4)

@bot.command()
async def stop(ctx):
    global searching
    searching = False
    await ctx.send("🛑 **Search Halted.**")

# Handle missing token error
if TOKEN is None:
    print("Error: DISCORD_TOKEN variable not found in Railway settings.")
else:
    bot.run(TOKEN)
