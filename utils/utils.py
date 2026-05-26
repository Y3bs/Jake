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
    'ewallet': '<:ewallet:1508893580150833223>',
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
    if select == 'e-wallet':
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

def get_current_month_stats(user_id, game_filter="all"):
    """
    Get current month statistics for a user, optionally filtered by game.
    
    Args:
        user_id: Discord user ID
        game_filter: "all" for all games, or specific game name like "bo7", "ow2", etc.
        
    Returns:
        dict: Current month statistics or error message
    """
    try:
        # First check if player is registered in players collection
        player_data = db.find_player(user_id)
        
        # Handle not registered users
        if not player_data:
            return {
                'error': True,
                'message': "أنت غير مسجل في قاعدة البيانات. استخدم `/register` أولاً!",
                'registered': False,
                'no_history': False,
                'game_filter': game_filter
            }
        
        # Get current month and year
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        
        # Get all records for this user
        try:
            player_records = db.get_player_records(user_id)
        except AttributeError:
            try:
                records_collection = db.records
                player_records = list(records_collection.find({'user_id': user_id}))
            except Exception as e:
                return {
                    'error': True,
                    'message': f"فشل في الوصول إلى سجلات اللاعب: {str(e)}",
                    'registered': True,
                    'no_history': False,
                    'game_filter': game_filter
                }
        
        # If no records found
        if not player_records:
            return {
                'error': True,
                'message': "ليس لديك أي سجلات للحسابات بعد!",
                'registered': True,
                'no_history': True,
                'game_filter': game_filter
            }
        
        # Filter records for current month AND optionally by game
        current_month_records = []
        for record in player_records:
            try:
                record_time = pd.to_datetime(record.get('timestamp') or record.get('time'))
                
                # Check if record is in current month/year
                time_match = record_time.month == current_month and record_time.year == current_year
                
                # Check game filter
                game_match = True
                if game_filter != "all":
                    record_game = record.get('game', '').lower()
                    game_filter_lower = game_filter.lower()
                    game_match = record_game == game_filter_lower
                
                if time_match and game_match:
                    current_month_records.append(record)
            except Exception:
                continue
        
        # If no records match the filter
        if not current_month_records:
            if game_filter == "all":
                return {
                    'error': True,
                    'message': f"ليس لديك أي سجلات في شهر {now.strftime('%B')}!",
                    'registered': True,
                    'no_history': True,
                    'month_name': now.strftime("%B"),
                    'year': current_year,
                    'game_filter': game_filter
                }
            else:
                game_display = get_game_display_name(game_filter) or game_filter
                return {
                    'error': True,
                    'message': f"ليس لديك أي سجلات للعبة {game_display} في شهر {now.strftime('%B')}!",
                    'registered': True,
                    'no_history': True,
                    'month_name': now.strftime("%B"),
                    'year': current_year,
                    'game_filter': game_filter
                }
        
        # Calculate current month stats
        sold_current_month = 0
        banned_current_month = 0
        earnings_current_month = 0
        games_handled = set()  # Track unique games in filtered records
        
        for record in current_month_records:
            action = record.get('action', '').lower()
            price = record.get('price', 0) or record.get('amount', 0)
            game = record.get('game', 'unknown')
            
            # Track unique games
            games_handled.add(game)
            
            if action == 'sold':
                sold_current_month += 1
                earnings_current_month += int(price) if price else 0
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
        
        # Get wallet count from player data
        wallets = player_data.get('wallets', {})
        wallets_count = 0
        for wallet_type in ['visa', 'e-wallet', 'instapay']:
            wallet_data = wallets.get(wallet_type, [])
            if isinstance(wallet_data, list):
                wallets_count += len(wallet_data)
            elif wallet_data:
                wallets_count += 1
        
        # Get filtered all-time stats for comparison
        total_sold_all_time = 0
        total_earnings_all_time = 0
        games_all_time = set()
        
        for record in player_records:
            action = record.get('action', '').lower()
            game = record.get('game', 'unknown')
            
            # Apply game filter for all-time stats too
            if game_filter != "all":
                record_game = record.get('game', '').lower()
                if record_game != game_filter.lower():
                    continue
            
            games_all_time.add(game)
            
            if action == 'sold':
                total_sold_all_time += 1
                total_earnings_all_time += int(record.get('price', 0) or record.get('amount', 0))
        
        return {
            'error': False,
            'sold_current_month': sold_current_month,
            'banned_current_month': banned_current_month,
            'earnings_current_month': earnings_current_month,
            'success_rate_current_month': success_rate_current_month,
            'avg_sale_current_month': avg_sale_current_month,
            'wallets_count': wallets_count,
            'total_current_month': total_current_month,
            'month_name': now.strftime("%B"),
            'year': current_year,
            'total_sold_all_time': total_sold_all_time,
            'total_earnings_all_time': total_earnings_all_time,
            'records_count': len(current_month_records),
            'game_filter': game_filter,
            'games_handled': list(games_handled),
            'games_all_time': list(games_all_time)
        }
        
    except Exception as e:
        return {
            'error': True,
            'message': f"فشل في إنشاء الإحصائيات: {str(e)}",
            'registered': True,
            'no_history': False,
            'game_filter': game_filter
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
        if stats_data.get('registered') == False:
            return "## ❌ التسجيل مطلوب\nأنت غير مسجل في قاعدة البيانات. استخدم `/register` أولاً!"
        elif stats_data.get('no_history'):
            month_name = stats_data.get('month_name', 'هذا الشهر')
            year = stats_data.get('year', '')
            game_filter = stats_data.get('game_filter', 'all')
            
            if game_filter == "all":
                return f"## 📭 لا توجد سجلات\nليس لديك أي سجلات للحسابات في {month_name} {year}!\nابدأ ببيع الحسابات لترى إحصائياتك هنا."
            else:
                game_display = get_game_display_name(game_filter) or game_filter
                return f"## 🎮 لا توجد سجلات للعبة\nليس لديك أي سجلات للعبة **{game_display}** في {month_name} {year}!"
        else:
            return f"## ❌ خطأ في الإحصائيات\n{stats_data.get('message', 'حدث خطأ غير معروف.')}"
    
    month_name = stats_data.get('month_name', '')
    year = stats_data.get('year', '')
    game_filter = stats_data.get('game_filter', 'all')
    
    # Create header based on filter
    if game_filter == "all":
        message = f"## 📊 إحصائيات {month_name} {year} - جميع الألعاب\n"
    else:
        game_display = get_game_display_name(game_filter) or game_filter
        game_emoji = get_game_emoji(game_filter)
        message = f"## {game_emoji} إحصائيات {month_name} {year} - {game_display}\n"
    
    message += f"**للمستخدم:** {user_mention}\n\n"
    
    # Current month stats
    if game_filter == "all":
        message += "**📈 إحصائيات الشهر الحالي (جميع الألعاب):**\n"
    else:
        message += f"**📈 إحصائيات الشهر الحالي:**\n"
    
    message += f"• **💸 مباع هذا الشهر:** {stats_data['sold_current_month']} حساب\n"
    message += f"• **⛔ محظور هذا الشهر:** {stats_data['banned_current_month']} حساب\n"
    message += f"• **📦 معدل النجاح:** {stats_data['success_rate_current_month']:.1f}%\n"
    message += f"• **💰 أرباح هذا الشهر:** {stats_data['earnings_current_month']:,} ج.م\n"
    message += f"• **⚖️ متوسط سعر البيع:** {stats_data['avg_sale_current_month']:.1f} ج.م\n"
    
    # Only show wallets count for all games (it's user-specific, not game-specific)
    if game_filter == "all":
        message += f"• **💳 محافظ مسجلة:** {stats_data['wallets_count']}\n"
    
    # Show games handled in this month (if filtered by "all")
    if game_filter == "all" and stats_data.get('games_handled'):
        games_list = []
        for game in stats_data['games_handled']:
            game_display = get_game_display_name(game) or game
            games_list.append(game_display)
        
        if games_list:
            message += f"• **🎮 الألعاب التي تم التعامل معها:** {', '.join(games_list)}\n"
    
    # Add all-time stats if available
    if stats_data.get('total_sold_all_time') is not None:
        if game_filter == "all":
            message += "\n**⏳ إحصائيات كل الوقت (جميع الألعاب):**\n"
        else:
            message += f"\n**⏳ إحصائيات كل الوقت للعبة:**\n"
        
        message += f"• **🏆 إجمالي المباع:** {stats_data['total_sold_all_time']} حساب\n"
        message += f"• **💎 إجمالي الأرباح:** {stats_data['total_earnings_all_time']:,} ج.م\n"
    
    # Add a summary footer
    if stats_data['total_current_month'] > 0:
        if game_filter == "all":
            message += f"\n**📋 ملخص الشهر:** تمت معالجة **{stats_data['total_current_month']}** حساب من {len(stats_data.get('games_handled', []))} لعبة مختلفة"
        else:
            message += f"\n**📋 ملخص الشهر:** تمت معالجة **{stats_data['total_current_month']}** حساب"
    
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