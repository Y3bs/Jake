import discord
from discord.ext import commands
from discord import app_commands
from discord import Interaction, SelectOption
from discord.ui import ActionRow, Container, Label, LayoutView, Separator, TextDisplay, Select
from utils.utils import EMOJIS
from cogs.wallet_modals import EWallet, Instapay, Visa

class WalletTypeDropDown(Select):
    def __init__(self):
        options = [
            SelectOption(label='محفظة إلكترونية', value='e-wallet', emoji=EMOJIS['ewallet']),
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
        if selected == 'e-wallet':
            await interaction.response.send_modal(EWallet())
        if selected == 'instapay':
            await interaction.response.send_modal(Instapay())
        if selected == 'visa':
            await interaction.response.send_modal(Visa())


class WalletType(LayoutView):
    def __init__(self):
        super().__init__(timeout=None)
        container = Container()

        self.title = TextDisplay('# محفظتك 💳')
        container.add_item(self.title)

        container.add_item(Separator())

        self.text = TextDisplay('الانواع المدعومة')
        container.add_item(self.text)

        container.add_item(Separator())

        self.supported = TextDisplay(f"{EMOJIS["ewallet"]} محفظة إلكترونية\n{EMOJIS["instapay"]} انستاباي\n{EMOJIS["visa"]} فيزا'")
        container.add_item(self.supported)

        self.wallet = ActionRow(WalletTypeDropDown())
        container.add_item(self.wallet)

        self.add_item(container)
    

class Wallet(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @app_commands.command(name='save_wallet', description='احفظ عنوان الدفع الخاص بك للوصول السهل لاحقًا')
    async def register_wallet(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(view=WalletType(), ephemeral=True)

async def setup(client):
    await client.add_cog(Wallet(client))