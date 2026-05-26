from enum import member
from discord.ext import commands
import utils.database as db
from discord import Interaction, Member, app_commands

class MemberEvent(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @app_commands.command(name='register', description="سجل نفسك في قاعدة البيانات")
    async def register(self, interaction: Interaction, member: Member=None):
        await interaction.response.defer(ephemeral=True)
        if member is not None and not interaction.user.guild_permissions.administrator:
            return await interaction.followup.send("أنت لا تملك الصلاحيات اللازمة لتسجيل لاعب آخر")
        if member is None:
            member = interaction.user
        uid = member.id
        if db.find_player(uid):
            return await interaction.followup.send("أنت موجود بالفعل في قاعدة البيانات")
        db.save_player(uid)
        await interaction.followup.send(f"تم تسجيل {member.mention} في قاعدة البيانات")
    
    # @commands.Cog.listener()
    # async def on_member_remove(self, member: Member):
    #     uid = member.id
    #     db.delete_player(uid)

async def setup(client):
    await client.add_cog(MemberEvent(client))