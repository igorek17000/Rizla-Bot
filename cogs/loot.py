import discord
from discord.ext import commands
class loot(commands.Cog):
 def __init__(self, bot):
  self.bot = bot
def setup(bot):
 bot.add_cog(loot(bot))
