import sqlite3
from datetime import *

import requests
from discord.ext import commands


class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sync(self, ctx):
        await ctx.message.delete()
        conn = sqlite3.connect('dbs/keystore.db')
        cur = conn.cursor()
        cur.execute(f'''SELECT owner_key FROM data WHERE guild_id = {ctx.guild.id}''')
        key = cur.fetchall()[0]
        api_key = str(key[0])
        conn2 = sqlite3.connect('dbs/registered.db')
        cur2 = conn2.cursor()
        cur2.execute(f'''SELECT nation_id FROM data WHERE discord_id = {ctx.message.author.id}''')
        nationid = str(cur2.fetchall()[0])
        remove_this = "()'',"
        for rt in remove_this:
            nationid = nationid.replace(rt, "")
        if nationid is None:
            await ctx.send('User Not Found.')
        elif key is None:
            await ctx.send('Error parsing the api key, please contact Simons#7609 for solve the problem.')
        else:
            query = f"""
     {{
      nations(id: {nationid}, first: 1){{
       data{{
        nation_name
        leader_name
        continent
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
                natid = nation['id']
            for off_wars in nation['wars']:
                if off_wars['att_id'] == natid and off_wars['turns_left'] > 0:
                    offensive_wars += 1
            for def_wars in nation['wars']:
                if def_wars['def_id'] == natid and def_wars['turns_left'] > 0:
                    defensive_wars += 1
            for infra in nation['cities']:
                infrastructure += infra['infrastructure']
                lastactive = datetime.fromisoformat(nation['last_active']).replace(tzinfo=None)
                nowtime = datetime.today()
                convtime = round(abs(nowtime - lastactive).total_seconds() / 86400.0)
                natname = nation['nation_name']
                leadname = nation['leader_name']
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
            sql = (
                f"""UPDATE data SET discord_id = '{ctx.message.author.id}', nation_name = '{natname}', leader_name = '{leadname}', last_active = '{convtime}', alliance_position = '{allpos}', color = '{color}', beige_turns = '{beiget}', vacation_mode_turns = '{vacmode}', score = '{score}', soldiers = '{soldiers}', tanks = '{tanks}', aircraft = '{aircraft}', ships = '{ships}', missiles = '{missiles}', nukes = {nukes}, cities = '{cities}', offensive_wars = '{offensive_wars}', defensive_wars = '{defensive_wars}', avg_infra = '{average}', alliance_name = '{allname}', alliance_link = '{allurl}', nation_flag = '{flag}' WHERE discord_id = {ctx.message.author.id}""")
            cur2.execute(sql)
            conn2.commit()
            cur2.close()
            conn2.close()
            await ctx.send(f'{natname} Has been updated.')

    @sync.error
    async def sync_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send(f'The bot encountered the following error : {error}')


def setup(bot):
    bot.add_cog(Sync(bot))
