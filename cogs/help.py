# cogs/help_v2.py
import discord
from discord.ext import commands
from discord.ui import LayoutView,View, Container, TextDisplay, Separator, Button, ActionRow
from discord import Interaction, TextStyle, Color, app_commands

from utils.utils import EMOJIS

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
        getting_started = TextDisplay(content="""**1.** `/register` - إنشاء ملفك الشخصي 
**2.** `/save_wallet` - إضافة محفظة 
**3.** `/me` - عرض إحصائياتك وأرباحك
**4.** استخدم لوحة الحسابات لبدء البيع""")
        container.add_item(getting_started)
        container.add_item(Separator())
        
        # Game Support section  
        container.add_item(TextDisplay(content="## 🎯 الألعاب المدعومة"))
        games = TextDisplay(content=f"""• {EMOJIS['bo7']} **BO7** - Call of Duty: Black Ops 7
• {EMOJIS['ow2']} **OW2** - Overwatch 2  
• {EMOJIS['rivals']} **Marvel Rivals**
• {EMOJIS['battlefield6']} **Battlefield 6**
• {EMOJIS['wz']} **Warzone** - Call of Duty: Black Ops 7 Warzone
• {EMOJIS['valorant']} **VALORANT**
• {EMOJIS['arcraiders']} **Arc Raiders**""")
        container.add_item(games)
        container.add_item(Separator())
        
        # Account Process section
        container.add_item(TextDisplay(content="## 📦 عملية الحساب"))
        process = TextDisplay(content="""**Pending 🔃** → الحساب لسه فريش
**For Sale 🏷️** → جاهز ومتاح للبيع  
**Sold 📦** → الحساب تم تسليمه
**Paid 💰** → تم استلام الفلوس
**Banned ⛔** → الحساب اتبند""")
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