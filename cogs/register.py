import discord
import sqlite3
import requests
import random
from datetime import *
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import commands
class register(commands.Cog):
 def __init__(self, bot):
  self.bot = bot
 @commands.group(name='register', invoke_without_command=True)
 async def register(self, ctx):
  await ctx.message.delete()
  embed = discord.Embed(title='Register Options', color=discord.Colour.from_rgb(58, 194, 243))
  embed.add_field(name='-register user <nation_id>', value='This command allow to register yourself in the bot database.', inline=True)
  embed.add_field(name='-register admin @user <nation_id>', value='This command allow a admin to register a nation in the database, bypassing the code input.', inline=True)
  await ctx.send(embed=embed)
 @register.error
 async def register_error(self, ctx, error):
  if isinstance(error, commands.CommandError):
   await ctx.send(f'{error}')
 @register.command()
 async def user(self, ctx, arg):
  await ctx.message.delete()
  conn = sqlite3.connect('dbs/keystore.db')
  cur = conn.cursor()
  cur.execute(f'''SELECT owner_key FROM data WHERE guild_id = {ctx.guild.id}''')
  key = cur.fetchall()[0]
  api_key = str(key[0])
  conn2 = sqlite3.connect('dbs/registered.db')
  cur2 = conn2.cursor()
  cur2.execute(f'''SELECT nation_id FROM data WHERE discord_id = {ctx.message.author.id}''')
  output = cur2.fetchall()
  nation = str(output)
  if key == 'None':
   await ctx.message.delete()
   await ctx.send('Error parsing the api key, please contact Simons#7609 for solve the problem')
  elif arg in nation:
   await ctx.message.delete()
   await ctx.send('This nation is already registered.')
  else:
   code = random.randint(1,9999)
   subject = 'Rizla Verification Code'
   message = f'Greetings dear player.<br>Your verification code is : {code}.<br>Copy the code and past it in the verification channel.'
   endpoint = 'https://politicsandwar.com/api/send-message/'
   values = {'key' : f'{api_key}',
            'to' : f'{arg}',
            'subject' : f'{subject}',
            'message' : f'{message}'
            }
   r = requests.post(endpoint, data = values)
   await ctx.send('The verification code has been sent in-game.')
   message = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=600.0)
   if message.content.lower() == f'{code}':
    query = f"""
     {{
      nations(id: {arg}, first: 1){{
       data{{
        nation_name
        leader_name
        id
        last_active
        alliance_position
        color
        beige_turns
        vacation_mode_turns
        score
        soldiers
        tanks
        aircraft
        ships
        missiles
        nukes
        num_cities
        flag
       wars{{
        att_id
        def_id
        turns_left
       }}
       cities{{
        infrastructure
       }}
       alliance{{
        id
        name
       }}
       }}
       }}
       }}
      """
    r = requests.post(f'https://api.politicsandwar.com/graphql?api_key={api_key}', json={'query': query})
    data = r.json()['data']['nations']['data']
    infrastructure = 0
    offensive_wars = 0
    defensive_wars = 0
    for nation in data:
     for off_wars in nation['wars']:
      if off_wars['att_id'] == arg and off_wars['turns_left'] > 0:
       offensive_wars += 1
     for def_wars in nation['wars']:
      if def_wars['def_id'] == arg and def_wars['turns_left'] > 0:
       defensive_wars += 1
     for infra in nation['cities']:
      infrastructure += infra['infrastructure']
     natname = nation['nation_name']
     leadname = nation['leader_name']
     natid = nation['id']
     natlink = f'https://politicsandwar.com/nation/id={natid}'
     lastactive = datetime.fromisoformat(nation['last_active']).replace(tzinfo=None)
     nowtime = datetime.today()
     convtime = round(abs(nowtime - lastactive).total_seconds() / 86400.0)
     allpos = nation['alliance_position']
     color = nation['color']
     beiget = nation['beige_turns']
     vacmode = nation['vacation_mode_turns']
     score = nation['score']
     soldiers = nation['soldiers']
     tanks = nation['tanks']
     aircraft = nation['aircraft']
     ships = nation['ships']
     missiles = nation['missiles']
     nukes = nation['nukes']
     cities = nation['num_cities']
     flag = nation['flag']
     average = round(infrastructure / nation['num_cities'])
     allname = nation['alliance']['name']
     allid = nation['alliance']['id']
     allurl = f'https://politicsandwar.com/alliance/id={allid}'
    sql = ('''INSERT INTO data(nation_id, discord_id, nation_name, leader_name, nation_link, last_active, alliance_position, color, beige_turns, vacation_mode_turns, score, soldiers, tanks, aircraft, ships, missiles, nukes, cities, offensive_wars, defensive_wars, avg_infra, alliance_name, alliance_link, nation_flag) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''')
    val = (natid, ctx.message.author.id, natname, leadname, natlink, convtime, allpos, color, beiget, vacmode, score, soldiers, tanks, aircraft, ships, missiles, nukes, cities, offensive_wars, defensive_wars,  average, allname, allurl, flag)
    cur2.execute(sql, val)
    conn2.commit()
    cur2.close()
    conn2.close()
    await ctx.send(f'Your nation {natname} has been registered correctly.')
   else:
    await ctx.send('Something goes wrong.')
 @user.error
 async def user_error(self, ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
   await ctx.message.delete()
   await ctx.send(f'{error}')
  elif isinstance(error, commands.CommandError):
   await ctx.message.delete()
   await ctx.send(f'{error}')
 @register.command()
 @has_permissions(administrator=True)
 async def admin(self, ctx, member: discord.Member, arg):
  await ctx.message.delete()
  conn = sqlite3.connect('dbs/keystore.db')
  cur = conn.cursor()
  cur.execute(f'''SELECT owner_key FROM data WHERE guild_id = {ctx.guild.id}''')
  key = cur.fetchall()[0]
  api_key = str(key[0])
  conn2 = sqlite3.connect('dbs/registered.db')
  cur2 = conn2.cursor()
  cur2.execute(f'''SELECT nation_id FROM data WHERE discord_id = {member.id}''')
  output = cur2.fetchall()
  nation = str(output)
  if key == 'None':
   await ctx.message.delete()
   await ctx.send('Error parsing the api key, please contact Simons#7609 for solve the problem.')
  elif arg in nation:
   await ctx.message.delete()
   await ctx.send('This nation is already registered.')
  else:
    query = f"""
     {{
      nations(id: {arg}, first: 1){{
       data{{
        nation_name
        leader_name
        id
        last_active
        alliance_position
        color
        beige_turns
        vacation_mode_turns
        score
        soldiers
        tanks
        aircraft
        ships
        missiles
        nukes
        num_cities
        flag
       wars{{
        att_id
        def_id
        turns_left
       }}
       cities{{
        infrastructure
       }}
       alliance{{
        id
        name
       }}
       }}
       }}
       }}
      """
    r = requests.post(f'https://api.politicsandwar.com/graphql?api_key={api_key}', json={'query': query})
    data = r.json()['data']['nations']['data']
    infrastructure = 0
    offensive_wars = 0
    defensive_wars = 0
    for nation in data:
     for off_wars in nation['wars']:
      if off_wars['att_id'] == arg and off_wars['turns_left'] > 0:
       offensive_wars += 1
     for def_wars in nation['wars']:
      if def_wars['def_id'] == arg and def_wars['turns_left'] > 0:
       defensive_wars += 1
     for infra in nation['cities']:
      infrastructure += infra['infrastructure']
     natname = nation['nation_name']
     leadname = nation['leader_name']
     natid = nation['id']
     natlink = f'https://politicsandwar.com/nation/id={natid}'
     lastactive = datetime.fromisoformat(nation['last_active']).replace(tzinfo=None)
     nowtime = datetime.today()
     convtime = round(abs(nowtime - lastactive).total_seconds() / 86400.0)
     allpos = nation['alliance_position']
     color = nation['color']
     beiget = nation['beige_turns']
     vacmode = nation['vacation_mode_turns']
     score = nation['score']
     soldiers = nation['soldiers']
     tanks = nation['tanks']
     aircraft = nation['aircraft']
     ships = nation['ships']
     missiles = nation['missiles']
     nukes = nation['nukes']
     cities = nation['num_cities']
     flag = nation['flag']
     average = round(infrastructure / nation['num_cities'])
     allname = nation['alliance']['name']
     allid = nation['alliance']['id']
     allurl = f'https://politicsandwar.com/alliance/id={allid}'
    sql = ('''INSERT INTO data(nation_id, discord_id, nation_name, leader_name, nation_link, last_active, alliance_position, color, beige_turns, vacation_mode_turns, score, soldiers, tanks, aircraft, ships, missiles, nukes, cities, offensive_wars, defensive_wars, avg_infra, alliance_name, alliance_link, nation_flag) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''')
    val = (natid, member.id, natname, leadname, natlink, convtime, allpos, color, beiget, vacmode, score, soldiers, tanks, aircraft, ships, missiles, nukes, cities, offensive_wars, defensive_wars,  average, allname, allurl, flag)
    cur2.execute(sql, val)
    conn2.commit()
    cur2.close()
    conn2.close()
    await ctx.send(f'The nation {natname} has been registered correctly.')
 @admin.error
 async def admin_error(self, ctx, error):
  if isinstance(error, MissingPermissions):
   await ctx.message.delete()
   await ctx.send(f'{error}')
  elif isinstance(error, commands.MissingRequiredArgument):
   await ctx.message.delete()
   await ctx.send(f'{error}')
  elif isinstance(error, commands.CommandError):
   await ctx.message.delete()
   await ctx.send(f'{error}')
class unregister(commands.Cog):
 def __init__(self, bot):
  self.bot = bot
 @commands.command()
 async def unregister(self, ctx):
  await ctx.message.delete()
  conn = sqlite3.connect('dbs/registered.db')
  cur = conn.cursor()
  cur.execute(f'''SELECT discord_id FROM data WHERE discord_id = {ctx.message.author.id}''')
  res = cur.fetchone()
  if res is None:
   await ctx.send('User Not Found')
  else:
   sql = (f'''DELETE from data WHERE discord_id=({ctx.message.author.id})''')
   cur.execute(sql)
   conn.commit()
   cur.close()
   conn.close()
   await ctx.send('Your nation has been unregistered correctly.')
 @unregister.error
 async def unregister_error(self, ctx, error):
  if isinstance(error, commands.CommandError):
   await ctx.message.delete()
   await ctx.send(f'{error}')   
def setup(bot):
 bot.add_cog(register(bot))
 bot.add_cog(unregister(bot))
