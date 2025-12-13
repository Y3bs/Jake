# cogs/stats_v2.py
import discord
from discord.ext import commands
from discord.ui import LayoutView, Container, TextDisplay, Separator, MediaGallery
from discord import Interaction, File, app_commands
import utils.database as db
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import io
import os

def plot_stats(interaction, df):
    """Generate stats plot and save to attachments folder"""
    # Create attachments folder if it doesn't exist
    if not os.path.exists('attachments'):
        os.makedirs('attachments')
    
    filename = f"{interaction.user.id}_stats.png"
    filepath = os.path.join('attachments', filename)

    df['time'] = pd.to_datetime(df['time'])
    plt.figure(figsize=(12, 6))  
    sns.set_theme(style="darkgrid")
    sns.set_context("talk")
    plt.rcParams['font.size'] = 14
    plt.rcParams['figure.facecolor'] = '#2F3136'
    plt.rcParams['axes.facecolor'] = '#2F3136'
    plt.rcParams['text.color'] = 'white'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['xtick.color'] = 'white'
    plt.rcParams['ytick.color'] = 'white'

    # Create the plot with better styling
    ax = sns.lineplot(x='time', y='price', data=df, marker='o', linewidth=3, color='#00E6E6')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d-%b"))
    plt.title(f"{interaction.user.display_name}'s Earnings", pad=20, fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Price (L.E)', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    # Style the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Save to attachments folder
    plt.savefig(filepath, bbox_inches='tight', facecolor='#2F3136')
    plt.close()
    
    return filename

class StatsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name='me_v2', description="يعرض أرباحك وعدد الحسابات المباعة والمحظورة")
    async def stats_v2(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        
        uid = interaction.user.id
        user_stats = db.find_player(uid)
        
        # Handle not registered users
        if not user_stats:
            error_view = LayoutView()
            error_container = Container(accent_color=discord.Color.red())
            error_container.add_item(TextDisplay(content="# ❌ التسجيل مطلوب"))
            error_container.add_item(TextDisplay(content="أنت غير مسجل في قاعدة البيانات. استخدم `/register` أولاً!"))
            error_view.add_item(error_container)
            return await interaction.followup.send(view=error_view, ephemeral=True)
        
        # Handle no history
        if not user_stats.get('history'):
            no_history_view = LayoutView()
            no_history_container = Container(accent_color=discord.Color.blue())
            no_history_container.add_item(TextDisplay(content="# 📊 لا يوجد تاريخ للحسابات"))
            no_history_container.add_item(TextDisplay(content="ليس لديك أي تاريخ للحسابات بعد!\nابدأ ببيع الحسابات لترى إحصائياتك هنا."))
            no_history_view.add_item(no_history_container)
            return await interaction.followup.send(view=no_history_view, ephemeral=True)
        
        try:
            # Generate stats and chart
            user_df = pd.DataFrame(user_stats['history'])
            chart_filename = plot_stats(interaction, user_df)
            
            # Calculate stats
            success_rate = db.success_rate(uid)
            avg_sale = db.avg_sale(uid)
            
            # Create Components V2 view
            stats_view = LayoutView(timeout=None)
            
            # Main container for stats
            main_container = Container(accent_color=discord.Color.from_rgb(0, 230, 230))
            
            # Title section
            main_container.add_item(TextDisplay(content=f"# 📊 إحصائيات {interaction.user.mention}"))
            main_container.add_item(Separator())
            
            # Stats display
            stats_text = (
                f"**💸 مباع:** {user_stats['sold']} حساب\n"
                f"**⛔ محظور:** {user_stats['banned']} حساب\n"
                f"**📦 معدل النجاح:** {success_rate}%\n"
                f"**💰 إجمالي الأرباح:** {user_stats['earnings']} ج.م\n"
                f"**⚖️ متوسط سعر البيع:** {avg_sale} ج.م\n"
                f"**💳 محافظ:** {len(user_stats['wallets'])} مسجلة"
            )
            
            main_container.add_item(TextDisplay(content=stats_text))
            stats_view.add_item(main_container)
            
            # Add separator
            stats_view.add_item(Separator())
            
            # Create MediaGallery for the chart
            media_gallery = MediaGallery()
            
            # Add chart to media gallery
            chart_file = File(f"attachments/{chart_filename}", filename=chart_filename)
            media_gallery.add_item(media=chart_file)
         
            stats_view.add_item(media_gallery)
            
            # Send the message with both the view and file
            await interaction.followup.send(
                view=stats_view,
                file=chart_file,
                ephemeral=True
            )
            
        except Exception as e:
            # Error handling with Components V2
            error_view = LayoutView()
            error_container = Container(accent_color=discord.Color.red())
            error_container.add_item(TextDisplay(content="# ❌ خطأ في إنشاء الإحصائيات"))
            error_container.add_item(TextDisplay(content=f"فشل في إنشاء الإحصائيات: {str(e)}"))
            error_view.add_item(error_container)
            await interaction.followup.send(view=error_view, ephemeral=True)

async def setup(client):
    await client.add_cog(StatsCog(client))