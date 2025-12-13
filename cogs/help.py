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
        container.add_item(TextDisplay(content="# 🤖 بوت إدارة الحسابات - المساعدة"))
        container.add_item(TextDisplay(content="دليل شامل لاستخدام نظام إدارة الحسابات"))
        container.add_item(Separator())
        
        # Setup Requirement - NEW SECTION
        container.add_item(TextDisplay(content="## ⚠️ الخطوة الأولى: إعداد السيرفر"))
        setup_info = TextDisplay(content="""**يجب على مدراء السيرفر تشغيل:** `/setup`
هذا الأمر ينشئ كل القنوات والفئات الضرورية لعمل البوت بشكل صحيح.

إذا لم تكن القنوات موجودة، لن يتمكن المستخدمون من تقديم الحسابات!""")
        container.add_item(setup_info)
        container.add_item(Separator())
        
        # Getting Started section
        container.add_item(TextDisplay(content="## 🎮 البداية"))
        getting_started = TextDisplay(content="""**1.** `/register` - إنشاء ملفك الشخصي كبائع
**2.** `/register_wallet` - إضافة طرق الدفع
**3.** `/me` - عرض إحصائياتك وأرباحك
**4.** استخدم لوحة الحسابات لبدء البيع""")
        container.add_item(getting_started)
        container.add_item(Separator())
        
        # Game Support section  
        container.add_item(TextDisplay(content="## 🎯 الألعاب المدعومة"))
        games = TextDisplay(content="""• **BO7** - Call of Duty: Black Ops 7
• **OW2** - Overwatch 2  
• **Marvel Rivals**
• **Battlefield 6**
• **Warzone** - Call of Duty: Black Ops 7 Warzone""")
        container.add_item(games)
        container.add_item(Separator())
        
        # Account Process section
        container.add_item(TextDisplay(content="## 📦 عملية الحساب"))
        process = TextDisplay(content="""**Pending 🔃** → الحساب تم تقديمه
**For Sale 🏷️** → جاهز للعملاء  
**Sold 📦** → الحساب تم تسليمه
**Paid 💰** → تم استلام الدفع
**Banned ⛔** → الحساب محظور""")
        container.add_item(process)
        
        self.add_item(container)

class HelpCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="help", description="تعلم كيفية استخدام البوت بواجهة حديثة")
    async def help_v2(self, interaction: Interaction):
        """إرسال رسالة المساعدة باستخدام Components V2"""
        help_view = HelpV2()
        
        # Send with Components V2 flag
        await interaction.response.send_message(
            view=help_view,
            ephemeral=True
        )

async def setup(client):
    await client.add_cog(HelpCog(client))