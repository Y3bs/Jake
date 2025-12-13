import enum
import discord 
from discord import Embed,Activity,Game,ActivityType,Message
from itertools import cycle 
import asyncio
import re

EMOJIS = {
    # games
    'rivals': '<:MarvelRivals:1437768326733627494>',
    'bo7': '<:Warzone:1437768013981024348>',
    'valorant': '<:valorant:1437768016841412668>',
    'ow2':'<:ow2:1437768015285452921>',
    'battlefield6':'<:bf6:1437768012391252108>',
    'wz': '<:wz:1447992598253010944>',
    # platform
    'steam':'<:steam:1437767650032877608>',
    'activision':'<:activision:1437767648476921916>',
    'epic':'<:epic:1437767647138676757>',
    'ea':'<:ea:1437767645892972684>',
    'battlenet':'<:battlenet:1437769329885184040>',
    # wallets
    'vodafone': '<:Vodafone:1437769331076501607>',
    'instapay': '<:Instapay:1437769332506497147>',
    'visa': '<:Visa:1437769333790212168>',
    # ow2 ranks
    'ow2bronze': '<:ow2bronze:1438254342561075221>',
    'ow2silver': '<:ow2silver:1438254344242987150>',
    'ow2gold': '<:ow2gold:1438254346382086285>',
    'ow2plat': '<:ow2plat:1438254348453937152>',
    'ow2dia': '<:ow2dia:1438254350257488106>',
    'ow2master': '<:ow2master:1438254352174416025>',
    'ow2gm': '<:ow2gm:1438254354414043318>',
    'ow2champ': '<:ow2champ:1438254356741882017>',
    # bo7 (AR)
    'm15': '<:m15:1439201943766564946>',
    'ak27': '<:ak27:1439201940931219586>',
    'mxr17': '<:mxr17:1439201938053926992>',
    'x9': '<:x9:1439201935268773958>',
    'ds20': '<:ds20:1439201932538548245>',
    'mk1': '<:mk1:1439201930034417734>',
    # bo7 (OP)
    '5050operator': '<:5050operator:1439307395254849566>',
    'andersonoperator': '<:andersonoperator:1439307397473636453>',
    'carveroperator': '<:carveroperator:1439307399558201436>',
    'dempseyoperator1': '<:dempseyoperator1:1439307401546174484>',
    'falkneroperator': '<:falkneroperator:1439307403182080253>',
    'greyoperator': '<:greyoperator:1439307405375701013>',
    'grimmoperator': '<:grimmoperator:1439307407409942672>',
    'harperoperator': '<:harperoperator:1439307409876058114>',
    'juradooperator': '<:juradooperator:1439307411331485866>',
    'kaganoperator': '<:kaganoperator:1439307412946288784>',
    'karmaoperator': '<:karmaoperator:1439307414804365545>',
    'masonoperator': '<::1439307416574361842>',
    'mayaoperator': '<:mayaoperator:1439307418529038618>',
    'nikolaioperator1': '<::1439307420919660654>',
    'razoroperator': '<:razoroperator:1439307424392675458>',
    'reaperewr3operator': '<:reaperewr3operator:1439307427471294769>',
    'richtofenoperator1': '<:richtofenoperator1:1439307429383897219>',
    'samuelsoperator': '<:samuelsoperator:1439307445263532218>',
    'takeooperator1': '<:takeooperator1:1439307457179553905>',
    'teddoperator': '<:teddoperator:1439307458823720961>',
    'vermaakoperator': '<:vermaakoperator:1439307461348688023>',
    'weaveroperator': '<:weaveroperator:1439307463173214348>',
    'weilinoperator':'<:weilinoperator:1439307465291202672>',
    'zaverioperator': '<:zaverioperator:1439307466633380031>'
}

async def move_channel(channel,category_name,emoji,color,title,desc):
    guild = channel.guild
    category = discord.utils.get(guild.categories,name=category_name)
    if category is None:
        category = await guild.create_category(category_name)
    await channel.edit(name=f'{emoji}{channel.name[1:]}',category=category)
    return Embed(title=title,description=desc,color=color)

statuses = cycle([
    Game("💸 Selling accounts"),
    Activity(type=ActivityType.listening, name="customers"),
    Activity(type=ActivityType.watching, name="📦 Orders come & go"),
    Game("⛔ Handling bans"),
    Activity(type=ActivityType.watching, name="earnings grow 💰"),
    Activity(type=ActivityType.listening,name='Auto saving files 🗃️'),
    Game("v4.0")
])

async def cycle_status(client, interval=60):
    """Loop through statuses every X seconds (default 60)."""
    while True:
        await client.change_presence(activity=next(statuses))
        await asyncio.sleep(interval)

def get_user_id(msg: Message):
    id = re.search(r"<@!?(\d+)>", msg.content)
    if id:
        return int(id.group(1))
    return None

def check_wallet_type(select:str,type: str):
    if select == 'vodafone':
        num = '0125'
        if not type.startswith('01') or type[2] not in num or not type[3:].isdigit():
            return False
    if select == 'instapay':
        if not type.endswith('@instapay'):
            return False
    if select == 'visa':
        if not type.isdigit():
            return False
        total = 0
        reverse = type[::-1]

        for i,digit in enumerate(reverse):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -=9
            total += n
        return total % 10 == 0
    return True

def setup(client):
    pass