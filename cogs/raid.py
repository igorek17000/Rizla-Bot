import discord
from discord.ext import commands
class raid(commands.Cog):
 def __init__(self, bot):
  self.bot = bot
def setup(bot):
 bot.add_cog(raid(bot))
