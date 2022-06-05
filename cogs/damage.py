import random
import sqlite3

import discord
import requests
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
            await ctx.send(f'{error}')

    @damage.command()
    async def missile(self, ctx, arg):
        conn = sqlite3.connect('dbs/keystore.db')
        cur = conn.cursor()
        cur.execute(f'''SELECT owner_key FROM data WHERE guild_id = {ctx.guild.id}''')
        key = cur.fetchall()[0]
        api_key = str(key[0])
        conn2 = sqlite3.connect('dbs/registered.db')
        cur2 = conn2.cursor()
        cur2.execute(f'''SELECT score FROM data WHERE discord_id = {ctx.message.author.id}''')
        score = str(cur2.fetchall()[0])
        remove_this = "()'',"
        for rt in remove_this:
            score = score.replace(rt, "")
        maxscore = float(score) * 1.75
        minscore = float(score) * 0.75
        if key == 'None':
            await ctx.send('Error parsing the api key, please contact Simons#7609 for solve the problem')
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
            infrastructure = 0
            land = 0
            output = 0
            targets = ''
            for nations in data:
                nat_id = nations['id']
                nat_link = f'https://politicsandwar.com/nation/id={nat_id}'
                nat_name = nations['nation_name']
                cities = nations['num_cities']
                population = nations['population']
                aapos = nations['alliance_position']
                color = nations['color']
                vacmode = nations['vacation_mode_turns']
                for city in nations['cities']:
                    infrastructure += city['infrastructure']
                    land += city['land']
                    avg_infra = round(float(infrastructure / cities))
                    pop_density = round(float(population / land))
                    formula = round(
                        min(random.uniform(300, max(350, pop_density * 3)), (avg_infra * 0.3 + 100), avg_infra), 1)
                    inflict = avg_infra - formula
                    r = requests.get(
                        f"https://politicsandwar.com/city/estimate_infra_land_cost.php?q1={str(inflict)}&q2={str(avg_infra)}").text
                    if aapos != 'APPLICANT' and color != 'beige' and vacmode == 0 and avg_infra >= 1500 and nat_name not in targets and output <= 4:
                        output += 1
                        targets += f'[{nat_name}]({nat_link}) - Estimated Damage : ${r}\n'
        if targets == '':
            await ctx.send('No targets has been found')
        else:
            embed = discord.Embed(title="Missile Damage Targets", description=targets,
                                  color=discord.Colour.from_rgb(58, 194, 243))
            await ctx.send(embed=embed)

    @missile.error
    async def missile_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{error}')
        elif isinstance(error, commands.CommandError):
            await ctx.send(f'{error}')

    @damage.command()
    async def nuke(self, ctx, arg):
        conn = sqlite3.connect('dbs/keystore.db')
        cur = conn.cursor()
        cur.execute(f'''SELECT owner_key FROM data WHERE guild_id = {ctx.guild.id}''')
        key = cur.fetchall()[0]
        api_key = str(key[0])
        conn2 = sqlite3.connect('dbs/registered.db')
        cur2 = conn2.cursor()
        cur2.execute(f'''SELECT score FROM data WHERE discord_id = {ctx.message.author.id}''')
        score = str(cur2.fetchall()[0])
        remove_this = "()'',"
        for rt in remove_this:
            score = score.replace(rt, "")
        maxscore = float(score) * 1.75
        minscore = float(score) * 0.75
        if key == 'None':
            await ctx.send('Error parsing the api key, please contact Simons#7609 for solve the problem')
        else:
            await ctx.send('Please wait...')
            query = f"""
     {{
      nations(first:50, alliance_id:{arg}, min_score:{minscore}, max_score:{maxscore}){{
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
            infrastructure = 0
            land = 0
            output = 0
            targets = ''
            for nations in data:
                nat_id = nations['id']
                nat_link = f'https://politicsandwar.com/nation/id={nat_id}'
                nat_name = nations['nation_name']
                cities = nations['num_cities']
                population = nations['population']
                aapos = nations['alliance_position']
                color = nations['color']
                vacmode = nations['vacation_mode_turns']
                for city in nations['cities']:
                    infrastructure += city['infrastructure']
                    land += city['land']
                    avg_infra = round(float(infrastructure / cities))
                    pop_density = round(float(population / land))
                    formula = round(
                        min(random.uniform(1700, max(2000, pop_density * 13.5)), (avg_infra * 0.8 + 150), avg_infra), 2)
                    inflict = avg_infra - formula
                    r = requests.get(
                        f"https://politicsandwar.com/city/estimate_infra_land_cost.php?q1={str(inflict)}&q2={str(avg_infra)}").text
                    if aapos != 'APPLICANT' and color != 'beige' and vacmode == 0 and avg_infra >= 1800 and nat_name not in targets and output <= 4:
                        output += 1
                        targets += f'[{nat_name}]({nat_link}) - Estimated Damage : ${r}\n'
                if targets == '':
                    await ctx.send('No targets has been found')
                else:
                    embed = discord.Embed(title="Missile Damage Targets", description=targets,
                                          color=discord.Colour.from_rgb(58, 194, 243))
                    await ctx.send(embed=embed)

    @nuke.error
    async def nuke_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{error}')
        elif isinstance(error, commands.CommandError):
            await ctx.send(f'{error}')


def setup(bot):
    bot.add_cog(Damage(bot))
