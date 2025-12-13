import os
import re
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

async def auto_update_views():
    """Automatically update all views on bot restart by scanning categories"""
    print("🔄 Auto-updating views by scanning categories...")
    
    updated_count = 0
    
    # Scan all guilds
    for guild in client.guilds:
        print(f"📋 Scanning guild: {guild.name}")
        
        # Update account panel
        updated_count += await update_account_panel(guild)
        
        # Update channels in account categories
        updated_count += await update_account_channels(guild)
    
    print(f"✅ Auto-update complete: {updated_count} views updated")

async def update_account_panel(guild):
    """Find and update the account panel in the panel category"""
    from utils.storage import get_panel_channel_id
    from cogs.acc_panel import Accs
    
    # Method 1: Try to get from storage
    panel_channel_id = get_panel_channel_id(guild.id)
    if panel_channel_id:
        channel = guild.get_channel(panel_channel_id)
        if channel:
            try:
                # Update all messages in the panel channel
                updated = await update_messages_in_channel(channel, "acc_panel", guild.id)
                if updated > 0:
                    print(f"  ✅ Updated account panel from storage in #{channel.name}")
                    return updated
            except Exception as e:
                print(f"  ⚠️ Couldn't update panel from storage: {e}")
    
    # Method 2: Search for panel category
    panel_category = discord.utils.get(guild.categories, name="📌 Panel")
    if panel_category:
        for channel in panel_category.text_channels:
            if "panel" in channel.name.lower() or "لوحة" in channel.name:
                try:
                    updated = await update_messages_in_channel(channel, "acc_panel", guild.id)
                    if updated > 0:
                        print(f"  ✅ Found and updated panel in #{channel.name}")
                        return updated
                except Exception as e:
                    print(f"  ⚠️ Error updating panel in #{channel.name}: {e}")
    
    # Method 3: Search all channels
    for channel in guild.text_channels:
        if channel.name in ["📮-account-panel", "account-panel", "لوحة-الحسابات"]:
            try:
                updated = await update_messages_in_channel(channel, "acc_panel", guild.id)
                if updated > 0:
                    print(f"  ✅ Found panel by name in #{channel.name}")
                    return updated
            except Exception as e:
                print(f"  ⚠️ Error updating panel in #{channel.name}: {e}")
    
    return 0

async def update_account_channels(guild):
    """Find and update all account channels in account categories"""
    # List of account categories to scan
    account_categories = [
        "Pending 🔃",
        "For Sale 🏷️", 
        "Sold 📦",
        "Banned ⛔",
        "Paid 💰"
    ]
    
    updated_count = 0
    
    for category_name in account_categories:
        category = discord.utils.get(guild.categories, name=category_name)
        if category:
            print(f"  🔍 Scanning category: {category_name}")
            
            # Get all text channels in this category
            for channel in category.text_channels:
                try:
                    # Update all messages with views in this channel
                    updated = await update_account_channel_messages(channel, guild.id)
                    if updated > 0:
                        print(f"    ✅ Updated {updated} view(s) in #{channel.name}")
                        updated_count += updated
                except Exception as e:
                    print(f"    ⚠️ Error in #{channel.name}: {e}")
    
    return updated_count

async def update_account_channel_messages(channel, guild_id):
    """Update all messages with views in an account channel"""
    updated = 0
    
    try:
        # Get ALL messages (no limit)
        messages = []
        async for message in channel.history(limit=None):
            messages.append(message)
        
        # Process messages from oldest to newest (reverse the list)
        messages.reverse()
        
        for message in messages:
            if message.components:
                # Extract data BEFORE updating
                view_data = extract_view_data_from_message(message, channel.category.name)
                if view_data:
                    # Update the message with extracted data
                    success = await update_message_with_data(message, view_data, guild_id)
                    if success:
                        updated += 1
                        
    except discord.Forbidden:
        print(f"    ⛔ No permission to read #{channel.name}")
    except Exception as e:
        print(f"    ⚠️ Error reading #{channel.name}: {e}")
    
    return updated

def extract_view_data_from_message(message, category_name):
    """Extract ALL data from a message to preserve it during update"""
    try:
        # Get the view type first
        view_type = None
        if category_name == "Pending 🔃":
            view_type = "pending"
        elif category_name == "For Sale 🏷️":
            view_type = "mark_sold"
        elif category_name == "Sold 📦":
            view_type = "cash_in"
        elif category_name == "Paid 💰":
            return None  # Paid views are static, don't update
        elif category_name == "Banned ⛔":
            return None  # Banned views are static, don't update
        
        if not view_type:
            return None
        
        # Extract user ID from message content (looking for <@UID>)
        uid = None
        try:
            # Try to get from message content first
            if message.content:
                match = re.search(r'<@(\d+)>', message.content)
                if match:
                    uid = int(match.group(1))
            
            # If not in content, try to extract from components
            if not uid and message.components:
                # Look for TextDisplay with mention
                for component in message.components:
                    if hasattr(component, 'children'):
                        for child in component.children:
                            if hasattr(child, 'content') and '<@' in str(child.content):
                                match = re.search(r'<@(\d+)>', str(child.content))
                                if match:
                                    uid = int(match.group(1))
                                    break
                    if uid:
                        break
        except:
            uid = None
        
        # Extract account content - this is CRITICAL
        acc_content = ""
        try:
            # Look for account content in TextDisplay components
            if message.components:
                for component in message.components:
                    if hasattr(component, 'children'):
                        for child in component.children:
                            if hasattr(child, 'content'):
                                content_str = str(child.content)
                                # Look for account content (code blocks or specific patterns)
                                if '```' in content_str:
                                    # Extract from code blocks
                                    matches = re.findall(r'```(.*?)```', content_str, re.DOTALL)
                                    if matches:
                                        acc_content = matches[0].strip()
                                        break
                                elif content_str and len(content_str) > 20:
                                    # Might be account content without code blocks
                                    # Check if it looks like account info (has newlines or specific patterns)
                                    if '\n' in content_str or ':' in content_str:
                                        acc_content = content_str
                                        break
                    if acc_content:
                        break
        except:
            acc_content = ""
        
        # Extract game type from channel name
        game = "bo7"  # Default
        try:
            channel_name = message.channel.name.lower()
            if "bo7" in channel_name or "black ops" in channel_name:
                game = "bo7"
            elif "ow2" in channel_name or "overwatch" in channel_name:
                game = "ow2"
            elif "rivals" in channel_name:
                game = "rivals"
            elif "bf6" in channel_name or "battlefield" in channel_name:
                game = "battlefield6"
            elif "wz" in channel_name or "warzone" in channel_name:
                game = "warzone"
        except:
            game = "bo7"
        
        return {
            "type": view_type,
            "uid": uid,
            "acc": acc_content,
            "game": game
        }
        
    except Exception as e:
        print(f"    ⚠️ Error extracting view data: {e}")
        return None

async def update_message_with_data(message, view_data, guild_id):
    """Update a message with the appropriate view using extracted data"""
    try:
        from cogs.views import Pending, MarkSoldLayout, CashInLayout
        
        view_type = view_data["type"]
        uid = view_data.get("uid")
        acc_content = view_data.get("acc", "")
        game = view_data.get("game", "bo7")
        
        if view_type == "pending":
            if uid:
                new_view = Pending(guild_id, uid, acc_content, game)
                await message.edit(view=new_view)
                return True
            else:
                print(f"    ⚠️ Skipping pending view - no user ID found")
                return False
                
        elif view_type == "mark_sold":
            if uid:
                new_view = MarkSoldLayout(guild_id, uid, acc_content)
                await message.edit(view=new_view)
                return True
            else:
                print(f"    ⚠️ Skipping mark_sold view - no user ID found")
                return False
                
        elif view_type == "cash_in":
            if uid:
                new_view = CashInLayout(guild_id, uid, acc_content)
                await message.edit(view=new_view)
                return True
            else:
                print(f"    ⚠️ Skipping cash_in view - no user ID found")
                return False
        
        return False
        
    except Exception as e:
        print(f"    ⚠️ Error updating message with data: {e}")
        return False

async def update_messages_in_channel(channel, view_type, guild_id):
    """Update all messages with views in a channel"""
    updated = 0
    
    try:
        # Get all messages
        messages = []
        async for message in channel.history(limit=None):
            messages.append(message)
        
        # Process from oldest to newest
        messages.reverse()
        
        for message in messages:
            if message.components:
                if view_type == "acc_panel":
                    from cogs.acc_panel import Accs
                    new_view = Accs(guild_id)
                    await message.edit(view=new_view)
                    updated += 1
                    
    except Exception as e:
        print(f"  ⚠️ Error reading #{channel.name}: {e}")
    
    return updated

@client.event
async def on_ready():
    global _extensions_loaded

    if not _extensions_loaded:
        await load_extensions()
        _extensions_loaded = True

        # Register persistent view classes
        from cogs.acc_panel import Accs
        from cogs.views import CashInLayout, MarkSoldLayout, Pending
        from cogs.help import HelpV2
        from cogs.setup import SetupV2
    
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

    # Guild sync
    try:
        guild = discord.Object(id=1325056936231571486)
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
    
    # Auto-update views on restart
    await auto_update_views()

client.run(TOKEN)