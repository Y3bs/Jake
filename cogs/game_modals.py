from typing import Text
import discord
from discord import Interaction,Embed,PermissionOverwrite, SelectOption
from discord.ui import Modal,TextInput, Label, Select, Button, View,ChannelSelect
from discord.ui.text_input import TextStyle
# from utils.utils import EMOJIS
from utils.emojis import EMOJIS
# Avoid importing views at module load to prevent circular imports

class WeaponSelect1(Select):
    def __init__(self):
        options = [
            # AR
            SelectOption(label='M15 MOD 0', value='M15 MOD 0', emoji=EMOJIS['m15']),
            SelectOption(label='AK-27', value='AK-27', emoji=EMOJIS['ak27']),
            SelectOption(label='MXR-17', value='MXR-17', emoji=EMOJIS['mxr17']),
            SelectOption(label='X9 Maverick', value='X9 Maverick', emoji=EMOJIS['x9']),
            SelectOption(label='DS20 Mirage', value='DS20 Mirage', emoji=EMOJIS['ds20']),
            SelectOption(label='Peacekeeper MK1', value='Peacekeeper MK1', emoji=EMOJIS['mk1']),
            # smg
            SelectOption(label='Ryden 45K', value='Ryden 45K', emoji=EMOJIS['Ryden_45K']),
            SelectOption(label='RK-9', value='RK-9', emoji=EMOJIS['RK9']),
            SelectOption(label='Razor 9mm', value='Razor 9mm', emoji=EMOJIS['Razor_9mm']),
            SelectOption(label='Dravec 45', value='Dravec 45', emoji=EMOJIS['Dravec_45']),
            SelectOption(label='Carbon 57', value='Carbon 57', emoji=EMOJIS['Carbon_57']),
            SelectOption(label='MPC-25', value='MPC-25', emoji=EMOJIS['MPC25']),
            # shotgun
            SelectOption(label='M10 Breacher',value='M10 Breacher',emoji = EMOJIS['M10_Breacher']),
            SelectOption(label='Echo 12',value='Echo 12',emoji = EMOJIS['Echo_12']),
            SelectOption(label='Akita',value='Akita',emoji = EMOJIS['Akita']),
        ]
        super().__init__(
            min_values=0,
            max_values=len(options),
            options=options,
            required=False,
            placeholder='Choose weapons... '
        )

    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(self.values[0])

class WeaponSelect2(Select):
    def __init__(self):
        options = [
            # LMG
            SelectOption(label='MK.78',value='MK.78',emoji = EMOJIS['MK78']),
            SelectOption(label='XM325',value='XM325',emoji = EMOJIS['XM325']),
            # Marksman
            SelectOption(label='M8A1',value='M8A1',emoji = EMOJIS['M8A1']),
            SelectOption(label='Warden 308',value='Warden 308',emoji = EMOJIS['Warden_308']),
            SelectOption(label='M34 Novaline',value='M34 Novaline',emoji = EMOJIS['M34_Novaline']),
            # Sniper
            SelectOption(label='VS Recon',value='VS Recon',emoji = EMOJIS['VS_Recon']),
            SelectOption(label='Shadow SK',value='Shadow SK',emoji = EMOJIS['Shadow_SK']),
            SelectOption(label='XR-3 Ion',value='XR-3 Ion',emoji = EMOJIS['XR3_Ion']),
            # # Pistol
            SelectOption(label='Jager 45',value='Jager 45',emoji = EMOJIS['Jager_45']),
            SelectOption(label='Velox 5.7',value='Velox 5.7',emoji = EMOJIS['Velox_5']),
            SelectOption(label='Coda 9',value='Coda 9',emoji = EMOJIS['Coda_9']),
            # # Launcher
            SelectOption(label='AAROW 109',value='AAROW 109',emoji = EMOJIS['AAROW_109']),
            SelectOption(label='A.R.C. M1',value='A.R.C. M1',emoji = EMOJIS['A_R_C_M1']),
            # # Knife
            SelectOption(label='Knife',value='Knife',emoji = EMOJIS['Knife']),
            SelectOption(label='Flatline Mk.II',value='Flatline Mk.II',emoji = EMOJIS['Flatline_Mkii']),
        ]
        super().__init__(
            min_values=0,
            max_values=len(options),
            options=options,
            required=False,
            placeholder='Choose weapons...'
        )

    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(self.values[0])

class Operators(ChannelSelect):
    def __init__(self):
        options = [
            # Null
            SelectOption(label='No OPS',value='No Operators',emoji='🪹'),
            # OPS
            SelectOption(label='50/50', value='50/50', emoji=EMOJIS['5050operator']),
            SelectOption(label='Anderson', value='Anderson', emoji=EMOJIS['andersonoperator']),
            SelectOption(label='Carver', value='Carver', emoji=EMOJIS['carveroperator']),
            SelectOption(label='Dempsey', value='Dempsey', emoji=EMOJIS['dempseyoperator1']),
            SelectOption(label='Falkner', value='Falkner', emoji=EMOJIS['falkneroperator']),
            SelectOption(label='Grey', value='Grey', emoji=EMOJIS['greyoperator']),
            SelectOption(label='Grimm', value='Grimm', emoji=EMOJIS['grimmoperator']),
            SelectOption(label='Harper', value='Harper', emoji=EMOJIS['harperoperator']),
            SelectOption(label='Jurado', value='Jurado', emoji=EMOJIS['juradooperator']),
            SelectOption(label='Kagan', value='Kagan', emoji=EMOJIS['kaganoperator']),
            SelectOption(label='Karma', value='Karma', emoji=EMOJIS['karmaoperator']),
            SelectOption(label='Mason', value='Mason', emoji=EMOJIS['masonoperator']),
            SelectOption(label='Maya', value='Maya', emoji=EMOJIS['mayaoperator']),
            SelectOption(label='Nikolai', value='Nikolai', emoji=EMOJIS['nikolaioperator1']),
            SelectOption(label='Razor', value='Razor', emoji=EMOJIS['razoroperator']),
            SelectOption(label='Reaper', value='Reaper', emoji=EMOJIS['reaperewr3operator']),
            SelectOption(label='Richtofen', value='Richtofen', emoji=EMOJIS['richtofenoperator1']),
            SelectOption(label='Samuels', value='Samuels', emoji=EMOJIS['samuelsoperator']),
            SelectOption(label='Takeo', value='Takeo', emoji=EMOJIS['takeooperator1']),
            SelectOption(label='T.E.D.D.', value='T.E.D.D.', emoji=EMOJIS['teddoperator']),
            SelectOption(label='Vermaak', value='Vermaak', emoji=EMOJIS['vermaakoperator']),
            SelectOption(label='Weaver', value='Weaver', emoji=EMOJIS['weaveroperator']),
            SelectOption(label='Wei Lin', value='Wei Lin', emoji=EMOJIS['weilinoperator']),
            SelectOption(label='Zaveri', value='Zaveri', emoji=EMOJIS['zaverioperator']),
        ]
        super().__init__(
            min_values=1,
            max_values=len(options),
            options=options,
            required=False,
            placeholder='Choose operators'
        )

    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(self.values[0])

class Bo7(Modal):
    def __init__(self, guild_id, parent_message=None, original_content: str = "", uid: int | None = None, acc: str | None = None ,camo_type:str | None = None):
        super().__init__(title="Account Details")
        self.guild_id = guild_id
        self.parent_message = parent_message
        self.original_content = original_content
        self.uid = uid
        self.acc = acc
        self.camo = camo_type
        # 1) Integer input (Level)
        self.level_input = TextInput(label="Level/Prestige", style=TextStyle.short, placeholder=" حط لفل الاكونت والبرستيج وبينهم علامة ,", required=True)
        self.add_item(self.level_input)

        # 2) Dropdown (Ready for Rank / Not Ready for Rank)
        # self.rank_dropdown = Label(text='Select account type', component=RankNoRank())
        # self.add_item(self.rank_dropdown)

        # 3) Dropdown list for maxed weapons
        self.weapon_select1 = Label(text='Select maxed weapons (AR, SMG, Shotguns)...', component=WeaponSelect1())
        self.add_item(self.weapon_select1)

        # 4) Dropdown list for gold camos weapons
        self.weapon_select2 = Label(text='Select maxed weapons (LMG, Marksman, etc)...',component=WeaponSelect2())
        self.add_item(self.weapon_select2)

        # 5) Dropdown list for archlight camos weapons
        self.camo_select1 = Label(text='Select camo weapons (AR, SMG, Shotguns)...',component=WeaponSelect1())
        self.add_item(self.camo_select1)

        # 5) Dropdown list for archlight camos weapons
        self.camo_select2 = Label(text='Select camo weapons (LMG, Marksman, etc)...',component=WeaponSelect2())
        self.add_item(self.camo_select2)
        
    async def on_submit(self, interaction: Interaction):
        # Validate integer level
        try:
            level_prestige = self.level_input.value.split(',')
            level = level_prestige[0]
            prestige = level_prestige[1]
        except (TypeError, ValueError):
            return await interaction.response.send_message('حط لفل الاكونت كرقم', ephemeral=True)

        # rank = self.rank_dropdown.component.values[0]
        guns1 = self.weapon_select1.component.values if self.weapon_select1.component.values else []
        guns2 = self.weapon_select2.component.values if self.weapon_select2.component.values else []
        guns = guns1 + guns2
        camos1 = self.camo_select1.component.values if self.camo_select1.component.values else []
        camos2 = self.camo_select2.component.values if self.camo_select1.component.values else []
        camos = camos1 + camos2
        guild = interaction.guild
        # rank = 'rfr' if rank == 'rfr' else 'norfr'
        if self.camo == 'arclight':
            account_name = f'bo7-{level}-{len(camos)}-arc-{len(guns)}-max'
        elif self.camo == 'gold':
            account_name = f'bo7-{level}-{len(camos)}-gold-{len(guns)}-max'
        elif self.camo == 'max':
            account_name = f'bo7-{level}-{len(guns)}-max'
        else:
            account_name = f'bo7-{level}'
        # Build account content string from modal data
        acc_content_parts = []
        # Include original account content if it exists
        if self.acc:
            acc_content_parts.append("")
            acc_content_parts.append(str(self.acc)+'\n')
        acc_content_parts.append(f"Level: {level}")
        acc_content_parts.append(f"Prestige: {prestige}")
        # acc_content_parts.append(f"Rank: {'RFR' if rank == 'rfr' else 'NoRFR'}")
        acc_content_parts.append(f"Maxed Weapons: {guns if guns != [] else None}")
        acc_content_parts.append(f"Gold camos: {camos if self.camo == 'gold' else None}")
        acc_content_parts.append(f"Archlight camos: {camos if self.camo == 'arclight' else None}")
        acc_content_parts.append(f"Singularity camos: {camos if self.camo == 'singularity' else None}")
        
        acc_content = "\n".join(acc_content_parts)
        
        # Update the original pending message to MarkSoldLayout with account content
        if self.parent_message is not None:
            try:
                from cogs.views import MarkSoldLayout  # local import to avoid circular
                updated_view = MarkSoldLayout(self.guild_id, self.uid, acc=acc_content)
                await self.parent_message.edit(view=updated_view)
            except Exception as e:
                print(f"Error updating message view: {e}")
        
        # Move current channel to For Sale with the edited message
        if self.parent_message is not None:
            sale_category = discord.utils.get(guild.categories, name="For Sale 🏷️")
            if sale_category is None:
                sale_category = await guild.create_category("For Sale 🏷️")
            try:
                await self.parent_message.channel.edit(category=sale_category, name=f"🏷️{account_name}")
            except Exception:
                pass

        # Acknowledge submission ephemerally
        try:
            await interaction.response.send_message("تم حفظ التفاصيل ✅", ephemeral=True)
        except Exception:
            pass

    def _build_pending_view_finished(self) -> View:
        view = View(timeout=None)
        # Row 0: user mention
        uid_label = f"# <@{self.uid}>" if self.uid is not None else '#'
        view.add_item(Button(label=uid_label, style=discord.ButtonStyle.gray, disabled=True, row=0))
        # Row 1: separator
        view.add_item(Button(label='────────────────', style=discord.ButtonStyle.gray, disabled=True, row=1))

        # Row 2: Part 2 finished state
        view.add_item(Button(label='الكاش 💰', style=discord.ButtonStyle.gray, disabled=True, row=2))
        paid_btn = Button(label='استلمت الكاش', style=discord.ButtonStyle.green, custom_id='pending_paid', row=2)
        async def _paid_on_click(interaction: Interaction):
            try:
                from cogs.views import Money  # local import to avoid circular
                await interaction.response.send_modal(Money(self.guild_id, self.parent_message, self.uid, acc=self.acc))
            except Exception:
                pass
        paid_btn.callback = _paid_on_click
        view.add_item(paid_btn)
        # Row 3: Part 3 compressed
        acc_text = (str(self.acc) if self.acc is not None else '').splitlines()
        part3_line1 = acc_text[0][:80] if acc_text else '\u200b'
        part3_line2 = acc_text[1][:80] if len(acc_text) > 1 else None
        view.add_item(Button(label=part3_line1, style=discord.ButtonStyle.gray, disabled=True, row=3))
        if part3_line2:
            view.add_item(Button(label=part3_line2, style=discord.ButtonStyle.gray, disabled=True, row=3))

        # Row 4: Part 4 unchanged
        view.add_item(Button(label='لو اتبند', style=discord.ButtonStyle.gray, disabled=True, row=4))
        view.add_item(Button(label='اتبند', style=discord.ButtonStyle.red, custom_id='pending_banned', row=4))
        return view

class SingularityBo7(Modal):
    def __init__(self, guild_id, parent_message=None, original_content: str = "", uid: int | None = None, acc: str | None = None ,camo_type:str | None = None):
        super().__init__(title='Account Details')
        self.guild_id = guild_id
        self.parent_message = parent_message
        self.original_content = original_content
        self.uid = uid
        self.acc = acc

        self.level = TextInput(label="Level", style=TextStyle.short, placeholder="حط لفل الاكونت", required=True)
        self.add_item(self.level)

        self.prestige = TextInput(label='Prestige',style = TextStyle.short, placeholder="حط برستيج الاكونت",required=True)
        self.add_item(self.prestige)
    async def on_submit(self, interaction: Interaction):
        try:
            level = int(self.level.value)
            prestige = int(self.prestige.value)
        except (TypeError, ValueError):
            return await interaction.response.send_message('Level & Prestige should be numbers')
        bo7_weapons = [
    # Assault Rifles (6)
    "M15 Mod 0",
    "AK-27",
    "MXR-17",
    "X9 Maverick",
    "DS20 Mirage",
    "Peacekeeper MK1",

    # Submachine Guns - SMGs (6)
    "Ryden 45K",
    "RK-9",
    "Razor 9mm",
    "Dravec 45",
    "Carbon 57",
    "MPC-25",

    # Shotguns (3)
    "M10 Breacher",
    "Echo 12",
    "Akita",

    # Light Machine Guns - LMGs (2)
    "MK.78",
    "XM325",

    # Marksman Rifles (3)
    "M8A1",
    "Warden 308",
    "M34 Novaline",

    # Sniper Rifles (3)
    "VS Recon",
    "Shadow SK",
    "XR-3 Ion",

    # Pistols (3)
    "Jäger 45",
    "Velox 5.7",
    "Coda 9",

    # Launchers (2)
    "AAROW 109",
    "A.R.C. M1",

    # Melee Weapons (2)
    "Knife",
    "Flatline Mk.II"
]
        acc_content_parts = []
        # Include original account content if it exists
        if self.acc:
            acc_content_parts.append("")
            acc_content_parts.append(str(self.acc)+'\n')
        acc_content_parts.append(f"Level: {level}")
        acc_content_parts.append(f"Prestige: {prestige}")
        # acc_content_parts.append(f"Rank: {'RFR' if rank == 'rfr' else 'NoRFR'}")
        acc_content_parts.append(f"Maxed Weapons: None")
        acc_content_parts.append(f"Gold camos: None")
        acc_content_parts.append(f"Archlight camos: None")
        acc_content_parts.append(f"Singularity camos: {bo7_weapons}")
        
        acc_content = "\n".join(acc_content_parts)

        guild = interaction.guild
        account_name = f"bo7-{level}-{len(bo7_weapons)}-singu"

        if self.parent_message is not None:
            try:
                from cogs.views import MarkSoldLayout
                updated_view = MarkSoldLayout(self.guild_id, self.uid, acc=acc_content)
                await self.parent_message.edit(view=updated_view)
            except Exception as e:
                print(f"Error updating message view: {e}")

        if self.parent_message is not None and guild is not None:
            sale_category = discord.utils.get(guild.categories, name="For Sale 🏷️")
            if sale_category is None:
                sale_category = await guild.create_category("For Sale 🏷️")
            try:
                await self.parent_message.channel.edit(category=sale_category, name=f"🏷️{account_name}")
            except Exception:
                pass

        try:
            await interaction.response.send_message("تم حفظ التفاصيل ✅", ephemeral=True)
        except Exception:
            pass

class Ow2Roles(Select):
    def __init__(self):
        self.roles = [
            SelectOption(label='DPS',value='dps',emoji=EMOJIS['damage']),
            SelectOption(label='Tank',value='tank',emoji=EMOJIS['tank']),  
            SelectOption(label='Support',value='sup',emoji=EMOJIS['support']),
        ]
        super().__init__(
            placeholder='select how many roles....',
            min_values=1,
            max_values=3,
            options=self.roles,
            required=False,
            custom_id='role_selector'
        )
    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(self.values[0])

class Ow2Rank(Select):
    def __init__(self):
        self.rank = [
            SelectOption(label='Bronze',value='Bronze',emoji=EMOJIS['ow2bronze']),
            SelectOption(label='Silver',value='Silver',emoji=EMOJIS['ow2silver']),
            SelectOption(label='Gold',value='Gold',emoji=EMOJIS['ow2gold']),
            SelectOption(label='Platinum',value='Platinum',emoji=EMOJIS['ow2plat']),
            SelectOption(label='Diamond',value='Diamond',emoji=EMOJIS['ow2dia']),
            SelectOption(label='Master',value='Master',emoji=EMOJIS['ow2master']),
            SelectOption(label='Grand Master',value='Grand Master',emoji=EMOJIS['ow2gm']),
            SelectOption(label='Champion',value='Champion',emoji=EMOJIS['ow2champ'])
        ]
        super().__init__(
            placeholder='select rank..',
            max_values=1,
            min_values=1,
            options=self.rank,
            required=False,
            custom_id='rank_selector'
        )
    async def callback(self,interaction: Interaction):
        await interaction.response.send_message(self.values[0])

class RFR(Select):
    def __init__(self):
        options = [
            SelectOption(label='RFR (Ready for Rank only)',value='t',emoji='✅'),
            SelectOption(label='NoRFR (not Ready for Rank only)',value ='f',emoji='❌')
        ]
        super().__init__(
            placeholder='rfr ?',
            max_values=1,
            min_values=1,
            options=options,
            required=False,
            custom_id='rfr_selector',
        )
    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(self.values[0])

class OW2(Modal):
    def __init__(self, guild_id, parent_message=None, original_content: str = "", uid: int | None = None, acc: str | None = None):
        super().__init__(title="Account Details")
        self.guild_id = guild_id
        self.parent_message = parent_message
        self.original_content = original_content
        self.uid = uid
        self.acc = acc

        self.rfr = Label(text='Rank Ready',component=RFR())

        self.roles = Label(text='Roles',component=Ow2Roles())

        self.rank = Label(text='Rank',component=Ow2Rank())

        self.add_item(self.rfr)
        self.add_item(self.roles)
        self.add_item(self.rank)

    async def on_submit(self, interaction: Interaction):
        roles = self.roles.component.values if self.roles.component.values else None
        rank = self.rank.component.values[0] if self.rank.component.values else None
        rfr = True if self.rfr.component.values[0] == 't' or roles or rank else False
        guild = interaction.guild
        
        # Build account content string from modal data
        acc_content_parts = []
        # Include original account content if it exists
        if self.acc:
            acc_content_parts.append("")
            acc_content_parts.append(str(self.acc)+'\n')
        acc_content_parts.append(f"Roles: {roles}")
        acc_content_parts.append(f"Rank: {rank}")
        acc_content_parts.append(f"RFR: {'RFR' if rfr else 'NoRFR'}")
        
        acc_content = "\n".join(acc_content_parts)
        
        # Update the original pending message to MarkSoldLayout with account content
        if self.parent_message is not None:
            try:
                from cogs.views import MarkSoldLayout  # local import to avoid circular
                updated_view = MarkSoldLayout(self.guild_id, self.uid, acc=acc_content)
                await self.parent_message.edit(view=updated_view)
            except Exception as e:
                print(f"Error updating message view: {e}")
        
        # Move current channel to For Sale with the edited message
        if self.parent_message is not None:
            sale_category = discord.utils.get(guild.categories, name="For Sale 🏷️")
            if sale_category is None:
                sale_category = await guild.create_category("For Sale 🏷️")
            try:
                account_name = f'ow2-{len(roles)}-role-{rank}-{'RFR' if rfr else 'noRFR'}'
                await self.parent_message.channel.edit(category=sale_category, name=f"🏷️{account_name}")
            except Exception:
                pass

            # Acknowledge submission ephemerally
            try:
                await interaction.response.send_message("تم حفظ التفاصيل ✅", ephemeral=True)
            except Exception:
                pass
        else:
            # If no parent_message, create new channel (original behavior)
            category = discord.utils.get(guild.categories, name="For Sale 🏷️")
            if category is None:
                category = await guild.create_category("For Sale 🏷️")

            account_name = f'ow2-{roles}-role-{rank}-{'RFR' if rfr else 'noRFR'}'

            user = interaction.user
            everyone = guild.default_role
            overwrites = {
                everyone: discord.PermissionOverwrite(view_channel=False),
                user: discord.PermissionOverwrite(view_channel=True,send_messages=True)
            }
            channel = await category.create_text_channel(f'🏷️{account_name}',overwrites=overwrites)
            confirm_embed = Embed(
                title='✅ Channel created successfully',
                description=f'Your channel\n# {channel.mention}',
                color=0x038c07
            )
            await interaction.response.send_message(embed=confirm_embed,ephemeral=True)
            from cogs.views import MarkSoldLayout  # local import to avoid circular
            msg = await channel.send(view=MarkSoldLayout(self.guild_id, interaction.user.id, acc=acc_content))
            await msg.pin()

class RivalsRank(Select):
    def __init__(self):
        options = [
            SelectOption(label='Bronze',value='Bronze',emoji=EMOJIS['img_rank_dan_01']),
            SelectOption(label='Silver',value='Silver',emoji=EMOJIS['img_rank_dan_02']),
            SelectOption(label='Gold',value='Gold',emoji=EMOJIS['img_rank_dan_03']),
            SelectOption(label='Platinum',value='Platinum',emoji=EMOJIS['img_rank_dan_04']),
            SelectOption(label='Diamond',value='Diamond',emoji=EMOJIS['img_rank_dan_05']),
            SelectOption(label='Grand Master',value='Grand Master',emoji=EMOJIS['img_rank_dan_06']),
            SelectOption(label='Celestial',value='Celestial',emoji=EMOJIS['img_rank_dan_07']),
            SelectOption(label='Eternity',value='Eternity',emoji=EMOJIS['img_rank_dan_08']),
            SelectOption(label='One Above All',value='One Above All',emoji=EMOJIS['img_rank_dan_09'])
        ]
        super().__init__(
            placeholder='اختار رانك الاكونت',
            max_values=1,
            min_values=1,
            options=options,
            required=False,
            custom_id='rivals_rank_selector',
        )
    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(self.values[0])

class Rivals(Modal):
    def __init__(self, guild_id, parent_message=None, original_content: str = "", uid: int | None = None, acc: str | None = None):
        super().__init__(title="Account Details")
        self.guild_id = guild_id
        self.parent_message = parent_message
        self.original_content = original_content
        self.uid = uid
        self.acc = acc

        self.level_input = TextInput(label="Level", style=TextStyle.short, placeholder="لفل الاكونت بتاعك", required=True)
        self.add_item(self.level_input)

        self.rank_input = Label(text='Rank', component=RivalsRank())
        self.add_item(self.rank_input)

    async def on_submit(self, interaction: Interaction):
        # Get level value
        try:
            level = int(self.level_input.value)
        except:
            return await interaction.response.send_message('حط لفل الاكونت كا رقم فقط')
        # Get rank value (handle empty selection)
        rank = self.rank_input.component.values[0] if self.rank_input.component.values else None
        
        guild = interaction.guild
        
        # Build account content string from modal data
        acc_content_parts = []
        
        # Include original account content if it exists
        if self.acc:
            acc_content_parts.append("")
            acc_content_parts.append(str(self.acc)+'\n')
        
        acc_content_parts.append(f"Level: {level}")
        acc_content_parts.append(f"Rank: {rank}")
        
        acc_content = "\n".join(acc_content_parts)
        
        # Update the original pending message to MarkSoldLayout with account content
        if self.parent_message is not None:
            try:
                from cogs.views import MarkSoldLayout  # local import to avoid circular
                updated_view = MarkSoldLayout(self.guild_id, self.uid, acc=acc_content)
                await self.parent_message.edit(view=updated_view)
            except Exception as e:
                print(f"Error updating message view: {e}")
        
        # Move current channel to For Sale with the edited message
        if self.parent_message is not None:
            sale_category = discord.utils.get(guild.categories, name="For Sale 🏷️")
            if sale_category is None:
                sale_category = await guild.create_category("For Sale 🏷️")
            try:
                account_name = f'rivals-{level}'
                if rank:
                    account_name = f'rivals-{level}-{rank.lower()}'
                await self.parent_message.channel.edit(category=sale_category, name=f"🏷️{account_name}")
            except Exception:
                pass

            # Acknowledge submission ephemerally
            try:
                await interaction.response.send_message("تم حفظ التفاصيل ✅", ephemeral=True)
            except Exception:
                pass
        else:
            # If no parent_message, create new channel (original behavior)
            category = discord.utils.get(guild.categories, name="For Sale 🏷️")
            if category is None:
                category = await guild.create_category("For Sale 🏷️")

            account_name = f'rivals-{level}'
            if rank:
                account_name = f'rivals-{level}-{rank.lower()}'

            user = interaction.user
            everyone = guild.default_role
            overwrites = {
                everyone: discord.PermissionOverwrite(view_channel=False),
                user: discord.PermissionOverwrite(view_channel=True,send_messages=True)
            }
            channel = await category.create_text_channel(f'🏷️{account_name}',overwrites=overwrites)
            confirm_embed = Embed(
                title='✅ Channel created successfully',
                description=f'Your channel\n# {channel.mention}',
                color=0x038c07
            )
            await interaction.response.send_message(embed=confirm_embed,ephemeral=True)
            from cogs.views import MarkSoldLayout  # local import to avoid circular
            msg = await channel.send(view=MarkSoldLayout(self.guild_id, interaction.user.id, acc=acc_content))
            await msg.pin()
# === BATTLEFIELD 6 WEAPON SELECTORS ===
class BF6WeaponSelect1(Select):
    def __init__(self):
        options = [
            # Assault Rifles (6)
            SelectOption(label='AM 16', value='AM 16'),
            SelectOption(label='FR-27', value='FR-27'),
            SelectOption(label='MH-9K', value='MH-9K'),
            SelectOption(label='TSR-50', value='TSR-50'),
            SelectOption(label='SX-47', value='SX-47'),
            SelectOption(label='CR-56', value='CR-56'),
            # Submachine Guns (5)
            SelectOption(label='PXC-11', value='PXC-11'),
            SelectOption(label='KX-9', value='KX-9'),
            SelectOption(label='SA-87', value='SA-87'),
            SelectOption(label='VMG-45', value='VMG-45'),
            SelectOption(label='UL-360', value='UL-360'),
            # Shotguns (3)
            SelectOption(label='Trench 12', value='Trench 12'),
            SelectOption(label='Auto 870', value='Auto 870'),
            SelectOption(label='SPAS-15', value='SPAS-15'),
        ]
        super().__init__(
            min_values=0,
            max_values=len(options),
            options=options,
            required=False,
            placeholder='Choose BF6 weapons (AR, SMG, Shotguns)...'
        )

    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(self.values[0])

class BF6WeaponSelect2(Select):
    def __init__(self):
        options = [
            # Light Machine Guns (3)
            SelectOption(label='LAMG-240', value='LAMG-240'),
            SelectOption(label='PKP Pecheneg', value='PKP Pecheneg'),
            SelectOption(label='M60E4', value='M60E4'),
            # Marksman Rifles (3)
            SelectOption(label='SVK', value='SVK'),
            SelectOption(label='M417', value='M417'),
            SelectOption(label='CS5', value='CS5'),
            # Sniper Rifles (3)
            SelectOption(label='L96A1', value='L96A1'),
            SelectOption(label='M200 Intervention', value='M200 Intervention'),
            SelectOption(label='GOL Magnum', value='GOL Magnum'),
            # Pistols (3)
            SelectOption(label='MP-443 Grach', value='MP-443 Grach'),
            SelectOption(label='M1911', value='M1911'),
            SelectOption(label='Desert Eagle', value='Desert Eagle'),
            # Launchers (2)
            SelectOption(label='FGM-148 Javelin', value='FGM-148 Javelin'),
            SelectOption(label='RPG-7V2', value='RPG-7V2'),
            # Battle Pickups / Special (2)
            SelectOption(label='XM25 Airburst', value='XM25 Airburst'),
            SelectOption(label='RAWR Flamethrower', value='RAWR Flamethrower'),
        ]
        super().__init__(
            min_values=0,
            max_values=len(options),
            options=options,
            required=False,
            placeholder='Choose BF6 weapons (LMG, Snipers, Special)...'
        )

    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(self.values[0])

# === BATTLEFIELD 6 MODAL ===
class BF6(Modal):
    def __init__(self, guild_id, parent_message=None, original_content: str = "", uid: int | None = None, acc: str | None = None):
        super().__init__(title="Battlefield 6 Account Details")
        self.guild_id = guild_id
        self.parent_message = parent_message
        self.original_content = original_content
        self.uid = uid
        self.acc = acc
        
        # Level input
        self.level_input = TextInput(label="Level", style=TextStyle.short, placeholder="Enter your BF6 level", required=True)
        self.add_item(self.level_input)
        
        # UNLOCKED WEAPONS - Split into 2 selectors
        self.unlocked_select1 = Label(text='Unlocked Weapons (AR, SMG, Shotguns)...', component=BF6WeaponSelect1())
        self.add_item(self.unlocked_select1)
        
        self.unlocked_select2 = Label(text='Unlocked Weapons (LMG, Snipers, Special)...', component=BF6WeaponSelect2())
        self.add_item(self.unlocked_select2)
        
        # ELITE WEAPONS - Split into 2 selectors
        self.elite_select1 = Label(text='Elite Weapons (AR, SMG, Shotguns)...', component=BF6WeaponSelect1())
        self.add_item(self.elite_select1)
        
        self.elite_select2 = Label(text='Elite Weapons (LMG, Snipers, Special)...', component=BF6WeaponSelect2())
        self.add_item(self.elite_select2)
        
    async def on_submit(self, interaction: Interaction):
        # Get input values
        level = self.level_input.value
        
        # Get UNLOCKED selected weapons from BOTH selectors
        unlocked_weapons1 = self.unlocked_select1.component.values if self.unlocked_select1.component.values else []
        unlocked_weapons2 = self.unlocked_select2.component.values if self.unlocked_select2.component.values else []
        unlocked_weapons = unlocked_weapons1 + unlocked_weapons2
        
        # Get ELITE selected weapons from BOTH selectors
        elite_weapons1 = self.elite_select1.component.values if self.elite_select1.component.values else []
        elite_weapons2 = self.elite_select2.component.values if self.elite_select2.component.values else []
        elite_weapons = elite_weapons1 + elite_weapons2
        
        guild = interaction.guild
        
        # Build account content string
        acc_content_parts = []
        if self.acc:
            acc_content_parts.append("")
            acc_content_parts.append(str(self.acc)+'\n')
        
        acc_content_parts.append(f"Level: {level}")
        acc_content_parts.append(f"Unlocked Weapons: {unlocked_weapons if unlocked_weapons != [] else None}")
        acc_content_parts.append(f"Elite Weapons: {elite_weapons if elite_weapons != [] else None}")
        
        acc_content = "\n".join(acc_content_parts)
        
        # Update the original pending message to MarkSoldLayout
        if self.parent_message is not None:
            try:
                from cogs.views import MarkSoldLayout
                updated_view = MarkSoldLayout(self.guild_id, self.uid, acc=acc_content)
                await self.parent_message.edit(view=updated_view)
            except Exception as e:
                print(f"Error updating BF6 message view: {e}")
        
        # Move current channel to For Sale
        if self.parent_message is not None:
            sale_category = discord.utils.get(guild.categories, name="For Sale 🏷️")
            if sale_category is None:
                sale_category = await guild.create_category("For Sale 🏷️")
            try:
                account_name = f'bf6-{level}-{len(unlocked_weapons)}unl-{len(elite_weapons)}elite'
                await self.parent_message.channel.edit(category=sale_category, name=f"🏷️{account_name}")
            except Exception:
                pass

            # Acknowledge submission
            try:
                await interaction.response.send_message("تم حفظ تفاصيل باتلفيلد 6 ✅", ephemeral=True)
            except Exception:
                pass

# === WARZONE RFR SELECTOR ===
class WarzoneRFR(Select):
    def __init__(self):
        options = [
            SelectOption(label='RFR (Ready for Rank)', value='rfr', emoji='✅'),
            SelectOption(label='NoRFR (Not Ready for Rank)', value='norfr', emoji='❌'),
        ]
        super().__init__(
            placeholder='Is the account ready for ranked?',
            min_values=1,
            max_values=1,
            options=options,
            custom_id='warzone_rfr_selector',
        )
    
    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(self.values[0])

# === WARZONE MODAL ===
class Warzone(Modal):
    def __init__(self, guild_id, parent_message=None, original_content: str = "", uid: int | None = None, acc: str | None = None):
        super().__init__(title="Warzone Account Details")
        self.guild_id = guild_id
        self.parent_message = parent_message
        self.original_content = original_content
        self.uid = uid
        self.acc = acc
        
        # Level input
        self.level_input = TextInput(label="Level", style=TextStyle.short, placeholder="Enter your Warzone level", required=True)
        self.add_item(self.level_input)
        
        # RFR selector (Ready for Rank)
        self.rfr_label = Label(text='Is the account Ready for Rank?', component=WarzoneRFR())
        self.add_item(self.rfr_label)
        
        # MAXED WEAPONS - Split into 2 selectors (reusing BO7 WeaponSelect classes)
        self.maxed_select1 = Label(text='Maxed Weapons (AR, SMG, Shotguns)...', component=WeaponSelect1())
        self.add_item(self.maxed_select1)
        
        self.maxed_select2 = Label(text='Maxed Weapons (LMG, Marksman, Snipers)...', component=WeaponSelect2())
        self.add_item(self.maxed_select2)
        
    async def on_submit(self, interaction: Interaction):
        # Get input values
        level = self.level_input.value
        rfr_value = self.rfr_label.component.values[0] if self.rfr_label.component.values else None
        
        # Get MAXED selected weapons from BOTH selectors
        maxed_weapons1 = self.maxed_select1.component.values if self.maxed_select1.component.values else []
        maxed_weapons2 = self.maxed_select2.component.values if self.maxed_select2.component.values else []
        maxed_weapons = maxed_weapons1 + maxed_weapons2
        
        guild = interaction.guild
        
        # Build account content string
        acc_content_parts = []
        if self.acc:
            acc_content_parts.append("")
            acc_content_parts.append(str(self.acc)+'\n')
        
        acc_content_parts.append(f"Level: {level}")
        acc_content_parts.append(f"Ready for Rank: {'RFR' if rfr_value == 'rfr' else 'NoRFR'}")
        acc_content_parts.append(f"Maxed Weapons: {maxed_weapons if maxed_weapons != [] else None}")
        
        acc_content = "\n".join(acc_content_parts)
        
        # Update the original pending message to MarkSoldLayout
        if self.parent_message is not None:
            try:
                from cogs.views import MarkSoldLayout
                updated_view = MarkSoldLayout(self.guild_id, self.uid, acc=acc_content)
                await self.parent_message.edit(view=updated_view)
            except Exception as e:
                print(f"Error updating Warzone message view: {e}")
        
        # Move current channel to For Sale
        if self.parent_message is not None:
            sale_category = discord.utils.get(guild.categories, name="For Sale 🏷️")
            if sale_category is None:
                sale_category = await guild.create_category("For Sale 🏷️")
            try:
                rfr_status = 'rfr' if rfr_value == 'rfr' else 'norfr'
                account_name = f'wz-{level}-{rfr_status}-{len(maxed_weapons)}max'
                await self.parent_message.channel.edit(category=sale_category, name=f"🏷️{account_name}")
            except Exception:
                pass

            # Acknowledge submission
            try:
                await interaction.response.send_message("تم حفظ تفاصيل وارزون ✅", ephemeral=True)
            except Exception:
                pass

async def setup(client):
    pass