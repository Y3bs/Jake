import platform
import discord
from discord.ext import commands
from discord import ButtonStyle, Color, TextStyle, app_commands
from discord.ui import File, FileUpload, Label, LayoutView, Container, Modal, Section, Separator, TextDisplay, ActionRow, Select, TextInput, Button, View
from discord import Embed, Interaction, SelectOption
from utils.utils import EMOJIS
from cogs.views import Pending
import utils.database as db

SUPPORTED_GAMES = ['BO7','OW2','Rivals','Battlefield6','WZ']

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
        await interaction.response.defer(ephemeral=True)
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

        # Create the pending channel
        await self.create_pending_channel(interaction, acc_content)

    async def create_pending_channel(self, interaction: Interaction, acc_content: str = ""):
        """Helper function to create the pending channel with or without account content"""
        guild = self.guild
        user = self.user
        
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
        view = Pending(self.guild_id, user.id, acc_content, self.game)
        await channel.send(view=view)

        # Acknowledge ephemerally
        try:
            await interaction.followup.send(f"تم إنشاء قناة التسجيل ✅\n# <#{channel.id}>", ephemeral=True)
        except Exception:
            pass

class SkipOrUploadView(View):
    def __init__(self, guild, user, game_value, guild_id):
        super().__init__(timeout=60)
        self.guild = guild
        self.user = user
        self.game_value = game_value
        self.guild_id = guild_id
    
    @discord.ui.button(label="تخطي وإنشاء القناة", style=discord.ButtonStyle.secondary, emoji="⏭️")
    async def skip_button(self, interaction: Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        
        # Create the modal instance to use its helper method
        modal = AccContent(self.guild, self.user, self.game_value, self.guild_id)
        await modal.create_pending_channel(interaction, "")
        
        # Disable buttons after use
        for child in self.children:
            child.disabled = True
        await interaction.edit_original_response(view=self)
    
    @discord.ui.button(label="رفع ملف الحساب", style=discord.ButtonStyle.primary, emoji="📤")
    async def upload_button(self, interaction: Interaction, button: Button):
        # Send the file upload modal
        modal = AccContent(self.guild, self.user, self.game_value, self.guild_id)
        await interaction.response.send_modal(modal)
        
        # Disable buttons after use
        for child in self.children:
            child.disabled = True
        await interaction.edit_original_response(view=self)
    
    async def on_timeout(self):
        # Disable buttons when timeout
        for child in self.children:
            child.disabled = True

class Games(Select):
    def __init__(self, guild_id):
        self.guild_id = guild_id
        options = [
            SelectOption(label='BO7', value='bo7', emoji=EMOJIS['bo7']),
            SelectOption(label='Overwatch 2', value='ow2', emoji=EMOJIS['ow2']),
            SelectOption(label='Marvel Rivals', value='rivals', emoji=EMOJIS['rivals']),
            SelectOption(label='Battlefield 6', value='battlefield6', emoji=EMOJIS['battlefield6']),
            SelectOption(label='Warzone', value='warzone', emoji=EMOJIS['wz']),
            SelectOption(label='Valorant', value='valorant',emoji=EMOJIS['valorant'])
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
        
        # Create and send the skip/upload view
        view = SkipOrUploadView(
            guild=interaction.guild,
            user=interaction.user,
            game_value=game_value,
            guild_id=interaction.guild.id
        )
        
        embed = Embed(
            title="خيارات رفع الحساب",
            description="اختر كيفية المتابعة:",
            color=Color.blue()
        )
        embed.add_field(
            name="⏭️ تخطي وإنشاء القناة",
            value="إنشاء قناة التحقق بدون رفع ملف الحساب. يمكنك إضافة تفاصيل الحساب لاحقًا في القناة.",
            inline=False
        )
        embed.add_field(
            name="📤 رفع ملف الحساب",
            value="ارفع ملف `.txt` يحتوي على تفاصيل حسابك للتحقق.",
            inline=False
        )
        
        await interaction.response.send_message(
            embed=embed,
            view=view,
            ephemeral=True
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
        
        # Stats button - UPDATED
        self.stats_btn = Button(label='احصائياتي', style=ButtonStyle.green, emoji='📊', custom_id='stats_btn')
        self.stats_btn.callback = self.stats_callback  
        
        self.stats_title = TextDisplay('# الاحصائيات 📊')
        self.stats_desc = TextDisplay('احصائيات الشهر الحالي')
        self.stats_section = ActionRow(self.stats_btn)

        # Create container with the action row
        self.container = Container()
        self.container.add_item(self.title)
        self.container.add_item(self.sep)
        self.container.add_item(self.desc)
        self.container.add_item(self.action_row)

        self.container.add_item(self.sep)
        self.container.add_item(self.stats_title)
        self.container.add_item(self.stats_desc)
        self.container.add_item(self.stats_section)
        # Add container to the layout
        self.add_item(self.container)
    
    async def stats_callback(self, interaction: Interaction):
        """Callback for stats button - shows current month statistics"""
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Get current month stats using the helper function
            from utils.utils import get_current_month_stats, format_monthly_stats_message
            
            # Get stats for current user
            stats_data = get_current_month_stats(interaction.user.id)
            
            # Create a LayoutView for displaying stats
            stats_view = LayoutView(timeout=None)
            container = Container(accent_color=discord.Color.from_rgb(0, 230, 230))
            
            if stats_data.get('error'):
                # Error state
                if stats_data.get('registered') == False:
                    container.add_item(TextDisplay(content="# ❌ التسجيل مطلوب"))
                    container.add_item(Separator())
                    container.add_item(TextDisplay(content="أنت غير مسجل في قاعدة البيانات. استخدم `/register` أولاً!"))
                elif stats_data.get('no_history'):
                    container.add_item(TextDisplay(content="# 📊 لا يوجد تاريخ للحسابات"))
                    container.add_item(Separator())
                    container.add_item(TextDisplay(content="ليس لديك أي تاريخ للحسابات بعد!\nابدأ ببيع الحسابات لترى إحصائياتك هنا."))
                else:
                    container.add_item(TextDisplay(content="# ❌ خطأ في الإحصائيات"))
                    container.add_item(Separator())
                    container.add_item(TextDisplay(content=stats_data.get('message', 'حدث خطأ غير معروف.')))
            else:
                # Success state - format the message
                stats_message = format_monthly_stats_message(stats_data, interaction.user.mention)
                container.add_item(TextDisplay(content=stats_message))
                
                # Add a footer with total accounts this month
                if stats_data['total_current_month'] > 0:
                    footer_text = f"**إجمالي الحسابات هذا الشهر:** {stats_data['total_current_month']} حساب"
                    container.add_item(Separator())
                    container.add_item(TextDisplay(content=footer_text))
            
            stats_view.add_item(container)
            await interaction.followup.send(view=stats_view, ephemeral=True)
            
        except Exception as e:
            # Fallback error handling
            error_view = LayoutView()
            error_container = Container(accent_color=discord.Color.red())
            error_container.add_item(TextDisplay(content="# ❌ خطأ في جلب الإحصائيات"))
            error_container.add_item(TextDisplay(content=f"حدث خطأ: {str(e)}"))
            error_view.add_item(error_container)
            await interaction.followup.send(view=error_view, ephemeral=True)

class Panel(commands.Cog):
    def __init__(self,client):
        self.client = client

    @app_commands.command(name='acc_panel', description="يرسل لوحة الرسائل لتسجيل الحسابات")
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

        # Send the panel
        view = Accs(interaction.guild.id)
        message = await channel.send(view=view)
        
        # Store the panel channel ID for future updates
        from utils.storage import save_panel_channel_id
        save_panel_channel_id(interaction.guild.id, channel.id)
        
        await interaction.followup.send('Panel created ✅',ephemeral=True)

async def setup(client):
    await client.add_cog(Panel(client))