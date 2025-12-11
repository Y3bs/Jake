# cogs/setup_v2.py
import discord
from discord.ext import commands
from discord.ui import LayoutView, Container, TextDisplay, Separator, Button, ActionRow
from discord import Interaction, TextStyle, Color, app_commands
from cogs.acc_panel import Accs  # Import your existing Accs panel

class SetupButton(Button):
    def __init__(self, original_interaction: Interaction):
        super().__init__(
            style=discord.ButtonStyle.primary,
            label="🚀 Setup Bot",
            custom_id="setup_bot_button"
        )
        self.original_interaction = original_interaction
    
    async def callback(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        
        guild = interaction.guild
        user = interaction.user
        
        # Create required categories
        required_categories = ["Pending 🔃", "For Sale 🏷️", "Sold 📦", "Banned ⛔", "Paid 💰"]
        created_categories = []
        
        for category_name in required_categories:
            existing = discord.utils.get(guild.categories, name=category_name)
            if not existing:
                category = await guild.create_category(category_name)
                created_categories.append(category_name)
        
        # Create panel channel
        panel_channel = await self._create_panel_channel(guild, user)
        
        # Send panel and pin it
        panel_message = await self._send_and_pin_panel(panel_channel, guild.id)
        
        # Edit the original message to show completion
        await self._edit_original_message(created_categories, panel_channel)

    async def _create_panel_channel(self, guild, user):
        """Create the panel channel with proper permissions"""
        # Check if panel channel already exists
        existing_channel = discord.utils.get(guild.text_channels, name="📮-account-panel")
        if existing_channel:
            return existing_channel
        
        # Create channel in top position
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=False,
                add_reactions=False
            ),
            guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_messages=True,
                manage_channels=True
            )
        }
        
        panel_channel = await guild.create_text_channel(
            "📮-account-panel",
            overwrites=overwrites,
            position=0,  # Put at top of channel list
            topic="🎮 Account Submission Panel - Use this panel to submit your game accounts for sale"
        )
        
        return panel_channel

    async def _send_and_pin_panel(self, channel, guild_id):
        """Send the panel message and pin it"""
        # Create and send the panel
        panel_view = Accs(guild_id)
        panel_message = await channel.send(
            view=panel_view
        )
        
        # Pin the panel message
        await panel_message.pin()
        
        # Send instructions message (optional)
        instructions = await channel.send(
            content="## 📋 How to Use:\n"
                   "1. **Select your game** from the dropdown above\n"
                   "2. **Upload your account file** (.txt) when prompted\n"
                   "3. **Follow the process** in your private channel\n"
                   "4. **Track your sales** with `/me` command\n\n"
                   "*Need help? Use `/help` command*"
        )
        
        return panel_message

    async def _edit_original_message(self, created_categories, panel_channel):
        """Edit the original setup message to show completion"""
        completion_view = LayoutView()
        completion_container = Container(accent_color=Color.green())
        
        completion_container.add_item(TextDisplay(content="# ✅ Setup Complete!"))
        completion_container.add_item(TextDisplay(content="Your server is now fully configured for account management!"))
        completion_container.add_item(Separator())
        
        # Categories created
        if created_categories:
            completion_container.add_item(TextDisplay(content="## 📁 Created Categories"))
            categories_text = "\n".join([f"• {cat}" for cat in created_categories])
            completion_container.add_item(TextDisplay(content=categories_text))
        else:
            completion_container.add_item(TextDisplay(content="## 📁 Categories"))
            completion_container.add_item(TextDisplay(content="All required categories were already set up"))
        
        completion_container.add_item(Separator())
        
        # Panel channel info
        completion_container.add_item(TextDisplay(content="## 📋 Account Panel"))
        completion_container.add_item(TextDisplay(content=f"Panel created in {panel_channel.mention} and pinned for easy access!"))
        
        completion_container.add_item(Separator())
        
        # Next steps
        completion_container.add_item(TextDisplay(content="## 🎯 Ready to Go!"))
        next_steps = TextDisplay(content="""**Users can now:**
• Use the account panel to submit accounts
• Register with `/register` command  
• Add wallets with `/register_wallet`
• Check stats with `/me` command""")
        completion_container.add_item(next_steps)
        
        completion_view.add_item(completion_container)
        
        # Edit the original message that had the button
        await self.original_interaction.edit_original_response(
            view=completion_view,
            content=None  # Remove any existing content
        )

class SetupV2(LayoutView):
    def __init__(self, original_interaction: Interaction):
        super().__init__(timeout=None)
        self.original_interaction = original_interaction
        
        # Main setup container
        container = Container(accent_color=Color.blue())
        
        # Header
        container.add_item(TextDisplay(content="# ⚙️ Bot Setup Wizard"))
        container.add_item(TextDisplay(content="Click the button below to automatically set up the bot for your server"))
        container.add_item(Separator())
        
        # What will be set up
        container.add_item(TextDisplay(content="## 📋 This will create:"))
        setup_items = TextDisplay(content="""• **Organizational Categories** (Pending, For Sale, Sold, etc.)
• **Account Panel Channel** with pinned message
• **Proper Permission Structure**
• **Complete Workflow System**""")
        container.add_item(setup_items)
        
        container.add_item(Separator())
        
        # Requirements
        container.add_item(TextDisplay(content="## ⚠️ Requirements"))
        requirements = TextDisplay(content="""• Bot needs **Manage Channels** permission
• Bot needs **Manage Messages** permission  
• Bot needs **View Channel** permission
• You need **Administrator** role""")
        container.add_item(requirements)
        
        # Add the setup button in an action row
        setup_button = SetupButton(original_interaction)
        button_row = ActionRow(setup_button)
        container.add_item(button_row)
        
        self.add_item(container)

class SetupCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="setup", description="Interactive setup to configure the bot for your server")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_v2(self, interaction: Interaction):
        """Interactive setup command with button"""
        setup_view = SetupV2(interaction)
        
        await interaction.response.send_message(
            view=setup_view
        )

    @setup_v2.error
    async def setup_error(self, interaction: Interaction, error):
        """Handle setup command errors"""
        if isinstance(error, app_commands.MissingPermissions):
            error_container = Container(accent_color=Color.red())
            error_container.add_item(TextDisplay(content="# ⚠️ Permission Denied"))
            error_container.add_item(TextDisplay(content="You need **Administrator** permissions to run the setup!"))
            
            error_view = LayoutView()
            error_view.add_item(error_container)
            
            await interaction.response.send_message(
                view=error_view,
                ephemeral=True
            )

async def setup(client):
    await client.add_cog(SetupCog(client))