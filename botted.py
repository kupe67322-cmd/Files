import discord
from discord import app_commands, ui
import asyncio
import sys
import os

# --- CONFIG ---
TOKEN = "" 
OWNER_ID = 1429477060577067019

class FloodButton(ui.View):
    def __init__(self, message_content):
        super().__init__(timeout=None)
        self.msg = message_content

    @ui.button(label="press2fludz (5x)", style=discord.ButtonStyle.danger)
    async def flood_button(self, interaction: discord.Interaction, button: ui.Button):
        # FIXED: Tell Discord we received the click immediately
        await interaction.response.defer(ephemeral=True)
        
        for _ in range(5):
            try:
                # Use followup for global external sending
                await interaction.followup.send(self.msg)
                await asyncio.sleep(0.03)
            except:
                break

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.tree = app_commands.CommandTree(self)
        self.whitelist = {
            OWNER_ID, 
            292895476485980161,
            980778884767318046,
            741607657521020989, 
            1251370888830390386, 
            1394753272492851322
        } 

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Online. Whitelisted: {len(self.whitelist)}")

bot = MyBot()

def is_whitelisted(i: discord.Interaction):
    return i.user.id in bot.whitelist

@bot.tree.command(name="flood", description="cry")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def flood(i: discord.Interaction, message: str):
    if not is_whitelisted(i):
        return await i.response.send_message("luhh, no perms haha", ephemeral=True)
    
    view = FloodButton(message)
    await i.response.send_message(
        content="## Control Panel\nJoin for more:\nhttps://discord.gg/rougekin\nhttps://discord.gg/bZDFTVHC7", 
        view=view, 
        ephemeral=True
    )

@bot.tree.command(name="say", description="haha pasikat ohh")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def say(i: discord.Interaction, message: str):
    if not is_whitelisted(i): return
    await i.response.send_message("...", ephemeral=True)
    try:
        await i.followup.send(message)
    except:
        pass

bot.run(TOKEN)
