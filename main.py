import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils.database import db
from utils.emojis import load_emojis
from utils.utils import cycle_status

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)

load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("Missing TOKEN environment variable.")

_extensions_loaded = False


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if not filename.endswith(".py"):
            continue
        extension = f"cogs.{filename[:-3]}"
        if extension not in client.extensions:
            await client.load_extension(extension)


@client.event
async def on_ready():
    global _extensions_loaded

    if not _extensions_loaded:
        await load_extensions()
        _extensions_loaded = True

        # Lazy imports to register persistent views once
        from cogs.acc_panel import Accs
        from cogs.views import CashInLayout, MarkSoldLayout, Pending
        from cogs.help import HelpV2
        from cogs.setup import SetupV2, SetupButton
    
        client.add_view(Accs(None))
        client.add_view(Pending(None, None, None, None))
        client.add_view(MarkSoldLayout(None, None, None))
        client.add_view(CashInLayout(None, None, None))
        client.add_view(HelpV2())
        client.add_view(SetupV2(None))

    emoji_count = await load_emojis(client)
    client.loop.create_task(cycle_status(client))

    global_command_count = 0
    try:
        synced_global = await client.tree.sync()
        global_command_count = len(synced_global)
    except Exception as e:
        print(f"Failed to sync global commands: {e}")

    # Guild sync (optional, does not affect summary)
    try:
        guild = discord.Object(id=1325056936231571486)  # Replace with your guild ID
        await client.tree.sync(guild=guild)
    except Exception as e:
        print(f"Failed to sync guild commands: {e}")

    db_status = "Connected"
    try:
        db.admin.command("ping")
    except Exception as e:
        db_status = f"Failed ({e})"

    print("=" * 50)
    print(f"{client.user.name} Startup Summary")
    if client.user:
        print(f"Bot: {client.user} (ID: {client.user.id})")
    print(f"Emojis Loaded: {emoji_count}")
    print(f"Global Commands Loaded: {global_command_count}")
    print(f"Database Connection: {db_status}")
    print("=" * 50)

client.run(TOKEN)
