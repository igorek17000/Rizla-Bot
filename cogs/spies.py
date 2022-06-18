import math
import sqlite3

import aiohttp
import discord
import requests
from discord.ext import commands


class Spies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='spies', invoke_without_command=True)
    async def spies(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title='Spies Options', color=discord.Colour.from_rgb(58, 194, 243))
        embed.add_field(name='-spies amount <nation_id>', value='Display the amount of spies the nation have.',
                        inline=True)
        embed.add_field(name='-spies odds <nation_id>', value='Display the odds for each espionage type.', inline=True)
        await ctx.send(embed=embed)

    @spies.error
    async def spies_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send(f'{error}')

    @spies.command()
    async def amount(self, ctx, arg):
        await ctx.message.delete()
        conn = sqlite3.connect('dbs/keystore.db')
        cur = conn.cursor()
        cur.execute(f'''SELECT owner_key FROM data WHERE guild_id = {ctx.guild.id}''')
        key = cur.fetchall()[0]
        api_key = str(key[0])
        if key is None:
            await ctx.send('Error parsing the api key, please contact Simons#7609 for solve the problem')
        else:
            query = f"""
  {{
   nations(id:{arg}){{
    data{{
     nation_name
     id
     war_policy
     central_intelligence_agency
    }}
    }}
    }}
   """
            r = requests.post(f"https://api.politicsandwar.com/graphql?api_key={api_key}", json={"query": query})
            data = r.json()["data"]["nations"]["data"]
            for nations in data:
                nation_id = nations['id']
                nation_name = nations['nation_name']
                war_policy = nations['war_policy']
                central_intelligence_agency = nations['central_intelligence_agency']
                async with aiohttp.ClientSession() as session:
                    if war_policy == "ARCANE":
                        percent = 57.5
                    elif war_policy == "TACTICIAN":
                        percent = 42.5
                    else:
                        percent = 50
                    upper_lim = 60
                    lower_lim = 0
                    while True:
                        spycount = math.floor((upper_lim + lower_lim) / 2)
                        async with session.get(
                                f"https://politicsandwar.com/war/espionage_get_odds.php?id1=255385&id2={nation_id}&id3=0&id4=1&id5={spycount}") as probability:
                            probability = await probability.text()
                        if "Greater than 50%" in probability:
                            upper_lim = spycount
                        else:
                            lower_lim = spycount
                        if upper_lim - 1 == lower_lim:
                            break
                    spies = round((((100 * int(spycount)) / (percent - 25)) - 2) / 3)
                    if spies > 60:
                        spies = 60
                    elif spies > 50 and not central_intelligence_agency:
                        spies = 50
                    elif spies < 2:
                        spies = 0
                await ctx.send(f'{nation_name} have {spies} spies.')

    @spies.command()
    async def odds(self, ctx, arg):
        await ctx.message.delete()
        conn = sqlite3.connect('dbs/keystore.db')
        cur = conn.cursor()
        cur.execute(f'''SELECT owner_key FROM data WHERE guild_id = {ctx.guild.id}''')
        key = cur.fetchall()[0]
        api_key = str(key[0])
        conn2 = sqlite3.connect('dbs/registered.db')
        cur2 = conn2.cursor()
        cur2.execute(f'''SELECT nation_id FROM data WHERE discord_id = {ctx.message.author.id}''')
        your_id = str(cur2.fetchall()[0])
        remove_this = "()'',"
        for rt in remove_this:
            your_id = your_id.replace(rt, "")
        if key is None:
            await ctx.send('Error parsing the api key, please contact Simons#7609 for solve the problem')
        else:
            query = f"""
        {{
         nations(id:{arg}){{
          data{{
           nation_name
           id
           war_policy
           central_intelligence_agency
          }}
          }}
          }}
         """
            r = requests.post(f"https://api.politicsandwar.com/graphql?api_key={api_key}", json={"query": query})
            data = r.json()["data"]["nations"]["data"]
            for nations in data:
                nation_id = nations['id']
                war_policy = nations['war_policy']
                central_intelligence_agency = nations['central_intelligence_agency']
                async with aiohttp.ClientSession() as session:
                    if war_policy == "ARCANE":
                        percent = 57.5
                    elif war_policy == "TACTICIAN":
                        percent = 42.5
                    else:
                        percent = 50
                    upper_lim = 60
                    lower_lim = 0
                    while True:
                        spycount = math.floor((upper_lim + lower_lim) / 2)
                        async with session.get(
                                f"https://politicsandwar.com/war/espionage_get_odds.php?id1={your_id}&id2={nation_id}&id3=0&id1=3&id5={spycount}") as probability:
                            probability = await probability.text()
                        if "Greater than 50%" in probability:
                            upper_lim = spycount
                        else:
                            lower_lim = spycount
                        if upper_lim - 1 == lower_lim:
                            break
                    spies = round((((100 * int(spycount)) / (percent - 25)) - 2) / 3)
                    if spies > 60:
                        spies = 60
                    elif spies > 50 and not central_intelligence_agency:
                        spies = 50
                    elif spies < 2:
                        spies = 0
                    modifier = 0
                    if war_policy == "TACTICIAN":
                        modifier += 1.15
                    elif war_policy == "ARCANE":
                        modifier += 0.85
                    elif war_policy == "COVERT":
                        modifier += 1.15
                    odds = 3 * 25 + (int(spycount) * 100 / ((spies * 3) + 1)) * modifier
                    ass_tanks = odds / 1.5
                    sab_aircraft = odds / 2
                    sab_ships = odds / 3
                    sab_missile = odds / 4
                    sab_nuclear = odds / 5
                    await ctx.send(
                        f'You have {round(ass_tanks)}% chances to assasinate enemy spies.\nYou have {round(ass_tanks)}% chances to sabotage enemy tanks.\nYou have {round(sab_aircraft)}% chances to sabotage enemy aircraft.\nYou have {round(sab_ships)}% chances to sabotage enemy ships.\nYou have {round(sab_missile)}% chances to sabotage enemy missile.\nYou have {round(sab_nuclear)}% chances to sabotage enemy nuclear.\nThe chances are calculate using Extremely covert as paramether.')


def setup(bot):
    bot.add_cog(Spies(bot))
