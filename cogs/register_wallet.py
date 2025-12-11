import discord
from discord.ext import commands
from discord import app_commands
from discord import Embed, Interaction, SelectOption
from discord.ui import View,Select
from utils.utils import EMOJIS
from cogs.wallet_modals import Vodafone,Instapay,Visa

class WalletTypeDropDown(Select):
    def __init__(self):
        options = [
            SelectOption(label='Vodafone Cash',value='vodafone',emoji=EMOJIS['vodafone']),
            SelectOption(label='Instapay',value='instapay',emoji=EMOJIS['instapay']),
            SelectOption(label='Visa',value='visa',emoji=EMOJIS['visa'])
        ]
        
        super().__init__(
            placeholder='Select a wallet type',
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
    def __init__(self,client):
        self.client = client
    
    @app_commands.command(name='register_wallet',description='save ur payment addresse for ez access later')
    async def register_wallet(self,interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = Embed(
            title='Choose your wallet type',
            description=f'Supported types',
            color=0x040dbf
        )
        embed.add_field(name=f'{EMOJIS['vodafone']} Vodafone Cash',value=' ')
        embed.add_field(name=f'{EMOJIS['instapay']} Instapay',value=' ')
        embed.add_field(name=f'{EMOJIS['visa']} Visa',value=' ')
        await interaction.followup.send(embed=embed,view=WalletType(),ephemeral=True)

async def setup(client):
    await client.add_cog(Wallet(client))