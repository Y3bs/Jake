import discord
from discord.ext import commands
from discord import app_commands
from discord import Embed, Interaction, SelectOption
from discord.ui import View, Select
from utils.utils import EMOJIS
from cogs.wallet_modals import Vodafone, Instapay, Visa

class WalletTypeDropDown(Select):
    def __init__(self):
        options = [
            SelectOption(label='فودافون كاش', value='vodafone', emoji=EMOJIS['vodafone']),
            SelectOption(label='انستاباي', value='instapay', emoji=EMOJIS['instapay']),
            SelectOption(label='فيزا', value='visa', emoji=EMOJIS['visa'])
        ]
        
        super().__init__(
            placeholder='اختر نوع المحفظة',
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: Interaction):
        selected = self.values[0]
        if selected == 'vodafone':
            await interaction.response.send_modal(Vodafone())
        if selected == 'instapay':
            await interaction.response.send_modal(Instapay())
        if selected == 'visa':
            await interaction.response.send_modal(Visa())


class WalletType(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(WalletTypeDropDown())
    

class Wallet(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @app_commands.command(name='register_wallet', description='احفظ عنوان الدفع الخاص بك للوصول السهل لاحقًا')
    async def register_wallet(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = Embed(
            title='اختر نوع محفظتك',
            description='الأنواع المدعومة',
            color=0x040dbf
        )
        embed.add_field(name=f'{EMOJIS["vodafone"]} فودافون كاش', value=' ')
        embed.add_field(name=f'{EMOJIS["instapay"]} انستاباي', value=' ')
        embed.add_field(name=f'{EMOJIS["visa"]} فيزا', value=' ')
        await interaction.followup.send(embed=embed, view=WalletType(), ephemeral=True)

async def setup(client):
    await client.add_cog(Wallet(client))