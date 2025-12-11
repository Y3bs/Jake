from enum import member
from discord.ext import commands
import utils.database as db
from discord import  Interaction, Member, app_commands

class MemberEvent(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @app_commands.command(name='register',description="register your self in the database")
    async def register(self,interaction:Interaction):
        await interaction.response.defer(ephemeral=True)
        uid = interaction.user.id
        if db.find_player(uid):
            return await interaction.followup.send(f"You already exist in the database")
        db.save_player(uid)
        await interaction.followup.send(f"{interaction.user.mention} is registered in the database")
    
    @commands.Cog.listener()
    async def on_member_remove(self,member: Member):
        uid = member.id
        db.delete_player(uid)

async def setup(client):
    await client.add_cog(MemberEvent(client))

    