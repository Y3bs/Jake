import discord
from discord.ext import commands
from discord import app_commands
from discord import Interaction,Embed,File
import utils.database as db
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import io
import os

def plot_stats(interaction, df):
    filename = f"{interaction.user.id}_stats.png"
    filepath = os.path.join('attachments', filename)

    df['time'] = pd.to_datetime(df['time'])
    plt.figure(figsize=(10, 5))  
    sns.set_theme(style="dark")
    sns.set_context("talk")
    plt.rcParams['font.size'] = 12

    sns.lineplot(x='time', y='price', data=df, marker = 'o',linewidth = 2)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d-%b"))
    plt.title(f"{interaction.user.display_name}'s Earnings")
    plt.xlabel('Date')
    plt.ylabel('Price (L.E)') 
    
    plt.savefig(filepath, bbox_inches='tight')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close()
    buffer.seek(0)

    return buffer, filepath

class Stats(commands.Cog):
    def __init__(self,client):
        self.client = client

    @app_commands.command(name='me',description="shows your earnings, number of banned,sold accounts")
    async def stats(self,interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        
        uid = interaction.user.id
        user_stats = db.find_player(uid)
        if not user_stats:
            return await interaction.followup.send("❌ You are not registered in the database. Use `/register` first.", ephemeral=True)
        
        if not user_stats.get('history'):
            return await interaction.followup.send("📊 You don't have any account history yet!", ephemeral=True)
        
        user_df = pd.DataFrame(user_stats['history'])
        img, path = plot_stats(interaction,user_df)
        stats_plot = File(img,filename = 'stats.png')
        success_rate = db.success_rate(uid)
        avg_sale = db.avg_sale(uid)

        embed = Embed(
            description=f'# 📊 Stats for {interaction.user.mention}',
            color=0x00E6E6
        )
        embed.add_field(name='💸 Sold',value=f'{user_stats['sold']} Account')
        embed.add_field(name='⛔ Banned',value=f'{user_stats['banned']} Account')
        embed.add_field(name='📦 Success Rate',value=f'{success_rate}%')
        embed.add_field(name='💰 Total Earnings',value=f'{user_stats['earnings']} L.E')
        embed.add_field(name='⚖️ Avg. Sale Price',value=f'{avg_sale} L.E')
        embed.add_field(name='💳 Wallets',value=f'{len(user_stats['wallets'])}')
        embed.set_image(url='attachment://stats.png')

        await interaction.followup.send(embed=embed,file = stats_plot,ephemeral=True)

async def setup(client):
    await client.add_cog(Stats(client))