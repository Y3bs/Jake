import discord,re
from discord import ButtonStyle,Button,Interaction, SelectOption
from discord.ui import ActionRow, Container, Label, LayoutView, Section, Separator, View,Button,Modal,TextInput, TextDisplay, Select
from utils.utils import EMOJIS, copy_content,move_channel,create_banned_callback,extract_user_id_from_text
from cogs.game_modals import OW2, Bo7, SingularityBo7, BF6, Valorant, Warzone, Rivals
import utils.database as db

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
    def __init__(self, guild_id, uid, acc, game):
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
        # NEW PART: Game title with emoji from utils.py
        game_display_name = self._get_game_display_name(game)
        game_emoji = self._get_game_emoji(game)
        game_title = TextDisplay(f'## {game_emoji} {game_display_name}')
        container.add_item(game_title)
        
        container.add_item(Separator())
        
        # Part 2: text and a button on the same line
        finished_btn = Button(label='خلصت الاكونت', style=ButtonStyle.gray, emoji='🏁', custom_id='pending_finished')
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
            copy_btn = Button(label='نسخ',style=ButtonStyle.blurple, emoji='🖨️',custom_id='copy_btn')
            async def _copy_on_click(interaction: Interaction):
                await copy_content(interaction,clean_acc)
            copy_btn.callback = _copy_on_click
            part3_row = ActionRow(copy_btn)
            container.add_item(part3_row)
        else:
            container.add_item(TextDisplay('```No account content provided```'))
        
        container.add_item(Separator())

        # Part 4: text and a red button on the same line
        banned_btn = Button(label='اتبند', style=ButtonStyle.red, emoji='⛔', custom_id='pending_banned')
        banned_btn.callback = create_banned_callback(self)  
        part4_row = Section(accessory=banned_btn)
        part4_row.add_item(TextDisplay('لو اتبند'))
        container.add_item(part4_row)

        self.add_item(container)
    
    def _get_game_display_name(self, game):
        """Convert game key to display name"""
        game_names = {
            'bo7': 'BO7',
            'ow2': 'OW2',
            'rivals': 'RIVALS',
            'battlefield6': 'BATTLEFIELD6',
            'warzone': 'WARZONE',
            'valorant': 'VALORANT',
        }
        return game_names.get(game, game.upper())

    def _get_game_emoji(self, game):
        """Get appropriate emoji for each game from utils.py EMOJIS"""
        # Map game parameter to EMOJIS keys
        emoji_map = {
            'bo7': EMOJIS.get('bo7', '🎮'),
            'ow2': EMOJIS.get('ow2', '🔫'),
            'rivals': EMOJIS.get('rivals', '⚔️'),
            'battlefield6': EMOJIS.get('battlefield6', '🎖️'),
            'warzone': EMOJIS.get('wz', '☣️'),  
            'valorant': EMOJIS.get('valorant', '💥')
        }
        return emoji_map.get(game, EMOJIS.get('bo7', '🎮'))  # Default to BO7 emoji

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

    async def _open_game_modal(self, interaction: Interaction):
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
        elif self.game == 'valorant':
            await interaction.response.send_modal(
                Valorant(
                    guild_id=self.guild_id,
                    parent_message=interaction.message,
                    original_content=interaction.message.content,
                    uid=self.uid,
                    acc=self.acc
                )
            )

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
            await move_channel(interaction.channel,"Sold 📦" , "📦")
            
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
            copy_btn = Button(label='نسخ',style=ButtonStyle.blurple, emoji='🖨️')
            async def _copy_on_click(interaction: Interaction):
                await copy_content(interaction,clean_acc)
            copy_btn.callback = _copy_on_click
            part3_row = ActionRow(copy_btn)
            container.add_item(part3_row)
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
            wallets_data = []
            has_any = bool(visa_data or vodafone_data or instapay_data)
            if has_any:
                container.add_item(Separator())
                container.add_item(TextDisplay('💳 **المحافظ المسجلة**'))
                if visa_data:
                    for card in visa_data:
                        holder = card.get('holder name', '') if isinstance(card, dict) else ''
                        number = card.get('number', '') if isinstance(card, dict) else ''
                        container.add_item(TextDisplay(f"{EMOJIS['visa']} **Visa** ```ansi\n{holder} — [34m{number}[0m```"))
                        wallets_data.append({
                            'label':f'{holder} - {number}',
                            'value':f'{holder}\n{number}',
                            'emoji': EMOJIS['visa'],
                        })
                if vodafone_data:
                    for num in vodafone_data:
                        container.add_item(TextDisplay(f"{EMOJIS['vodafone']} **Vodafone Cash** ```ansi\n[31m{num}[0m```"))
                        wallets_data.append({
                            'label':num,
                            'value':num,
                            'emoji':EMOJIS['vodafone']
                        })
                if instapay_data:
                    for num in instapay_data:
                        container.add_item(TextDisplay(f"{EMOJIS['instapay']} **Instapay** ```ansi\n[35m{num}[0m```"))
                        wallets_data.append({
                            'label':num,
                            'value':num,
                            'emoji':EMOJIS['instapay']
                        })
            if wallets_data:
                options = []
                for option in wallets_data:
                    options.append(SelectOption(label=option['label'],value=option['value'],emoji=option['emoji']))
                copy_payments_row = ActionRow(CopyPayment(options))
                container.add_item(copy_payments_row)
        container.add_item(Separator())

        # Part 4: banned option
        banned_btn = Button(label='اتبند', style=ButtonStyle.red,emoji='⛔', custom_id='marksold_banned')
        banned_btn.callback = create_banned_callback(self)  # Use helper function
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
            copy_btn = Button(label='نسخ',style=ButtonStyle.blurple, emoji='🖨️')
            async def _copy_on_click(interaction: Interaction):
                await copy_content(interaction,clean_acc)
            copy_btn.callback = _copy_on_click
            part3_row = ActionRow(copy_btn)
            container.add_item(part3_row)
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
            wallets_data = []
            has_any = bool(visa_data or vodafone_data or instapay_data)
            if has_any:
                container.add_item(Separator())
                container.add_item(TextDisplay('💳 **المحافظ المسجلة**'))
                if visa_data:
                    for card in visa_data:
                        holder = card.get('holder name', '') if isinstance(card, dict) else ''
                        number = card.get('number', '') if isinstance(card, dict) else ''
                        container.add_item(TextDisplay(f"{EMOJIS['visa']} **Visa** ```ansi\n{holder} — [34m{number}[0m```"))
                        wallets_data.append({
                            'label':f'{holder} - {number}',
                            'value':f'{holder}\n{number}',
                            'emoji': EMOJIS['visa'],
                        })
                if vodafone_data:
                    for num in vodafone_data:
                        container.add_item(TextDisplay(f"{EMOJIS['vodafone']} **Vodafone Cash** ```ansi\n[31m{num}[0m```"))
                        wallets_data.append({
                            'label':num,
                            'value':num,
                            'emoji':EMOJIS['vodafone']
                        })
                if instapay_data:
                    for num in instapay_data:
                        container.add_item(TextDisplay(f"{EMOJIS['instapay']} **Instapay** ```ansi\n[35m{num}[0m```"))
                        wallets_data.append({
                            'label':num,
                            'value':num,
                            'emoji':EMOJIS['instapay']
                        })
            if wallets_data:
                options = []
                for option in wallets_data:
                    options.append(SelectOption(label=option['label'],value=option['value'],emoji=option['emoji']))
                copy_payments_row = ActionRow(CopyPayment(options))
                container.add_item(copy_payments_row)
        container.add_item(Separator())

        # Part 4: banned option
        banned_btn = Button(label='اتبند', style=ButtonStyle.red,emoji='⛔', custom_id='marksold_banned')
        banned_btn.callback = create_banned_callback(self)  
        part4_row = Section(accessory=banned_btn)
        part4_row.add_item(TextDisplay('لو اتبند'))
        container.add_item(part4_row)

        self.add_item(container)

class Money(Modal):
    def __init__(self,guild_id,msg,uid,acc: str | None = None):
        super().__init__(title='Price 🏷️')
        self.add_item(TextInput(label='Price',placeholder='حط تمن الاكونت هنا'))
        self.method = Label(text = 'Wallet type 💳',component=Method())
        self.add_item(self.method)
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
        method = self.method.component.values[0]
        db.log_account(self.uid,'sold',price)
        await interaction.followup.send('مليونير مليونير 💸',ephemeral=True)
        await move_channel(interaction.channel,"Paid 💰","💰")
        
        # Build final view with no buttons, just text (mention, account content, price)
        final_view = self._build_final_view(price,method)
        await self.msg.edit(view=final_view)

    def _build_final_view(self, price: int,method:str) -> LayoutView:
        """Build final view with no buttons, just text: mention, account content, price"""
        container = Container()
        
        # Part 1: user mention - PRESERVED
        container.add_item(TextDisplay(f'# <@{self.uid}>'))
        container.add_item(Separator())
        
        # Part 2: account content - PRESERVED
        if self.acc:
            clean_acc = str(self.acc).replace('```', '').strip()
            container.add_item(TextDisplay(f'```{clean_acc}```'))
        
        # Part 3: price
        container.add_item(TextDisplay(f'**Price**\n```ansi\n[32m {price} [0m L.E 💵```'))
        
        # Part 4: Method
        container.add_item(TextDisplay(f'**Method**\n{EMOJIS[method]} **{method.capitalize()}**'))

        view = LayoutView()
        view.add_item(container)
        return view

class Method(Select):
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
        await interaction.response.send_message(self.values[0])

class CopyPayment(Select):
    def __init__(self,options):        
        super().__init__(
            placeholder='اختار المحفظة اللي عايز تنسخها',
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(self.values[0],ephemeral=True)

async def setup(client):
    pass