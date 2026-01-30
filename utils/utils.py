import discord 
from discord import Activity,Game,ActivityType,Message,Interaction
from discord.ui import LayoutView,Container,TextDisplay,Separator
from itertools import cycle 
import asyncio, re
import pandas as pd
from datetime import datetime

from pandas.core.arrays import categorical
import utils.database as db

EMOJIS = {
    # games
    'rivals': '<:MarvelRivals:1437768326733627494>',
    'bo7': '<:bo7:1450430203204472957>',
    'valorant': '<:valorant:1437768016841412668>',
    'ow2':'<:ow2:1437768015285452921>',
    'battlefield6':'<:bf6:1437768012391252108>',
    'wz': '<:wz:1447992598253010944>',
    'arcraiders': '<:arcraiders:1465992591328677981>',
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
    'zaverioperator': '<:zaverioperator:1439307466633380031>',
    # Arc Items
    'items': '<:items:1466001914448711933>',
    'coins': '<:coins:1466004373053378611>'
}

async def move_channel(channel,category_name,emoji):
    guild = channel.guild
    category = discord.utils.get(guild.categories,name=category_name)
    if category is None:
        category = await guild.create_category(category_name)
    await channel.edit(name=f'{emoji}{channel.name[1:]}',category=category)

statuses = cycle([
    Game("💸 Selling accounts"),
    Activity(type=ActivityType.listening, name="Customers 🛍️"),
    Activity(type=ActivityType.watching, name="📦 Orders come & go"),
    Game("⛔ Handling bans"),
    Activity(type=ActivityType.watching, name="Earnings grow 💰"),
    Activity(type=ActivityType.listening,name='Auto saving files 🗃️'),
    Game("v4.5")
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

def get_current_month_stats(user_id):
    """
    Get current month statistics for a user without visualization.
    
    Args:
        user_id: Discord user ID
        
    Returns:
        dict: Current month statistics or error message
    """
    try:
        # Get user stats from database
        user_stats = db.find_player(user_id)
        
        # Handle not registered users
        if not user_stats:
            return {
                'error': True,
                'message': "أنت غير مسجل في قاعدة البيانات. استخدم `/register` أولاً!",
                'registered': False
            }
        
        # Handle no history
        if not user_stats.get('history'):
            return {
                'error': True,
                'message': "ليس لديك أي تاريخ للحسابات بعد!\nابدأ ببيع الحسابات لترى إحصائياتك هنا.",
                'no_history': True
            }
        
        # Get current month and year
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        
        # Filter history for current month
        current_month_history = []
        for record in user_stats.get('history', []):
            try:
                record_time = pd.to_datetime(record.get('time'))
                if record_time.month == current_month and record_time.year == current_year:
                    current_month_history.append(record)
            except:
                continue
        
        # Calculate current month stats
        sold_current_month = 0
        banned_current_month = 0
        earnings_current_month = 0
        
        for record in current_month_history:
            action = record.get('action', '').lower()
            price = record.get('price', 0)
            
            if action == 'sold':
                sold_current_month += 1
                earnings_current_month += price
            elif action == 'banned':
                banned_current_month += 1
        
        # Calculate success rate for current month
        total_current_month = sold_current_month + banned_current_month
        success_rate_current_month = 0
        if total_current_month > 0:
            success_rate_current_month = (sold_current_month / total_current_month) * 100
        
        # Calculate average sale for current month
        avg_sale_current_month = 0
        if sold_current_month > 0:
            avg_sale_current_month = earnings_current_month / sold_current_month
        
        # Get total number of wallets
        wallets_count = len(user_stats.get('wallets', {}))
        
        return {
            'error': False,
            'sold_current_month': sold_current_month,
            'banned_current_month': banned_current_month,
            'earnings_current_month': earnings_current_month,
            'success_rate_current_month': success_rate_current_month,
            'avg_sale_current_month': avg_sale_current_month,
            'wallets_count': wallets_count,
            'total_current_month': total_current_month,
            'month_name': now.strftime("%B"),  # Current month name
            'year': current_year
        }
        
    except Exception as e:
        return {
            'error': True,
            'message': f"فشل في إنشاء الإحصائيات: {str(e)}"
        }


def format_monthly_stats_message(stats_data, user_mention):
    """
    Format monthly statistics into a display message.
    
    Args:
        stats_data: Dictionary returned by get_current_month_stats
        user_mention: Discord user mention string
        
    Returns:
        str: Formatted message
    """
    if stats_data.get('error'):
        return stats_data.get('message', 'حدث خطأ في جلب الإحصائيات.')
    
    month_name = stats_data.get('month_name', '')
    year = stats_data.get('year', '')
    
    message = f"## 📊 إحصائيات {month_name} {year}\n"
    message += f"**للمستخدم:** {user_mention}\n\n"
    
    # Current month stats
    message += "**📈 إحصائيات الشهر الحالي:**\n"
    message += f"• **💸 مباع هذا الشهر:** {stats_data['sold_current_month']} حساب\n"
    message += f"• **⛔ محظور هذا الشهر:** {stats_data['banned_current_month']} حساب\n"
    message += f"• **📦 معدل النجاح:** {stats_data['success_rate_current_month']:.1f}%\n"
    message += f"• **💰 أرباح هذا الشهر:** {stats_data['earnings_current_month']} ج.م\n"
    message += f"• **⚖️ متوسط سعر البيع:** {stats_data['avg_sale_current_month']:.1f} ج.م\n"
    message += f"• **💳 محافظ مسجلة:** {stats_data['wallets_count']}\n"
    
    return message

def create_banned_callback(view_instance,game):
    async def _banned_on_click(interaction: Interaction):
        channel = interaction.channel
        # Edit message with LayoutView: Part 1 = mention, Part 2 = desc
        banned_view = LayoutView()
        banned_container = Container()
        # Part 1: game name
        game_display_name = get_game_display_name(game)
        game_emoji = get_game_emoji(game)
        game_title = TextDisplay(f'## {game_emoji} {game_display_name}')
        banned_container.add_item(game_title)
        banned_container.add_item(Separator())
        # Part 2: account type
        banned_container.add_item(TextDisplay(f"🏷️ **Type**"))
        banned_container.add_item(TextDisplay(f"```{channel.name[1:]}```"))
        banned_container.add_item(Separator())

        banned_view.add_item(banned_container)

        category = discord.utils.get(interaction.guild.categories,name='Banned ⛔')
        if category is None:
            category = await interaction.guild.create_category('Banned ⛔')

        target = f'{game}-banned'
        exist = None

        for ch in category.channels:
            if target in ch.name:
                exist = ch
                break
        
        if exist:
            await exist.send(view=banned_view)
        else:
            ch = await category.create_text_channel(f'⛔{game}-banned')
            await ch.send(view=banned_view)

        await interaction.channel.delete()
        # db.log_account(view_instance.uid, 'banned')
        db.log_rec(view_instance.uid,'banned',game)
        await interaction.response.defer()
    return _banned_on_click

def extract_user_id_from_text(text):
    """Extract user ID from mention text like '# <@123456789>'"""
    try:
        if not text:
            return None
        match = re.search(r'<@(\d+)>', str(text))
        return int(match.group(1)) if match else None
    except:
        return None 

async def copy_content(interaction: Interaction,txt):
    await interaction.response.send_message(txt,ephemeral=True)

def get_game_display_name(game):
    """Convert game key to display name"""
    game_names = {
        'bo7': 'Black Ops 7',
        'ow2': 'Overwatch 2',
        'rivals': 'Marvel Rivals',
        'battlefield6': 'Battlefield 6',
        'warzone': 'Warzone',
        'valorant': 'VALORANT',
    }
    return game_names.get(game, game.upper() if game else None)

def get_game_emoji(game):
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

def setup(client):
    pass