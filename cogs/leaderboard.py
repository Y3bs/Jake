# cogs/stats_v2.py
import discord
from discord.ext import commands
from discord.ui import LayoutView, Container, TextDisplay, Separator, ActionRow, Button, Select
from discord import Interaction, ButtonStyle, SelectOption, app_commands
import utils.database as db
import pandas as pd
from datetime import datetime, timedelta

class LeaderboardSelect(Select):
    def __init__(self):
        options = [
            SelectOption(label="📅 هذا الشهر", value="monthly", description="تصنيف شهر حالي", emoji="📅"),
            SelectOption(label="🏆 كل الوقت", value="all_time", description="تصنيف كل الوقت", emoji="🏆"),
            SelectOption(label="📈 هذا الأسبوع", value="weekly", description="تصنيف أسبوع حالي", emoji="📈"),
        ]
        super().__init__(
            placeholder="اختر نوع التصنيف",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="leaderboard_type"
        )

    async def callback(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        leaderboard_type = self.values[0]
        cog = interaction.client.get_cog("LeaderboardCog")
        await cog.show_leaderboard(interaction, leaderboard_type)

class LeaderboardCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    def calculate_monthly_points(self, sold_count, banned_count):
        """Calculate points for current month based on sold/banned counts"""
        points = (sold_count * 100) - (banned_count * 50)
        return max(points, 0)  # Don't show negative points

    def calculate_all_time_points(self, player_data):
        """Calculate all-time points from player collection"""
        sold = player_data.get('sold', 0)
        banned = player_data.get('banned', 0)
        points = (sold * 100) - (banned * 50)
        return max(points, 0), sold, banned

    async def get_monthly_leaderboard(self):
        """Get monthly leaderboard from records collection"""
        try:
            now = datetime.now()
            first_day_of_month = datetime(now.year, now.month, 1)
            
            # Get all records from current month
            monthly_records = list(db.db.carrier.records.find({
                'time': {'$gte': first_day_of_month.strftime('%Y-%m-%d')}
            }))
            
            # Group by player ID and count sold/banned
            player_stats = {}
            for record in monthly_records:
                player_id = record.get('id')
                if not player_id:
                    continue
                
                if player_id not in player_stats:
                    player_stats[player_id] = {'sold': 0, 'banned': 0}
                
                action = record.get('action', '').lower()
                if action == 'sold':
                    player_stats[player_id]['sold'] += 1
                elif action == 'banned':
                    player_stats[player_id]['banned'] += 1
            
            # Calculate points and prepare leaderboard
            leaderboard = []
            for player_id, stats in player_stats.items():
                points = self.calculate_monthly_points(stats['sold'], stats['banned'])
                if points > 0:  # Only include players with positive points
                    leaderboard.append({
                        'user_id': player_id,
                        'points': points,
                        'sold': stats['sold'],
                        'banned': stats['banned']
                    })
            
            # Sort by points (highest first)
            leaderboard.sort(key=lambda x: x['points'], reverse=True)
            return leaderboard
            
        except Exception as e:
            print(f"Error getting monthly leaderboard: {e}")
            return []

    async def get_weekly_leaderboard(self):
        """Get weekly leaderboard from records collection"""
        try:
            now = datetime.now()
            week_ago = now - timedelta(days=7)
            
            # Get all records from last 7 days
            weekly_records = list(db.db.carrier.records.find({
                'time': {'$gte': week_ago.strftime('%Y-%m-%d')}
            }))
            
            # Group by player ID and count sold/banned
            player_stats = {}
            for record in weekly_records:
                player_id = record.get('id')
                if not player_id:
                    continue
                
                if player_id not in player_stats:
                    player_stats[player_id] = {'sold': 0, 'banned': 0}
                
                action = record.get('action', '').lower()
                if action == 'sold':
                    player_stats[player_id]['sold'] += 1
                elif action == 'banned':
                    player_stats[player_id]['banned'] += 1
            
            # Calculate points and prepare leaderboard
            leaderboard = []
            for player_id, stats in player_stats.items():
                points = self.calculate_monthly_points(stats['sold'], stats['banned'])
                if points > 0:  # Only include players with positive points
                    leaderboard.append({
                        'user_id': player_id,
                        'points': points,
                        'sold': stats['sold'],
                        'banned': stats['banned']
                    })
            
            # Sort by points (highest first)
            leaderboard.sort(key=lambda x: x['points'], reverse=True)
            return leaderboard
            
        except Exception as e:
            print(f"Error getting weekly leaderboard: {e}")
            return []

    async def get_all_time_leaderboard(self):
        """Get all-time leaderboard from players collection"""
        try:
            # Get all players from players collection
            all_players = list(db.db.carrier.players.find())
            
            leaderboard = []
            for player in all_players:
                player_id = player.get('id')
                if not player_id:
                    continue
                
                points, sold, banned = self.calculate_all_time_points(player)
                if points > 0:  # Only include players with positive points
                    leaderboard.append({
                        'user_id': player_id,
                        'points': points,
                        'sold': sold,
                        'banned': banned,
                        'earnings': player.get('earnings', 0)
                    })
            
            # Sort by points (highest first)
            leaderboard.sort(key=lambda x: x['points'], reverse=True)
            return leaderboard
            
        except Exception as e:
            print(f"Error getting all-time leaderboard: {e}")
            return []

    async def get_username(self, user_id):
        """Try to get username from players collection or fetch from Discord"""
        try:
            # First try to get from players collection
            player = db.db.carrier.players.find_one({'id': user_id})
            if player and 'username' in player:
                return player['username']
            
            # Fallback: try to fetch from Discord (optional)
            try:
                user = await self.client.fetch_user(int(user_id))
                return user.name
            except:
                return f"User_{user_id[:6]}"
                
        except Exception:
            return f"User_{user_id[:6]}"

    @app_commands.command(name='leaderboard', description="يعرض لوحة المتصدرين بناءً على النقاط")
    async def leaderboard(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        
        view = LayoutView(timeout=None)
        container = Container(accent_color=discord.Color.gold())
        
        # Title
        container.add_item(TextDisplay(content="# 🏆 لوحة المتصدرين"))
        container.add_item(Separator())
        
        # Description
        desc = TextDisplay(content="""
**🎯 نظام النقاط:**
• كل حساب مباع: **+100 نقطة**
• كل حساب محظور: **-50 نقطة**

النقاط تحافظ على خصوصية أرباح اللاعبين مع إظهار الأداء النسبي.
        """)
        container.add_item(desc)
        container.add_item(Separator())
        
        # Leaderboard type selector
        select = LeaderboardSelect()
        actionrow = ActionRow(select)
        container.add_item(actionrow)
        
        view.add_item(container)
        
        await interaction.followup.send(view=view, ephemeral=True)

    async def show_leaderboard(self, interaction: Interaction, leaderboard_type="monthly"):
        """Show the actual leaderboard"""
        # Get leaderboard data based on type
        if leaderboard_type == "monthly":
            leaderboard_data = await self.get_monthly_leaderboard()
        elif leaderboard_type == "weekly":
            leaderboard_data = await self.get_weekly_leaderboard()
        else:  # all_time
            leaderboard_data = await self.get_all_time_leaderboard()
        
        # Create view
        view = LayoutView(timeout=None)
        container = Container(accent_color=discord.Color.gold())
        
        # Header
        if leaderboard_type == "monthly":
            month_name = datetime.now().strftime("%B")
            header = f"# 📅 تصنيف {month_name}"
        elif leaderboard_type == "weekly":
            header = "# 📈 تصنيف هذا الأسبوع"
        else:
            header = "# 🏆 تصنيف كل الوقت"
        
        container.add_item(TextDisplay(content=header))
        container.add_item(Separator())
        
        # Check if leaderboard is empty
        if not leaderboard_data:
            if leaderboard_type == "monthly":
                month_name = datetime.now().strftime("%B")
                container.add_item(TextDisplay(content=f"📭 لا توجد سجلات في {month_name}"))
            elif leaderboard_type == "weekly":
                container.add_item(TextDisplay(content="📭 لا توجد سجلات هذا الأسبوع"))
            else:
                container.add_item(TextDisplay(content="📭 لا توجد سجلات بعد"))
            
            container.add_item(Separator())
            container.add_item(TextDisplay(content="ابدأ ببيع الحسابات لترى اسمك في التصنيف! 🚀"))
        else:
            # Display top 10
            leaderboard_text = ""
            medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
            
            for i, player in enumerate(leaderboard_data[:10]):
                medal = medals[i] if i < len(medals) else f"{i+1}."
                user_mention = f"<@{player['user_id']}>"
                
                leaderboard_text += (
                    f"{medal} **{user_mention}**\n"
                    f"   النقاط: **{player['points']}** | "
                    f"مباع: {player['sold']} | "
                    f"محظور: {player['banned']}\n"
                )
            
            container.add_item(TextDisplay(content=leaderboard_text))
            container.add_item(Separator())
            
            # Find user's rank
            user_rank = None
            user_stats = None
            for i, player in enumerate(leaderboard_data):
                if str(player['user_id']) == str(interaction.user.id):
                    user_rank = i + 1
                    user_stats = player
                    break
            
            # Show user's rank
            if user_stats:
                user_text = (
                    f"**📊 ترتيبك: #{user_rank}**\n"
                    f"النقاط: **{user_stats['points']}** | "
                    f"مباع: {user_stats['sold']} | "
                    f"محظور: {user_stats['banned']}"
                )
                if leaderboard_type == "all_time" and 'earnings' in user_stats:
                    user_text += f"\n**💰 إجمالي الأرباح:** {user_stats['earnings']:,} ج.م"
                container.add_item(TextDisplay(content=user_text))
            else:
                container.add_item(TextDisplay(content="**📊 ترتيبك:** لم تحصل على نقاط بعد"))
                container.add_item(Separator())
                container.add_item(TextDisplay(content="🚀 ابدأ ببيع الحسابات لترى اسمك في التصنيف!"))
        
        # Add back button
        back_btn = Button(label="↩️ العودة", style=ButtonStyle.secondary, custom_id="back_to_main")
        async def back_callback(interaction: Interaction):
            await interaction.response.defer(ephemeral=True)
            await self.leaderboard(interaction)
        back_btn.callback = back_callback
        
        # Add refresh button
        refresh_btn = Button(label="🔄 تحديث", style=ButtonStyle.primary, custom_id="refresh_lb")
        async def refresh_callback(interaction: Interaction):
            await interaction.response.defer(ephemeral=True)
            await self.show_leaderboard(interaction, leaderboard_type)
        refresh_btn.callback = refresh_callback
        
        btn_row = ActionRow(back_btn, refresh_btn)
        container.add_item(btn_row)
        
        view.add_item(container)
        
        await interaction.followup.send(view=view, ephemeral=True)

async def setup(client):
    await client.add_cog(LeaderboardCog(client))