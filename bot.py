import discord
import os
import asyncio
import subprocess
import sys
import logging

def install_requirements():
    try:
        import nacl
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyNaCl"])

install_requirements()

TARGET_VC_ID = os.getenv('VC_ID') 

TOKENS = [
    os.getenv('USER_TOKEN_1'), 
    os.getenv('USER_TOKEN_2'),
    os.getenv('USER_TOKEN_3'), 
    os.getenv('USER_TOKEN_4'),
    os.getenv('USER_TOKEN_5'), 
    os.getenv('USER_TOKEN_6'),
    os.getenv('USER_TOKEN_7'), 
    os.getenv('USER_TOKEN_8')
]

logging.getLogger('discord').setLevel(logging.CRITICAL)

class SafePermanentAnchor(discord.Client):
    def __init__(self, vc_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_vc_id = int(vc_id) if vc_id else None
        self.is_reconnecting = False

    async def on_ready(self):
        print(f"LOGGED IN: {self.user} (ID: {self.user.id})")
        await asyncio.sleep(2)
        await self.join_vc()

    async def join_vc(self):
        if self.is_reconnecting or not self.target_vc_id:
            return

        self.is_reconnecting = True
        try:
            channel = await self.fetch_channel(self.target_vc_id)

            if self.voice_clients:
                for vc in self.voice_clients:
                    if vc.channel.id == self.target_vc_id:
                        print(f"[{self.user}] Already in target channel.")
                        self.is_reconnecting = False
                        return
                    await vc.disconnect()

            print(f"[{self.user}] Joining {channel.name}...")
            await channel.connect(self_deaf=False, self_mute=True, reconnect=True)
            print(f"[{self.user}] SESSION LOCKED")
        except Exception as e:
            print(f"[{self.user}] Join failed: {e}")
            await asyncio.sleep(30) 
        finally:
            self.is_reconnecting = False

    async def on_voice_state_update(self, member, before, after):
        if member.id == self.user.id and after.channel is None:
            if not self.is_reconnecting:
                print(f"[{self.user}] Disconnected. Reconnecting in 10s...")
                await asyncio.sleep(10) 
                await self.join_vc()

async def start_bots():
    valid_tokens = [t for t in TOKENS if t]

    if not TARGET_VC_ID or not valid_tokens:
        print("ERROR: Missing VC_ID or TOKENS.")
        return

    print(f"Launching {len(valid_tokens)} account(s)...")

    active_tasks = []
    for token in valid_tokens:
        client = SafePermanentAnchor(
            vc_id=TARGET_VC_ID,
            heartbeat_timeout=60.0
        )
        active_tasks.append(client.start(token))

    await asyncio.gather(*active_tasks)

if __name__ == "__main__":
    try:
        asyncio.run(start_bots())
    except KeyboardInterrupt:
        print("Process stopped.")
    except Exception as e:
        print(f"FATAL ERROR: {e}")
