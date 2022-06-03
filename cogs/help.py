import discord
from discord.ext import commands
class menu(commands.Cog):
 def __init__(self, bot):
  self.bot = bot
 @commands.command()
 async def help(self, ctx):
  await ctx.message.delete()
  embed = discord.Embed(title='Rizla Commands', color=discord.Colour.from_rgb(58, 194, 243))
  embed.add_field(name='-keystore', value='Display keystore commands information.', inline=True)
  embed.add_field(name='-register', value='Display register commands information.', inline=True)
  embed.add_field(name='-me', value='Display information about yourself.', inline=True)
  embed.add_field(name='-sync', value='Sync your nation information.', inline=True)
  embed.add_field(name='-fastbeige <resistance>', value='Display the best way for beige a enemy.', inline=True)
  embed.add_field(name='-remind <nation_id>', value='Set a reminder for a beige target.', inline=True)
  embed.add_field(name='-fastbeige <war_id>', value='Calculate the best attacks for beige a opponent.', inline=True)
  embed.add_field(name='-spies <nation_id>', value='Display the total spies of a nation and odds for each operation.', inline=True)
  embed.add_field(name='-value <resources>', value='Display the total value of the input resources.', inline=True)
  embed.add_field(name='-loot', value='Display loot commands information.', inline=True)
  embed.add_field(name='-raid', value='Display raid commands information.', inline=True)
  embed.add_field(name='-damage', value='Display damage commands information.', inline=True)
  await ctx.send(embed=embed)
 @help.error
 async def help_error(self, ctx, error):
  if isinstance(error, commands.CommandError):
   await ctx.send(f'{error}')
def setup(bot):
 bot.add_cog(menu(bot))
