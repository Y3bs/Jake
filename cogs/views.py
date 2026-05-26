import discord,re
from discord import ButtonStyle,Button,Interaction, MediaGalleryComponent, SelectOption,Color, TextStyle
from discord.components import MediaGalleryItem
from discord.ui import ActionRow, Container, File, Label, LayoutView, Section, Separator, View,Button,Modal,TextInput, TextDisplay, Select, MediaGallery, media_gallery
from utils.utils import EMOJIS, copy_content,move_channel,create_banned_callback,extract_user_id_from_text,get_game_display_name,get_game_emoji
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
        game_display_name = get_game_display_name(self.game)
        game_emoji = get_game_emoji(self.game)
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
        banned_btn.callback = create_banned_callback(self,self.game)  
        part4_row = Section(accessory=banned_btn)
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
    def __init__(self, guild_id, uid: int, acc: str | None = None,game:str | None = None):
        super().__init__(timeout=None)
        self.guild_id = guild_id
        self.uid = uid
        self.acc = acc
        self.game = game

        container = Container()

        # Part 1: user mention - PRESERVED
        container.add_item(TextDisplay(f'# <@{uid}>'))
        container.add_item(Separator())

        # NEW PART: Game title with emoji from utils.py
        
        game_display_name = get_game_display_name(self.game)
        game_emoji = get_game_emoji(self.game)
        game_title = TextDisplay(f'## {game_emoji} {game_display_name}')
        container.add_item(game_title)
        container.add_item(Separator())

        # Part 2: text and a "mark sold" button on the same line
        mark_sold_btn = Button(label='سلمت الاكونت', style=ButtonStyle.blurple, emoji='📦', custom_id='marksold_sold')
        async def _mark_sold_on_click(interaction: Interaction):
            # Move channel to Sold category
            await move_channel(interaction.channel,"Sold 📦" , "📦")
            
            # Edit message to show "cash in" button
            updated_view = CashInLayout(self.guild_id, self.uid, self.acc,self.game)
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
            e_wallet_data = wallets.get('e-wallet', [])
            instapay_data = wallets.get('instapay', [])
            wallets_data = []
            has_any = bool(visa_data or e_wallet_data or instapay_data)
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
                            'value':f'visa|{holder}\n{number}',
                            'emoji': EMOJIS['visa'],
                        })
                if e_wallet_data:
                    for num in e_wallet_data:
                        container.add_item(TextDisplay(f"{EMOJIS['ewallet']} **E-Wallet** ```{num}```"))
                        wallets_data.append({
                            'label':num,
                            'value':f'ewallet|{num}',
                            'emoji':EMOJIS['ewallet']
                        })
                if instapay_data:
                    for num in instapay_data:
                        container.add_item(TextDisplay(f"{EMOJIS['instapay']} **Instapay** ```ansi\n[35m{num}[0m```"))
                        wallets_data.append({
                            'label':num,
                            'value':f'instapay|{num}',
                            'emoji':EMOJIS['instapay']
                        })
            if wallets_data:
                options = []
                for option in wallets_data:
                    options.append(SelectOption(label=option['label'],value=option['value'],emoji=option['emoji']))
                copy_payments_row = ActionRow(CopyPayment(options))
                container.add_item(copy_payments_row)
        container.add_item(Separator())

        # # Part 4: banned option
        banned_btn = Button(label='اتبند', style=ButtonStyle.red,emoji='⛔', custom_id='marksold_banned')
        banned_btn.callback = create_banned_callback(self,self.game)  # Use helper function
        part4_row = Section(accessory=banned_btn)
        part4_row.add_item(TextDisplay('لو اتبند'))
        container.add_item(part4_row)

        self.add_item(container)

class CashInLayout(LayoutView):
    def __init__(self, guild_id, uid: int, acc: str | None = None,game:str | None = None):
        super().__init__(timeout=None)
        self.guild_id = guild_id
        self.uid = uid
        self.acc = acc
        self.game = game

        container = Container()

        # Part 1: user mention - PRESERVED
        container.add_item(TextDisplay(f'# <@{uid}>'))
        container.add_item(Separator())

        # NEW PART: Game title with emoji from utils.py
        game_display_name = get_game_display_name(self.game)
        game_emoji = get_game_emoji(self.game)
        game_title = TextDisplay(f'## {game_emoji} {game_display_name}')
        container.add_item(game_title)
        container.add_item(Separator())

        # Part 2: text and a "cash in" button on the same line (triggers Money modal)
        cash_in_btn = Button(label='استلمت الكاش', style=ButtonStyle.green, emoji='💰', custom_id='cashin_paid')
        async def _cash_in_on_click(interaction: Interaction):
            await interaction.response.send_modal(Money(self.guild_id, interaction.message, self.uid, acc=self.acc, game=self.game))
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
            e_wallet_data = wallets.get('e-wallet', [])
            instapay_data = wallets.get('instapay', [])
            wallets_data = []
            has_any = bool(visa_data or e_wallet_data or instapay_data)
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
                            'value':f'visa|{holder}\n{number}',
                            'emoji': EMOJIS['visa'],
                        })
                if e_wallet_data:
                    for num in e_wallet_data:
                        container.add_item(TextDisplay(f"{EMOJIS['ewallet']} **E-Wallet** ```{num}```"))
                        wallets_data.append({
                            'label':num,
                            'value':f'ewallet|{num}',
                            'emoji':EMOJIS['ewallet']
                        })
                if instapay_data:
                    for num in instapay_data:
                        container.add_item(TextDisplay(f"{EMOJIS['instapay']} **Instapay** ```ansi\n[35m{num}[0m```"))
                        wallets_data.append({
                            'label':num,
                            'value':f'instapay|{num}',
                            'emoji':EMOJIS['instapay']
                        })
            if wallets_data:
                options = []
                for option in wallets_data:
                    options.append(SelectOption(label=option['label'],value=option['value'],emoji=option['emoji']))
                copy_payments_row = ActionRow(CopyPayment(options))
                container.add_item(copy_payments_row)
        container.add_item(Separator())

        # # Part 4: banned option
        banned_btn = Button(label='اتبند', style=ButtonStyle.red,emoji='⛔', custom_id='marksold_banned')
        banned_btn.callback = create_banned_callback(self,self.game)  
        part4_row = Section(accessory=banned_btn)
        part4_row.add_item(TextDisplay('لو اتبند'))
        container.add_item(part4_row)

        self.add_item(container)

class Money(Modal):
    def __init__(self,guild_id,msg,uid,acc: str | None = None,game: str | None = None):
        super().__init__(title='Price 🏷️')
        self.add_item(TextInput(label='Price',placeholder='حط تمن الاكونت هنا'))
        self.method = Label(text = 'Wallet type 💳',component=Method())
        self.add_item(self.method)
        self.guild_id = guild_id
        self.msg = msg
        self.uid = uid
        self.acc = acc
        self.game = game

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            price = int(self.children[0].value)
        except ValueError:
            return await interaction.followup.send('حط سعر الاكونت كا رقم بس')
        if not db.find_player(self.uid):
            db.save_player(self.uid)
        method = self.method.component.values[0]
        # db.log_account(self.uid,'sold',price)
        db.log_rec(self.uid,'sold',self.game,interaction.channel.name[1:],price,method)
        await interaction.followup.send('مليونير مليونير 💸',ephemeral=True)
        # await move_channel(interaction.channel,"Paid 💰","💰")
        
        # Build final view with no buttons, just text (mention, account content, price)
        final_view = self._build_final_view(price,method,interaction.channel.name)
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name='Paid 💰')
        if category is None:
            category = await guild.create_category("Paid 💰")
        ch = self._is_game_logs_channel(category,self.game)
        if ch is None:
            ch = await category.create_text_channel(f'🗂️{self.game}-logs')
            await ch.send(view=final_view)
        else:
            await ch.send(view=final_view)
        await interaction.channel.delete()
    
    def _is_game_logs_channel(self,category,game):
        cat_channels = category.channels
        target = f'{game}-logs'
        for ch in cat_channels:
            if target in ch.name:
                return ch
        return None

    def _build_final_view(self, price: int,method:str,channel_name:str) -> LayoutView:
        """Build final view with no buttons, just text: mention, account content, price"""
        container = Container()
        
        # Part 1: Game title with emoji from utils.py
        game_display_name = get_game_display_name(self.game)
        game_emoji = get_game_emoji(self.game)
        game_title = TextDisplay(f'## {game_emoji} {game_display_name}')
        container.add_item(game_title)
        container.add_item(Separator())
        
        # Part 2: account content - PRESERVED
        container.add_item(TextDisplay(f'🏷️ **Type**'))
        container.add_item(TextDisplay(f"```{channel_name[1:]}```"))
        container.add_item(Separator())
        
        # Part 3: price
        container.add_item(TextDisplay(f'💰 **Price**'))
        container.add_item(TextDisplay(f"```ansi\n[32m {price} [0m L.E 💵```"))
        container.add_item(Separator())
        
        # Part 4: Method
        container.add_item(TextDisplay(f'💳 **Method**'))
        container.add_item(TextDisplay(f'{EMOJIS[method]} **{method.capitalize()}**'))

        view = LayoutView()
        view.add_item(container)
        return view

class Method(Select):
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
        value = self.values[0]
        for prefix in ('visa|', 'ewallet|', 'instapay|'):
            if value.startswith(prefix):
                value = value[len(prefix):]
                break
        await interaction.response.send_message(value, ephemeral=True)

class ArcItemsRarity(Select):
    def __init__(self):
        options = [
            SelectOption(label='Common',value='```ansi\n[30mCommon[0m```',emoji='⚫'),
            SelectOption(label='Uncommon',value='```ansi\n[32mUncommon[0m```',emoji='🟢'),
            SelectOption(label='Rare',value='```ansi\n[34mRare[0m```',emoji='🔵'),
            SelectOption(label='Epic',value='```ansi\n[35mEpic[0m```',emoji='🟣'),
            SelectOption(label='Legendary',value='```ansi\n[33mLegendary[0m```',emoji='🟡')
        ]
        super().__init__(
            placeholder='حدد نوع ال item',
            min_values=1,
            max_values=1,
            options=options,
            custom_id='arc_items_type_selector'
        )
    
    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(self.values[0])

class ArcItems(Modal):
    def __init__(self,logs_ch):
        super().__init__(title='🛠️ Arc Items')
        self.logs_ch = logs_ch

        self.item_name= TextInput(label='الاسم ، النوع',style=TextStyle.short,placeholder='حط الاسم  الاول وبعديه النوع مفصولين بعلامة ,')
        self.add_item(self.item_name)

        self.item_rare = Label(text='الندرة',component=ArcItemsRarity())
        self.add_item(self.item_rare)

        self.item_qnt = TextInput(label='الكمية')
        self.add_item(self.item_qnt)

        self.item_price = TextInput(label='سعر القطعة الواحدة',placeholder='سعر القطعة الواحدة مش مجموعهم')
        self.add_item(self.item_price)

        self.money_method = Label(text='المحفظة',component=Method())
        self.add_item(self.money_method)
    async def on_submit(self, interaction: Interaction):
        container = Container()
        title = TextDisplay(f'# {EMOJIS['items']} Item Sold')
        container.add_item(title)
        container.add_item(Separator())

        name_type = self.item_name.value.split(',')
        name = name_type[0]
        type = name_type[1] if len(name_type) == 2 else None
        rare = self.item_rare.component.values[0]
        try:
            qnt = int(self.item_qnt.value)
            price = int(self.item_price.value)
        except:
            return await interaction.response.send_message('لازم الكمية والسعر يكون ارقام فقط',ephemeral=True)
        method = str(self.money_method.component.values[0])

        nameplace = TextDisplay(f"**📝 Name**\n```{name.capitalize()}```")
        container.add_item(nameplace)

        typeplace = TextDisplay(f'**🏷️ Type**\n```{type.capitalize() if type is not None else 'No type provided'}```')
        container.add_item(typeplace)

        rarity = TextDisplay(f'**✨ Rarity**\n{rare}')
        container.add_item(rarity)

        qntplace = TextDisplay(f'**📦 Quantity**\n```{qnt}```')
        container.add_item(qntplace)

        total_price = TextDisplay(f'**💰 Total Price**\n```ansi\n[32m{qnt*price}[0m L.E 💵```')     
        container.add_item(total_price)

        methodplace = TextDisplay(f'**💳 Method**\n{EMOJIS[method]} {method.capitalize()}')
        container.add_item(methodplace)

        view = LayoutView()
        view.add_item(container)
        db.log_rec(interaction.user.id,'sold','arc_raiders',name_type,qnt*price,method)
        await self.logs_ch.send(view=view)
        await interaction.response.send_message('تم التسجيل ✅',ephemeral=True)

class ArcCoins(Modal):
    def __init__(self,logs_ch):
        super().__init__(title='🪙 Arc Coins')
        self.logs_ch = logs_ch

        self.coins_qnt = TextInput(label='الكمية',placeholder='500k, 1m, 2m')
        self.add_item(self.coins_qnt)

        self.coins_price = TextInput(label='السعر',placeholder='سعر الكمية كلها ')
        self.add_item(self.coins_price)

        self.money_method = Label(text='المحفظة',component=Method())
        self.add_item(self.money_method)

    async def on_submit(self, interaction: Interaction):
        container = Container()
        title = TextDisplay(f'# {EMOJIS['coins']} Coins Sold')
        container.add_item(title)
        container.add_item(Separator())
        qtn = self.coins_qnt.value
        try:
            price = int(self.coins_price.value)
        except:
            return await interaction.response.send_message('لازم تكون الكمية او السعر ارقام فقط',ephemeral=True)
        
        method = self.money_method.component.values[0]

        qtnplace = TextDisplay(f'**📦 Quantity**\n```{qtn} 🪙```')
        container.add_item(qtnplace)

        priceplace = TextDisplay(f'**💰 Price**\n```ansi\n[32m {price} [0m L.E 💵```')  
        container.add_item(priceplace)

        methodplace = TextDisplay(f'**💳 Method**\n{EMOJIS[method]} {method.capitalize()}')
        container.add_item(methodplace)

        view = LayoutView()
        view.add_item(container)
        db.log_rec(interaction.user.id,'sold','arc_raiders','coins',price,method)
        await self.logs_ch.send(view=view)
        await interaction.response.send_message('تم التسجيل ✅',ephemeral=True)


class ArcRaiders(LayoutView):
    def __init__(self,logs_channel):
        super().__init__(timeout=None)
        self.logs_ch = logs_channel

        container = Container()
        container = Container(accent_color=Color.from_str('#2D004A'))
        # 
        title = TextDisplay(f'# {EMOJIS['arcraiders']} Arc Raiders')
        container.add_item(title)

        container.add_item(Separator())

        desc = TextDisplay('اختار نوع الحاجة اللي بعتها من الزرارين اللي تحت')
        container.add_item(desc)

        container.add_item(Separator())

        image_gallery = MediaGallery(
            MediaGalleryItem(media='https://cdn.discordapp.com/attachments/1248397856482656379/1466047428603019264/e4b522c99ecf0578997e685bb8452aae.png?ex=697b5290&is=697a0110&hm=cc994a8f4d42efee2e297fda3f5ab210f77e6037688bdd703c81669686ae54a3&')
        )
        container.add_item(image_gallery)
        container.add_item(Separator())

        btn_row = ActionRow()
        items_btn = Button(label ='Items - أغراض',style=ButtonStyle.blurple,emoji=EMOJIS['items'],custom_id='arcraider_items')
        items_btn.callback = self.items_callback
        btn_row.add_item(items_btn)

        coins_btn = Button(label='Coins - عملات',style=ButtonStyle.green,emoji=EMOJIS['coins'],custom_id='arcraider_coins')
        coins_btn.callback = self.coins_callback
        btn_row.add_item(coins_btn)

        container.add_item(btn_row)

        self.add_item(container)

    async def items_callback(self, interaction: Interaction):  
        await interaction.response.send_modal(ArcItems(self.logs_ch))

    async def coins_callback(self,interaction:Interaction):
        await interaction.response.send_modal(ArcCoins(self.logs_ch))
        

async def setup(client):
    pass