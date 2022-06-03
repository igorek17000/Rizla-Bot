import discord
import sqlite3
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import commands
class keystore(commands.Cog):
 def __init__(self, bot):
  self.bot = bot
 @commands.group(name='keystore', invoke_without_command=True)
 @commands.has_permissions(administrator=True)
 async def keystore(self, ctx):
  await ctx.message.delete()
  embed = discord.Embed(title='Keystore Commands', color=discord.Colour.from_rgb(58, 194, 243))
  embed.add_field(name='-keystore settings', value='Display values in the database.', inline=True)
  embed.add_field(name='-keystore available', value='Display bot keystores.', inline=True)
  embed.add_field(name='-keystore channel #channel', value='Set channel for run bot commands.', inline=True)
  embed.add_field(name='-keystore role @role', value='Set role for run bot commands.', inline=True)
  embed.add_field(name='-keystore dnr <ids>', value='Set a list of alliance ids for exclude them from raid targets list.', inline=True)
  embed.add_field(name='-keystore remove <keystore>', value='Display options for remove keystores.', inline=True)
  await ctx.send(embed=embed)
 @keystore.error
 async def keystore_error(self, ctx, error):
  if isinstance(error, MissingPermissions):
   await ctx.message.delete()
   await ctx.send(f'{error}')
  elif isinstance(error, commands.CommandError):
   await ctx.message.delete()
   await ctx.send(f'{error}')
 @keystore.command()
 @commands.has_permissions(administrator=True)
 async def available(self, ctx):
  await ctx.message.delete()
  embed = discord.Embed(title='Keystore Values', color=discord.Colour.from_rgb(58, 194, 243))
  embed.add_field(name='guild_id', value='This value determine your server id.', inline=True)
  embed.add_field(name='owner_key', value='This value allow the interaction with PnW api.', inline=True)
  embed.add_field(name='commands_channel', value='This value determine the channel you want to use for Data commands.', inline=True)
  embed.add_field(name='commands_role', value='This value determine the role able to use Data commands.', inline=True)
  embed.add_field(name='dnr_list', value='This value force the bot to exclude certain alliance ids from the raid output list.', inline=True)
  await ctx.send(embed=embed)
 @available.error
 async def available_error(self, ctx, error):
  if isinstance(error, MissingPermissions):
   await ctx.message.delete()
   await ctx.send(f'{error}')
  elif isinstance(error, commands.CommandError):
   await ctx.message.delete()
   await ctx.send(f'{error}')
 @keystore.command()
 @has_permissions(administrator=True)
 async def settings(self, ctx):
  await ctx.message.delete()
  conn = sqlite3.connect('dbs/keystore.db')
  cur = conn.cursor()
  cur.execute(f'''SELECT guild_id FROM data WHERE guild_id = {ctx.guild.id}''')
  res = cur.fetchall()[0]
  cur.execute(f'''SELECT owner_key FROM data WHERE guild_id = {ctx.guild.id}''')
  res1 = cur.fetchall()[0]
  cur.execute(f'''SELECT commands_channel FROM data WHERE guild_id = {ctx.guild.id}''')
  res3 = cur.fetchall()[0]
  cur.execute(f'''SELECT commands_role FROM data WHERE guild_id = {ctx.guild.id}''')
  res4 = cur.fetchall()[0]
  cur.execute(f'''SELECT dnr_list FROM data WHERE guild_id = {ctx.guild.id}''')
  res5 = cur.fetchall()[0]
  guildid = str(res[0])
  apikey = str(res1[0])
  channelc = str(res3[0])
  channelrole = str(res4[0])
  output = str(res5[0])
  dnr = output.split()
  if apikey == 'None':
   embed = discord.Embed(title='Bot Configuration', color=discord.Colour.from_rgb(58, 194, 243))
   embed.add_field(name='Guild ID', value=guildid, inline=True)
   embed.add_field(name='Api Key', value=apikey, inline=True)
   embed.add_field(name='Commands Role', value=f"<@&{channelrole}>", inline=True)
   embed.add_field(name='DNR List', value=dnr, inline=True)
   await ctx.send(embed=embed)
  else:
   embed = discord.Embed(title='Bot Configuration', color=discord.Colour.from_rgb(58, 194, 243))
   embed.add_field(name='Guild ID', value=guildid, inline=True)
   embed.add_field(name='Api Key', value='Redacted', inline=True)
   embed.add_field(name='Commands Role', value=f"<@&{channelrole}>", inline=True)
   embed.add_field(name='DNR List', value=dnr, inline=True)
   await ctx.send(embed=embed)
 @settings.error
 async def settings_error(self, ctx, error):
  if isinstance(error, MissingPermissions):
   await ctx.message.delete()
   await ctx.send(f'{error}')
  elif isinstance(error, commands.CommandError):
   await ctx.message.delete()
   await ctx.send(f'{error}')
 @keystore.command()
 @has_permissions(administrator=True)
 async def channel(self, ctx, channel:discord.TextChannel):
  await ctx.message.delete()
  conn = sqlite3.connect('dbs/keystore.db')
  cur = conn.cursor()
  sql = ('''UPDATE data SET commands_channel = ? WHERE guild_id = ?''')
  val = (channel.id, ctx.guild.id)
  cur.execute(sql,val)
  conn.commit()
  cur.close()
  conn.close()
  await ctx.send(f'You will be able to use Data commands in the channel below.\n<#{channel.id}>.')
 @channel.error
 async def channel_error(self, ctx, error):
  if isinstance(error, MissingPermissions):
   await ctx.message.delete()
   await ctx.send(f'{error}')
  elif isinstance(error, commands.MissingRequiredArgument):
   await ctx.message.delete()
   await ctx.send(f'{error}')
  elif isinstance(error, commands.CommandError):
   await ctx.message.delete()
   await ctx.send(f'{error}')
 @keystore.command()
 @has_permissions(administrator=True)
 async def role(self, ctx, role:discord.Role):
  await ctx.message.delete()
  conn = sqlite3.connect('dbs/keystore.db')
  cur = conn.cursor()
  sql = ('''UPDATE data SET commands_role = ? WHERE guild_id = ?''')
  val = (role.id, ctx.guild.id)
  cur.execute(sql,val)
  conn.commit()
  cur.close()
  conn.close()
  await ctx.send(f'Every user with the role below will able to use Data commands.\n<@&{role.id}>.')
 @role.error
 async def role_error(self, ctx, error):
  if isinstance(error, MissingPermissions):
   await ctx.message.delete()
   await ctx.send(f'{error}')
  elif isinstance(error, commands.MissingRequiredArgument):
   await ctx.message.delete()
   await ctx.send(f'{error}')
  elif isinstance(error, commands.CommandError):
   await ctx.message.delete()
   await ctx.send(f'{error}')
 @keystore.command()
 @has_permissions(administrator=True)
 async def dnr(self, ctx, *, text):
  await ctx.message.delete()
  conn = sqlite3.connect('dbs/keystore.db')
  cur = conn.cursor()
  cur.execute(f'''SELECT dnr_list FROM data WHERE guild_id = {ctx.guild.id}''')
  res = cur.fetchone()
  currentdnr = str(res[0])
  if currentdnr == 'None':
   sql = ('''UPDATE data SET dnr_list = ? WHERE guild_id = ?''')
   val = (text, ctx.guild.id)
   cur.execute(sql,val)
   conn.commit()
   cur.close()
   conn.close()
   await ctx.send(f'Dnr list has been created successfully.\n{text}')
  else:
   olddnr = str(res[0])
   newdnr = ('{} {}'.format(olddnr, text))
   sql = ('''UPDATE data SET dnr_list = ? WHERE guild_id = ?''')
   val = (newdnr, ctx.guild.id)
   cur.execute(sql,val)
   conn.commit()
   cur.close()
   conn.close()
   await ctx.send(f'Dnr list has been updated successfully.\n{newdnr}')
 @dnr.error
 async def dnr_error(self, ctx, error):
  if isinstance(error, MissingPermissions):
   await ctx.message.delete()
   await ctx.send(f'{error}')
  elif isinstance(error, commands.MissingRequiredArgument):
   await ctx.message.delete()
   await ctx.send(f'{error}')
  elif isinstance(error, commands.CommandError):
   await ctx.message.delete()
   await ctx.send(f'{error}')
 @keystore.command()
 @has_permissions(administrator=True)
 async def remove(self, ctx, arg):
  await ctx.message.delete()
  if arg == 'guild_id':
   await ctx.send('No permission.')
  elif arg == 'owner_key':
   await ctx.send('No permission.')
  else:
   conn = sqlite3.connect('dbs/keystore.db')
   cur = conn.cursor()
   sql = (f'''UPDATE data SET {arg} = NULL WHERE guild_id = {ctx.guild.id}''')
   cur.execute(sql)
   conn.commit()
   cur.close()
   conn.close()
   await ctx.send(f'{arg} Keystore has been deleted.')
 @remove.error
 async def remove_error(self, ctx, error):
  if isinstance(error, commands.NotOwner):
   await ctx.message.delete()
   await ctx.send(f'{error}')
  elif isinstance(error, commands.MissingRequiredArgument):
   await ctx.message.delete()
   await ctx.send(f'{error}')
  elif isinstance(error, commands.CommandError):
   await ctx.message.delete()
   await ctx.send(f'{error}')
def setup(bot):
 bot.add_cog(keystore(bot))
