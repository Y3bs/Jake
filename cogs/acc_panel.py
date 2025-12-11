import platform
import discord
from discord.ext import commands
from discord import Color, TextStyle, app_commands
from discord.ui import File, FileUpload, Label, LayoutView, Container, Modal, Separator, TextDisplay, ActionRow, Select, TextInput
from discord import Embed, Interaction, SelectOption
from utils.utils import EMOJIS
from cogs.views import Pending
import utils.database as db

SUPPORTED_GAMES = ['BO7','OW2','Rivals','Battlefield6']

class AccContent(Modal):
    def __init__(self,guild,user,game_value,guild_id:int):
        super().__init__(title='📃 Account Content')
        self.guild = guild
        self.user = user
        self.game = game_value
        self.guild_id = guild_id
        self.upload = FileUpload(min_values=1,max_values=1,required=True)
        self.add_item(Label(text = 'Upload your account (.txt)',component=self.upload))
    
    async def on_submit(self, interaction: Interaction):
        await interaction.response.send_message(f'creating channel...', ephemeral=True)
        guild = self.guild
        guild_id = self.guild_id
        user = self.user
        acc_attachment = self.upload.values

        # read file & retrieve its content
        acc_file = acc_attachment[0]
        if not acc_file.filename.endswith('.txt'):
            return await interaction.followup.send('Only upload **.txt** files',ephemeral=True)
    
        data: bytes = await acc_file.read()
        try:
            acc_content = data.decode('utf-8')
        except:
            acc_content = data.decode('latin-1',errors='ignore')

        # Ensure Pending category
        category = discord.utils.get(guild.categories, name="Pending 🔃")
        if category is None:
            category = await guild.create_category("Pending 🔃")
        # Create user-named channel with restricted visibility
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                attach_files=True,
                read_message_history=True
            )
        }
        channel = await category.create_text_channel(
            f"🔃{user.name}",
            overwrites=overwrites
        )

        # Send Pending view and pass platform and game
        view = Pending(guild_id, user.id, acc_content, self.game)
        await channel.send(view=view)

        # Acknowledge ephemerally
        try:
            await interaction.followup.send(f"تم إنشاء قناة التسجيل ✅\n# <#{channel.id}>", ephemeral=True)
        except Exception:
            pass

class Games(Select):
    def __init__(self, guild_id):
        self.guild_id = guild_id
        # In the Games(Select) class __init__ method:
        options = [
            SelectOption(label='BO7', value='bo7', emoji=EMOJIS['bo7']),
            SelectOption(label='Overwatch 2', value='ow2', emoji=EMOJIS['ow2']),
            SelectOption(label='Marvel Rivals', value='rivals', emoji=EMOJIS['rivals']),
            SelectOption(label='Battlefield 6', value='battlefield6', emoji=EMOJIS['battlefield6']),
            SelectOption(label='Warzone', value='warzone', emoji=EMOJIS['warzone']),
        ]
        super().__init__(
            placeholder="Select your game...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="game_selector"
        )
    
    async def callback(self, interaction: Interaction):
        game_value = self.values[0]
        await interaction.response.send_modal(
            AccContent(
                guild = interaction.guild,
                user = interaction.user,
                game_value=game_value,
                guild_id = interaction.guild.id
            )
        )

class Accs(LayoutView):
    def __init__(self, guild_id):
        super().__init__(timeout=None)
        self.guild_id = guild_id
        
        # Create Text
        self.title = TextDisplay("# الاكونتات 📮")
        self.sep = Separator()
        self.desc = TextDisplay('اختار اللعبة 🎮')
        
        # Create action row for the select menu
        self.select_menu = Games(self.guild_id)
        self.action_row = ActionRow(self.select_menu)
        
        # Create container with the action row
        self.container = Container()
        self.container.add_item(self.title)
        self.container.add_item(self.sep)
        self.container.add_item(self.desc)
        self.container.add_item(self.action_row)
        # Add container to the layout
        self.add_item(self.container)

class Panel(commands.Cog):
    def __init__(self,client):
        self.client = client

    @app_commands.command(name='acc_panel', description="sends the panel message for logging accounts")
    async def acc_panel(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        if not interaction.user.guild_permissions.administrator:
            error = Embed(
                title='Permissions Error ⛔',
                description="You don't have permission to use to command **(Admins Only 🧑‍💼)**",
                color=0xE80000
            )
            return await interaction.followup.send(embed=error,ephemeral=True)
        channel = interaction.channel

        await channel.send(view=Accs(interaction.guild.id))
        await interaction.followup.send('Panel created ✅',ephemeral=True)

async def setup(client):
    await client.add_cog(Panel(client))
