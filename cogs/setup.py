# cogs/setup_v2.py
import discord
from discord.ext import commands
from discord.ui import LayoutView, Container, TextDisplay, Separator, Button, ActionRow
from discord import Interaction, TextStyle, Color, app_commands
from cogs.acc_panel import Accs  # Import your existing Accs panel
from utils.storage import save_panel_channel_id

class SetupButton(Button):
    def __init__(self, original_interaction: Interaction):
        super().__init__(
            style=discord.ButtonStyle.primary,
            label="🚀 إعداد البوت",
            custom_id="setup_bot_button"
        )
        self.original_interaction = original_interaction
    
    async def callback(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        
        guild = interaction.guild
        user = interaction.user
        
        # 1. Create panel category
        panel_category = await self._create_panel_category(guild)
        
        # 2. Create required account categories
        required_categories = ["Pending 🔃", "For Sale 🏷️", "Sold 📦", "Banned ⛔", "Paid 💰"]
        created_categories = []
        
        for category_name in required_categories:
            existing = discord.utils.get(guild.categories, name=category_name)
            if not existing:
                category = await guild.create_category(category_name)
                created_categories.append(category_name)
        
        # 3. Create panel channel in panel category
        panel_channel = await self._create_panel_channel(guild, panel_category)
        
        # 4. Save panel channel ID to storage
        save_panel_channel_id(guild.id, panel_channel.id)
        
        # 5. Send panel and pin it
        panel_message = await self._send_and_pin_panel(panel_channel, guild.id)
        
        # 6. Edit the original message to show completion
        await self._edit_original_message(panel_category, created_categories, panel_channel)

    async def _create_panel_category(self, guild):
        """Create the panel category if it doesn't exist"""
        panel_category = discord.utils.get(guild.categories, name="📌 Panel")
        if not panel_category:
            panel_category = await guild.create_category("📌 Panel", position=0)
        return panel_category

    async def _create_panel_channel(self, guild, panel_category):
        """Create the panel channel in the panel category"""
        # Check if panel channel already exists
        existing_channel = discord.utils.get(guild.text_channels, name="📮-account-panel")
        if existing_channel:
            return existing_channel
        
        # Create channel in panel category
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
            category=panel_category,
            position=0,
            topic="🎮 لوحة تقديم الحسابات - استخدم هذه اللوحة لتقديم حسابات الألعاب للبيع"
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
            content="## 📋 كيفية الاستخدام:\n"
                   "1. **اختر لعبتك** من القائمة المنسدلة أعلاه\n"
                   "2. **ارفع ملف حسابك** (.txt) عندما تتم مطالبتك بذلك\n"
                   "3. **اتبع العملية** في قناتك الخاصة\n"
                   "4. **تتبع مبيعاتك** باستخدام الأمر `/me`\n\n"
                   "*بحاجة إلى مساعدة؟ استخدم الأمر `/help`*"
        )
        
        return panel_message

    async def _edit_original_message(self, panel_category, created_categories, panel_channel):
        """Edit the original setup message to show completion"""
        completion_view = LayoutView()
        completion_container = Container(accent_color=Color.green())
        
        completion_container.add_item(TextDisplay(content="# ✅ اكتمل الإعداد!"))
        completion_container.add_item(TextDisplay(content="تم تكوين سيرفرك الآن بالكامل لإدارة الحسابات!"))
        completion_container.add_item(Separator())
        
        # Panel category created
        completion_container.add_item(TextDisplay(content="## 📍 فئة اللوحة الرئيسية"))
        completion_container.add_item(TextDisplay(content=f"تم إنشاء فئة {panel_category.mention} للوحة الحسابات"))
        
        completion_container.add_item(Separator())
        
        # Categories created
        if created_categories:
            completion_container.add_item(TextDisplay(content="## 📁 فئات الحسابات التي تم إنشاؤها"))
            categories_text = "\n".join([f"• {cat}" for cat in created_categories])
            completion_container.add_item(TextDisplay(content=categories_text))
        else:
            completion_container.add_item(TextDisplay(content="## 📁 فئات الحسابات"))
            completion_container.add_item(TextDisplay(content="جميع فئات الحسابات المطلوبة كانت موجودة بالفعل"))
        
        completion_container.add_item(Separator())
        
        # Panel channel info
        completion_container.add_item(TextDisplay(content="## 📋 لوحة الحسابات"))
        completion_container.add_item(TextDisplay(content=f"تم إنشاء اللوحة في {panel_channel.mention} وتثبيتها للوصول السهل!"))
        
        completion_container.add_item(Separator())
        
        # Next steps
        completion_container.add_item(TextDisplay(content="## 🎯 جاهز للانطلاق!"))
        next_steps = TextDisplay(content="""**يمكن للمستخدمين الآن:**
• استخدام لوحة الحسابات لتقديم الحسابات
• التسجيل باستخدام الأمر `/register`  
• إضافة محافظ باستخدام الأمر `/register_wallet`
• فحص الإحصائيات باستخدام الأمر `/me`""")
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
        container.add_item(TextDisplay(content="# ⚙️ معالج إعداد البوت"))
        container.add_item(TextDisplay(content="انقر على الزر أدناه لإعداد البوت تلقائيًا لسيرفرك"))
        container.add_item(Separator())
        
        # What will be set up
        container.add_item(TextDisplay(content="## 📋 سيقوم هذا بإنشاء:"))
        setup_items = TextDisplay(content="""• **فئة لوحة الحسابات 📌** (لوحة رئيسية)
• **فئات الحسابات** (Pending, For Sale, Sold, إلخ.)
• **قناة لوحة الحسابات** مع رسالة مثبتة
• **هيكل الصلاحيات المناسب**
• **نظام سير العمل الكامل**""")
        container.add_item(setup_items)
        
        container.add_item(Separator())
        
        # Requirements
        container.add_item(TextDisplay(content="## ⚠️ المتطلبات"))
        requirements = TextDisplay(content="""• يحتاج البوت إلى صلاحية **إدارة القنوات**
• يحتاج البوت إلى صلاحية **إدارة الرسائل**  
• يحتاج البوت إلى صلاحية **عرض القناة**
• أنت تحتاج إلى صلاحية **المشرف**""")
        container.add_item(requirements)
        
        # Add the setup button in an action row
        setup_button = SetupButton(original_interaction)
        button_row = ActionRow(setup_button)
        container.add_item(button_row)
        
        self.add_item(container)

class SetupCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="setup", description="إعداد تفاعلي لتكوين البوت لسيرفرك")
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
            error_container.add_item(TextDisplay(content="# ⚠️ تم رفض الصلاحية"))
            error_container.add_item(TextDisplay(content="أنت بحاجة إلى صلاحيات **المشرف** لتشغيل الإعداد!"))
            
            error_view = LayoutView()
            error_view.add_item(error_container)
            
            await interaction.response.send_message(
                view=error_view,
                ephemeral=True
            )

async def setup(client):
    await client.add_cog(SetupCog(client))