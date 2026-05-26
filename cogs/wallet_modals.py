from discord import Interaction,Embed
from discord.ui import Modal,TextInput
from discord.ui.text_input import TextStyle
from utils.utils import EMOJIS, check_wallet_type
import utils.database as db

class EWallet(Modal):
    def __init__(self):
        super().__init__(title='E-Wallet')
        self.add_item(
            TextInput(label='Wallet Number',style=TextStyle.short,min_length=11,max_length=11,required=True)
        )

    async def on_submit(self, interaction: Interaction):
        wallet = self.children[0].value
        await interaction.response.defer(ephemeral=True)

        if not check_wallet_type('e-wallet',wallet):
            error = Embed(
                title='❌ رقم محفظة غير صالح',
                description='أتأكد انك تحط رقم محفظة موجود فعلا',
                color=0xE80000
            )
            return await interaction.followup.send(embed=error,ephemeral=True)

        if db.wallet_exist(interaction.user.id,'e-wallet',wallet):
            embed = Embed(
                title='المحفظة موجودة بالفعل',
                description='المحفظة دي متسجلة بالفعل علي حسابك',
            )
            return await interaction.followup.send(embed=embed,ephemeral=True)

        embed = Embed(
            title='تم تسجيل محفظة جديدة 🆕',
            description=f'**E-Wallet** {EMOJIS['ewallet']} متسجلة ك',
            color=0x038c07
        )
        embed.add_field(name='E-Wallet Number',value=f'```{wallet}```')
        await interaction.followup.send(embed=embed,ephemeral=True)
        db.save_wallet(interaction.user.id,'e-wallet',wallet)

class Instapay(Modal):
    def __init__(self):
        super().__init__(title='Instapay')
        self.add_item(
            TextInput(label='Instapay ID',style=TextStyle.short,required=True)
        )
    
    async def on_submit(self, interaction: Interaction):
        wallet = self.children[0].value
        await interaction.response.defer(ephemeral=True)

        if db.wallet_exist(interaction.user.id,'instapay',wallet):
            embed = Embed(
                title='المحفظة موجودة بالفعل',
                description='المحفظة دي متسجلة بالفعل علي حسابك',
            )
            return await interaction.followup.send(embed=embed,ephemeral=True)

        embed = Embed(
            title='تم تسجيل محفظة جديدة 🆕',
            description=f'**Instapay ID** {EMOJIS['instapay']} متسجلة ك',
            color=0x038c07
        )
        embed.add_field(name='Instapay ID',value=f'```{wallet}```')
        await interaction.followup.send(embed=embed,ephemeral=True)
        db.save_wallet(interaction.user.id,'instapay',wallet)


class Visa(Modal):
    def __init__(self):
        super().__init__(title='Visa information')
        self.add_item(
            TextInput(label='Card Number',style=TextStyle.short,min_length=16,max_length=16,required=True)
        )
        self.add_item(
            TextInput(label='Card Holder Name',style=TextStyle.short,required=True)
        )
    
    async def on_submit(self, interaction: Interaction):
        wallet = []
        wallet.append(self.children[0].value)
        await interaction.response.defer(ephemeral=True)

        if not check_wallet_type('visa',wallet[0]):
            error = Embed(
                title='❌ رقم كارت غير صالح',
                description='اتأكد انك تحط رقم كارت صحيح',
                color=0xE80000
            )
            return await interaction.followup.send(embed=error,ephemeral=True)

        wallet.append(self.children[1].value)    
        if db.wallet_exist(interaction.user.id,'visa',wallet):
            embed = Embed(
                title='المحفظة موجودة بالفعل',
                description='المحفظة دي متسجلة بالفعل علي حسابك',
            )
            return await interaction.followup.send(embed=embed,ephemeral=True)

        embed = Embed(
            title='تم تسجيل محفظة جديدة 🆕',
            description=f'**Visa Card** {EMOJIS['visa']} متسجلة ك',
            color=0x038c07
        )
        embed.add_field(name='Holder Name',value=f'```{wallet[1]}```')
        embed.add_field(name='Number',value=f'```{wallet[0]}```')
        await interaction.followup.send(embed=embed,ephemeral=True)
        db.save_wallet(interaction.user.id,'visa',wallet)

async def setup(client):
    pass