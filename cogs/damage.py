import discord
import requests
import sqlite3
from discord.ext import commands


class Damage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='damage', invoke_without_command=True)
    async def damage(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title='Damage Options', color=discord.Colour.from_rgb(58, 194, 243))
        embed.add_field(name='-damage missile <alliance_id>',
                        value='Display targets for high infrastructure damage with missiles.', inline=True)
        embed.add_field(name='-damage nuke <alliance_id>',
                        value='Display targets for high infrastructure damage with nukes.', inline=True)
        await ctx.send(embed=embed)

    @damage.error
    async def damage_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send(f'The bot encountered the following error : {error}')

    @damage.command()
    async def missile(self, ctx, arg):
        await ctx.message.delete()
        conn = sqlite3.connect('dbs/keystore.db')
        cur = conn.cursor()
        cur.execute(f'''SELECT owner_key FROM data WHERE guild_id = {ctx.guild.id}''')
        key = cur.fetchall()[0]
        api_key = str(key[0])
        cur.execute(f'''SELECT commands_role FROM data WHERE guild_id = {ctx.guild.id}''')
        get_role = cur.fetchall()[0]
        role = ctx.message.guild.get_role(int(get_role[0]))
        cur.execute(f'''SELECT commands_channel FROM data WHERE guild_id = {ctx.guild.id}''')
        get_channel = cur.fetchall()[0]
        channel = str(get_channel[0])
        conn2 = sqlite3.connect('dbs/registered.db')
        cur2 = conn2.cursor()
        cur2.execute(f'''SELECT discord_id FROM data WHERE discord_id = {ctx.message.author.id}''')
        discord_id = cur2.fetchall()
        cur2.execute(f'''SELECT score FROM data WHERE discord_id = {ctx.message.author.id}''')
        score = str(cur2.fetchall()[0])
        remove_this = "()'',"
        for rt in remove_this:
            score = score.replace(rt, "")
        maxscore = float(score) * 1.75
        minscore = float(score) * 0.75
        if discord_id is None:
            await ctx.send('You are not registered.')
        elif role not in ctx.author.roles:
            await ctx.send(f'You do not have the role : {role}')
        elif str(ctx.channel.id) != channel:
            await ctx.send(f'Please run the command in <#{channel}>')
        else:
            await ctx.send('Please wait...')
            query = f"""
     {{
      nations(first:30, alliance_id:{arg}, min_score:{minscore}, max_score:{maxscore}){{
       data{{
        id
        nation_name
        num_cities
        population
        alliance_position
        color
        vacation_mode_turns
       cities{{
        infrastructure
        land
       }}
       }}
       }}
       }}
      """
            r = requests.post(f"https://api.politicsandwar.com/graphql?api_key={api_key}", json={"query": query})
            data = r.json()["data"]["nations"]["data"]
            for nations in data:
                aapos = nations['alliance_position']
                color = nations['color']
                vacmode = nations['vacation_mode_turns']
                city = sorted(nations['cities'], key=lambda x: x['infrastructure'], reverse=True)[0]
                infrastructure = city['infrastructure']
                land = city['land']
                formula = max(min((300 + max(350, infrastructure * 100 / land * 3)) / 2, infrastructure * 0.3 + 100), 0)
                r = requests.get(
                    f"https://politicsandwar.com/city/estimate_infra_land_cost.php?q1={str(infrastructure)}&q2={str(formula)}").text
                nations['r'] = float(r.replace(",", ""))
            data = sorted(data, key=lambda x: x['r'], reverse=True)
            output = 0
            n = 0
            targets = ""
            while output < 20 and n < len(data):
                nat_name = data[n]['nation_name']
                nat_link = f'https://politicsandwar.com/nation/id={data[n]["id"]}'
                r = data[n]['r']
                if aapos != 'APPLICANT' and color != 'beige' and vacmode == 0:
                    targets += f'[{nat_name}]({nat_link}) - Estimated Damage : ${r:,}\n'
                    output += 1
                n += 1
        if targets == '':
            await ctx.send('No targets has been found')
        else:
            embed = discord.Embed(title="Missile Damage Targets", description=targets,
                                  color=discord.Colour.from_rgb(58, 194, 243))
            await ctx.send(embed=embed)

    @missile.error
    async def missile_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Invalid alliange id.')
        elif isinstance(error, commands.CommandError):
            await ctx.send(f'The bot encountered the following error : {error}')

    @damage.command()
    async def nuke(self, ctx, arg):
        conn = sqlite3.connect('dbs/keystore.db')
        cur = conn.cursor()
        cur.execute(f'''SELECT owner_key FROM data WHERE guild_id = {ctx.guild.id}''')
        key = cur.fetchall()[0]
        api_key = str(key[0])
        cur.execute(f'''SELECT commands_role FROM data WHERE guild_id = {ctx.guild.id}''')
        get_role = cur.fetchall()[0]
        role = ctx.message.guild.get_role(int(get_role[0]))
        cur.execute(f'''SELECT commands_channel FROM data WHERE guild_id = {ctx.guild.id}''')
        get_channel = cur.fetchall()[0]
        channel = str(get_channel[0])
        conn2 = sqlite3.connect('dbs/registered.db')
        cur2 = conn2.cursor()
        cur2.execute(f'''SELECT discord_id FROM data WHERE discord_id = {ctx.message.author.id}''')
        discord_id = cur2.fetchall()
        cur2.execute(f'''SELECT score FROM data WHERE discord_id = {ctx.message.author.id}''')
        score = str(cur2.fetchall()[0])
        remove_this = "()'',"
        for rt in remove_this:
            score = score.replace(rt, "")
        maxscore = float(score) * 1.75
        minscore = float(score) * 0.75
        if discord_id is None:
            await ctx.send('You are not registered.')
        elif role not in ctx.author.roles:
            await ctx.send(f'You do not have the role : {role}')
        elif str(ctx.channel.id) != channel:
            await ctx.send(f'Please run the command in <#{channel}>')
        else:
            await ctx.send('Please wait...')
            query = f"""
        {{
         nations(first:30, alliance_id:{arg}, min_score:{minscore}, max_score:{maxscore}){{
          data{{
           id
           nation_name
           num_cities
           population
           alliance_position
           color
           vacation_mode_turns
          cities{{
           infrastructure
           land
          }}
          }}
          }}
          }}
         """
            r = requests.post(f"https://api.politicsandwar.com/graphql?api_key={api_key}", json={"query": query})
            data = r.json()["data"]["nations"]["data"]
            for nations in data:
                aapos = nations['alliance_position']
                color = nations['color']
                vacmode = nations['vacation_mode_turns']
                city = sorted(nations['cities'], key=lambda x: x['infrastructure'], reverse=True)[0]
                infrastructure = city['infrastructure']
                land = city['land']
                formula = max(
                    min((1700 + max(2000, infrastructure * 100 / land * 13.5)) / 2, infrastructure * 0.8 + 150), 0)
                r = requests.get(
                    f"https://politicsandwar.com/city/estimate_infra_land_cost.php?q1={str(infrastructure)}&q2={str(formula)}").text
                nations['r'] = float(r.replace(",", ""))
            data = sorted(data, key=lambda x: x['r'], reverse=True)
            output = 0
            n = 0
            targets = ""
            while output < 20 and n < len(data):
                nat_name = data[n]['nation_name']
                nat_link = f'https://politicsandwar.com/nation/id={data[n]["id"]}'
                r = data[n]['r']
                if aapos != 'APPLICANT' and color != 'beige' and vacmode == 0:
                    targets += f'[{nat_name}]({nat_link}) - Estimated Damage : ${r:,}\n'
                    output += 1
                n += 1
        if targets == '':
            await ctx.send('No targets has been found')
        else:
            embed = discord.Embed(title="Nuke Damage Targets", description=targets,
                                  color=discord.Colour.from_rgb(58, 194, 243))
            await ctx.send(embed=embed)

    @nuke.error
    async def nuke_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Invalid alliance id.')
        elif isinstance(error, commands.CommandError):
            await ctx.send(f'The bot encountered the following error : {error}')


def setup(bot):
    bot.add_cog(Damage(bot))
