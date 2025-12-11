# cogs/help_v2.py
import discord
from discord.ext import commands
from discord.ui import LayoutView,View, Container, TextDisplay, Separator, Button, ActionRow
from discord import Interaction, TextStyle, Color, app_commands

class HelpV2(LayoutView):
    def __init__(self):
        super().__init__(timeout=None)
        
        # Main container with accent color
        container = Container(accent_color=Color.dark_theme())
        
        # Title section
        container.add_item(TextDisplay(content="# 🤖 Account Manager Bot - Help"))
        container.add_item(TextDisplay(content="Complete guide to using our account management system"))
        container.add_item(Separator())
        
        # Setup Requirement - NEW SECTION
        container.add_item(TextDisplay(content="## ⚠️ First Step: Server Setup"))
        setup_info = TextDisplay(content="""**Server admins must run:** `/setup`
This creates all necessary channels and categories for the bot to work properly.

If channels don't exist, users won't be able to submit accounts!""")
        container.add_item(setup_info)
        container.add_item(Separator())
        
        # Getting Started section
        container.add_item(TextDisplay(content="## 🎮 Getting Started"))
        getting_started = TextDisplay(content="""**1.** `/register` - Create your seller profile
**2.** `/register_wallet` - Add payment methods
**3.** `/me` - View your stats & earnings
**4.** Use the account panel to start selling""")
        container.add_item(getting_started)
        container.add_item(Separator())
        
        # Game Support section  
        container.add_item(TextDisplay(content="## 🎯 Supported Games"))
        games = TextDisplay(content="""• **BO7** - Call of Duty: Black Ops 7
• **OW2** - Overwatch 2  
• **Marvel Rivals**
• **Battlefield 6**""")
        container.add_item(games)
        container.add_item(Separator())
        
        # Account Process section
        container.add_item(TextDisplay(content="## 📦 Account Process"))
        process = TextDisplay(content="""**Pending 🔃** → Account submitted
**For Sale 🏷️** → Ready for customers  
**Sold 📦** → Account delivered
**Paid 💰** → Payment received
**Banned ⛔** → Account banned""")
        container.add_item(process)
        
        self.add_item(container)

class HelpCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="help", description="Learn how to use the bot with modern interface")
    async def help_v2(self, interaction: Interaction):
        """Send the help message using Components V2"""
        help_view = HelpV2()
        
        # Send with Components V2 flag
        await interaction.response.send_message(
            view=help_view,
            ephemeral=True
        )

async def setup(client):
    await client.add_cog(HelpCog(client))