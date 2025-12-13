from typing import Text
from discord import ButtonStyle,Button,Interaction, SelectOption
from discord.ui import ActionRow, Container, LayoutView, Section, Separator, View,Button,Modal,TextInput,button, TextDisplay, Select
from utils.utils import EMOJIS, move_channel,get_user_id
from cogs.game_modals import OW2, Bo7, SingularityBo7, BF6, Warzone, Rivals
import utils.database as db
import re

# Helper function to extract user ID from mention text
def extract_user_id_from_text(text):
    """Extract user ID from mention text like '# <@123456789>'"""
    try:
        if not text:
            return None
        match = re.search(r'<@(\d+)>', str(text))
        return int(match.group(1)) if match else None
    except:
        return None

class Bo7FinishSelect(Select):
    def __init__(self, pending_view: 'Pending',guild_id,parent_message,original_content,uid,acc):
        self.pending_view = pending_view
        self.guild_id = guild_id
        self.parent_message = parent_message
        self.original_content = original_content
        self.uid = uid
        self.acc = acc
        options = [
            SelectOption(label='Maxed only',value='max',emoji='🎚'),
            SelectOption(label='Gold', value='gold', emoji='🥇'),
            SelectOption(label='Arclight', value='arclight', emoji='💠'),
            SelectOption(label='Singularity', value='singularity', emoji='🌌'),
        ]
        super().__init__(
            placeholder='اختر نوع الكامو',
            min_values=1,
            max_values=1,
            options=options,
            custom_id='pending_finished_bo7'
        )

    async def callback(self, interaction: Interaction):
        selected_value = self.values[0]
        if selected_value == 'singularity':
            await interaction.response.send_modal(
                SingularityBo7(
                    guild_id = self.guild_id,
                    parent_message=self.parent_message,
                    original_content=self.original_content,
                    uid=self.uid,
                    acc=self.acc
                )
            )
        else:
            await interaction.response.send_modal(
                Bo7(
                    guild_id=self.guild_id,
                    parent_message=self.parent_message,
                    original_content=self.original_content,
                    uid=self.uid,
                    acc=self.acc,
                    camo_type=selected_value,
                )
            )

class Pending(LayoutView):
    def __init__(self,guild_id,uid,acc,game):
        super().__init__(timeout=None)
        self.guild_id = guild_id
        self.uid = uid
        self.acc = acc
        self.game = game

        container = Container()

        # Part 1: user mention - MAKE SURE THIS IS PRESERVED
        user_mention_text = f'# <@{uid}>' if uid else '# <@unknown>'
        user = TextDisplay(user_mention_text)
        container.add_item(user)
        container.add_item(Separator())
        
        # Part 2: text and a button on the same line
        finished_btn = Button(label='خلصت الاكونت', style=ButtonStyle.gray,emoji='🏁', custom_id='pending_finished')
        async def _finished_on_click(interaction: Interaction):
            await self.finished_callback(finished_btn, interaction)

        finished_btn.callback = _finished_on_click
        part2_row = Section(accessory=finished_btn)
        part2_row.add_item(TextDisplay('الأكونت خلص'))
        container.add_item(part2_row)
        container.add_item(Separator())

        # Part 3: acc content (multiline-safe) - MAKE SURE THIS IS PRESERVED
        if acc:
            # Clean the acc content - remove any existing code block markers
            clean_acc = str(acc).replace('```', '').strip()
            container.add_item(TextDisplay(f'```{clean_acc}```'))
        else:
            container.add_item(TextDisplay('```No account content provided```'))
        container.add_item(Separator())

        # Part 4: text and a red button on the same line
        part4_row = Section(accessory=Button(label='اتبند', style=ButtonStyle.red, emoji='⛔', custom_id='pending_banned'))
        part4_row.add_item(TextDisplay('لو اتبند'))
        container.add_item(part4_row)

        self.add_item(container)

    async def finished_callback(self, button : Button, interaction: Interaction):
        if self.game == 'bo7':
                view = View()
                view.add_item(Bo7FinishSelect(self, 
                    guild_id=self.guild_id,
                    parent_message=interaction.message,
                    original_content=interaction.message.content,
                    uid=self.uid,
                    acc=self.acc,
                    ))
                await interaction.response.send_message('اختار نوع الكامو:', view=view, ephemeral=True)
        else:
            await self._open_game_modal(interaction)

    async def _open_game_modal(self, interaction: Interaction, camo_type: str | None = None):
        if self.game == 'ow2':
            await interaction.response.send_modal(
                OW2(
                    guild_id = self.guild_id,
                    parent_message=interaction.message,
                    original_content=interaction.message.content,
                    uid = self.uid,
                    acc=self.acc
                )
            )
        elif self.game == 'rivals':
            await interaction.response.send_modal(
                Rivals(
                    guild_id = self.guild_id,
                    parent_message=interaction.message,
                    original_content=interaction.message.content,
                    uid = self.uid,
                    acc=self.acc
                )
            )
        elif self.game == 'battlefield6':
            await interaction.response.send_modal(
                BF6(
                guild_id=self.guild_id,
                parent_message=interaction.message,
                original_content=interaction.message.content,
                uid=self.uid,
                acc=self.acc
                )
            )
        elif self.game == 'warzone':
            await interaction.response.send_modal(
                Warzone(
                guild_id=self.guild_id,
                parent_message=interaction.message,
                original_content=interaction.message.content,
                uid=self.uid,
                acc=self.acc
                )
            )

class Money(Modal):
    def __init__(self,guild_id,msg,uid,acc: str | None = None):
        super().__init__(title='Price 🏷️')
        self.add_item(TextInput(label='Price',placeholder='حط تمن الاكونت هنا'))
        self.guild_id = guild_id
        self.msg = msg
        self.uid = uid
        self.acc = acc

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            price = int(self.children[0].value)
        except ValueError:
            return await interaction.followup.send('حط سعر الاكونت كا رقم بس')
        db.log_account(self.uid,'sold',price)
        await interaction.followup.send('مليونير مليونير 💸',ephemeral=True)
        channel = interaction.channel   
        category_name = "Paid 💰"
        emoji = "💰"
        color = 0x10b8c4
        title = "الكاش وصل يا برو 🤑"
        desc = f'**Price**\n```{price} L.E```'
        await move_channel(channel,category_name,emoji,color,title,desc)
        
        # Build final view with no buttons, just text (mention, account content, price)
        final_view = self._build_final_view(price)
        await self.msg.edit(view=final_view)

    def _build_final_view(self, price: int) -> LayoutView:
        """Build final view with no buttons, just text: mention, account content, price"""
        container = Container()
        
        # Part 1: user mention - PRESERVED
        container.add_item(TextDisplay(f'# <@{self.uid}>'))
        container.add_item(Separator())
        
        # Part 2: account content - PRESERVED
        if self.acc:
            clean_acc = str(self.acc).replace('```', '').strip()
            container.add_item(TextDisplay(f'```{clean_acc}```'))
        
        # Wallets registered under account content
        try:
            data = db.find_player(self.uid)
        except Exception:
            data = None
        if data is not None:
            wallets = data.get('wallets', {}) if isinstance(data, dict) else {}
            visa_data = wallets.get('visa', [])
            vodafone_data = wallets.get('vodafone', [])
            instapay_data = wallets.get('instapay', [])

            has_any = bool(visa_data or vodafone_data or instapay_data)
            if has_any:
                container.add_item(Separator())
                container.add_item(TextDisplay('المحافظ المسجلة'))
                if visa_data:
                    for card in visa_data:
                        holder = card.get('holder name', '') if isinstance(card, dict) else ''
                        number = card.get('number', '') if isinstance(card, dict) else ''
                        container.add_item(TextDisplay(f"💳 {holder} — {number}"))
                if vodafone_data:
                    for num in vodafone_data:
                        container.add_item(TextDisplay(f"📱 {num}"))
                if instapay_data:
                    for num in instapay_data:
                        container.add_item(TextDisplay(f"🆔 {num}"))
        
        container.add_item(Separator())
        
        # Part 3: price
        container.add_item(TextDisplay(f'**Price**\n```{price} L.E```'))
        
        view = LayoutView()
        view.add_item(container)
        return view

class MarkSoldLayout(LayoutView):
    def __init__(self, guild_id, uid: int, acc: str | None = None):
        super().__init__(timeout=None)
        self.guild_id = guild_id
        self.uid = uid
        self.acc = acc

        container = Container()

        # Part 1: user mention - PRESERVED
        container.add_item(TextDisplay(f'# <@{uid}>'))
        container.add_item(Separator())

        # Part 2: text and a "mark sold" button on the same line
        mark_sold_btn = Button(label='سلمت الاكونت', style=ButtonStyle.blurple, emoji='📦', custom_id='marksold_sold')
        async def _mark_sold_on_click(interaction: Interaction):
            # Move channel to Sold category
            channel = interaction.channel
            category_name = "Sold 📦"
            emoji = "📦"
            color = 0x038c07
            title = "الكاش 💰"
            desc = 'دوس علي الزرار اللي تحت لما فلوس الاكونت توصلك'
            await move_channel(channel, category_name, emoji, color, title, desc)
            
            # Edit message to show "cash in" button
            updated_view = CashInLayout(self.guild_id, self.uid, self.acc)
            await interaction.message.edit(view=updated_view)
            await interaction.response.send_message('تم تسجيل البيع 📦', ephemeral=True)
        mark_sold_btn.callback = _mark_sold_on_click
        part2_row = Section(accessory=mark_sold_btn)
        part2_row.add_item(TextDisplay('الأكونت اتسلم'))
        container.add_item(part2_row)
        container.add_item(Separator())

        # Part 3: acc content - PRESERVED
        if acc:
            clean_acc = str(acc).replace('```', '').strip()
            container.add_item(TextDisplay(f'```{clean_acc}```'))
        else:
            container.add_item(TextDisplay('```No account content provided```'))

        # Wallets registered under account content
        try:
            data = db.find_player(uid)
        except Exception:
            data = None
        if data is not None:
            wallets = data.get('wallets', {}) if isinstance(data, dict) else {}
            visa_data = wallets.get('visa', [])
            vodafone_data = wallets.get('vodafone', [])
            instapay_data = wallets.get('instapay', [])

            has_any = bool(visa_data or vodafone_data or instapay_data)
            if has_any:
                container.add_item(Separator())
                container.add_item(TextDisplay('المحافظ المسجلة'))
                if visa_data:
                    for card in visa_data:
                        holder = card.get('holder name', '') if isinstance(card, dict) else ''
                        number = card.get('number', '') if isinstance(card, dict) else ''
                        container.add_item(TextDisplay(f"💳 {holder} — {number}"))
                if vodafone_data:
                    for num in vodafone_data:
                        container.add_item(TextDisplay(f"📱 {num}"))
                if instapay_data:
                    for num in instapay_data:
                        container.add_item(TextDisplay(f"🆔 {num}"))

        container.add_item(Separator())

        # Part 4: banned option
        banned_btn = Button(label='اتبند', style=ButtonStyle.red,emoji='⛔', custom_id='marksold_banned')
        async def _banned_on_click(interaction: Interaction):
            msg = interaction.message
            channel = interaction.channel
            category_name = "Banned ⛔"
            emoji = "⛔"
            color = 0xE80000
            title = "Banned ⛔"
            desc = 'الاكونت اتبند ! ربنا يعوض عليك يا برو شوفلك'
            try:
                await move_channel(channel, category_name, emoji, color, title, desc)
            except Exception:
                pass
            # Edit message with LayoutView: Part 1 = mention, Part 2 = desc
            banned_view = LayoutView()
            banned_container = Container()
            banned_container.add_item(TextDisplay(f'# <@{self.uid}>'))
            banned_container.add_item(Separator())
            banned_container.add_item(TextDisplay(desc))
            banned_view.add_item(banned_container)
            await msg.edit(view=banned_view)
            await interaction.response.send_message("gg go next 😥", ephemeral=True)
            db.log_account(self.uid, 'banned')
        banned_btn.callback = _banned_on_click
        part4_row = Section(accessory=banned_btn)
        part4_row.add_item(TextDisplay('لو اتبند'))
        container.add_item(part4_row)

        self.add_item(container)

class CashInLayout(LayoutView):
    def __init__(self, guild_id, uid: int, acc: str | None = None):
        super().__init__(timeout=None)
        self.guild_id = guild_id
        self.uid = uid
        self.acc = acc

        container = Container()

        # Part 1: user mention - PRESERVED
        container.add_item(TextDisplay(f'# <@{uid}>'))
        container.add_item(Separator())

        # Part 2: text and a "cash in" button on the same line (triggers Money modal)
        cash_in_btn = Button(label='استلمت الكاش', style=ButtonStyle.green, emoji='💰', custom_id='cashin_paid')
        async def _cash_in_on_click(interaction: Interaction):
            await interaction.response.send_modal(Money(self.guild_id, interaction.message, self.uid, acc=self.acc))
        cash_in_btn.callback = _cash_in_on_click
        part2_row = Section(accessory=cash_in_btn)
        part2_row.add_item(TextDisplay('الكاش 💰'))
        container.add_item(part2_row)
        container.add_item(Separator())

        # Part 3: acc content - PRESERVED
        if acc:
            clean_acc = str(acc).replace('```', '').strip()
            container.add_item(TextDisplay(f'```{clean_acc}```'))
        else:
            container.add_item(TextDisplay('```No account content provided```'))

        # Wallets registered under account content
        try:
            data = db.find_player(uid)
        except Exception:
            data = None
        if data is not None:
            wallets = data.get('wallets', {}) if isinstance(data, dict) else {}
            visa_data = wallets.get('visa', [])
            vodafone_data = wallets.get('vodafone', [])
            instapay_data = wallets.get('instapay', [])

            has_any = bool(visa_data or vodafone_data or instapay_data)
            if has_any:
                container.add_item(Separator())
                container.add_item(TextDisplay('المحافظ المسجلة'))
                if visa_data:
                    for card in visa_data:
                        holder = card.get('holder name', '') if isinstance(card, dict) else ''
                        number = card.get('number', '') if isinstance(card, dict) else ''
                        container.add_item(TextDisplay(f"💳 {holder} — {number}"))
                if vodafone_data:
                    for num in vodafone_data:
                        container.add_item(TextDisplay(f"📱 {num}"))
                if instapay_data:
                    for num in instapay_data:
                        container.add_item(TextDisplay(f"🆔 {num}"))

        container.add_item(Separator())

        # Part 4: banned option
        banned_btn = Button(label='اتبند', style=ButtonStyle.red,emoji='⛔', custom_id='cashin_banned')
        async def _banned_on_click(interaction: Interaction):
            msg = interaction.message
            channel = interaction.channel
            category_name = "Banned ⛔"
            emoji = "⛔"
            color = 0xE80000
            title = "Banned ⛔"
            desc = 'الاكونت اتبند ! ربنا يعوض عليك يا برو شوفلك'
            try:
                await move_channel(channel, category_name, emoji, color, title, desc)
            except Exception:
                pass
            # Edit message with LayoutView: Part 1 = mention, Part 2 = desc
            banned_view = LayoutView()
            banned_container = Container()
            banned_container.add_item(TextDisplay(f'# <@{self.uid}>'))
            banned_container.add_item(Separator())
            banned_container.add_item(TextDisplay(desc))
            banned_view.add_item(banned_container)
            await msg.edit(view=banned_view)
            await interaction.response.send_message("gg go next 😥", ephemeral=True)
            db.log_account(self.uid, 'banned')
        banned_btn.callback = _banned_on_click
        part4_row = Section(accessory=banned_btn)
        part4_row.add_item(TextDisplay('لو اتبند'))
        container.add_item(part4_row)

        self.add_item(container)

async def setup(client):
    pass