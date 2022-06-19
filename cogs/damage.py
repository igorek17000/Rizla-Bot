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
        keystores = sqlite3.connect('dbs/keystore.db')
        pull = keystores.cursor()
        users = sqlite3.connect('dbs/registered.db')
        pull2 = users.cursor()
        pull.execute(f'''SELECT owner_key FROM data WHERE guild_id = {ctx.guild.id}''')
        api_key = str(pull.fetchone()[0])
        if api_key is None:
            await ctx.send('Unable to retrieve the api key.')
        else:
            pull2.execute(f'''SELECT discord_id FROM data WHERE discord_id = {ctx.message.author.id}''')
            discord_id = pull2.fetchone()
            pull2.execute(f'''SELECT score FROM data WHERE discord_id = {ctx.message.author.id}''')
            score_check = pull2.fetchone()
        if discord_id is None and score_check is None:
            await ctx.send('You are not registered')
        else:
            pull.execute(f'''SELECT commands_role FROM data WHERE guild_id = {ctx.guild.id}''')
            get_role = pull.fetchall()[0]
            role = ctx.message.guild.get_role(int(get_role[0]))
        if role not in ctx.author.roles:
            await ctx.send(f'You do not have the role : {role}.')
        else:
            pull.execute(f'''SELECT commands_channel FROM data WHERE guild_id = {ctx.guild.id}''')
            get_channel = pull.fetchone()
            white_channel = str(get_channel[0])
        if white_channel != str(ctx.channel.id):
            await ctx.send(f'Run the comamnds in the channel : <#{white_channel}>.')
        else:
            score = str(score_check[0])
            remove_this = "()'',"
            for rt in remove_this:
                score = score.replace(rt, "")
            low_score = float(score) * 0.75
            high_score = float(score) * 1.75
            await ctx.send('Please wait...')
            query = f"""
     {{
      nations(first:30, alliance_id:{arg}, min_score:{low_score}, max_score:{high_score}){{
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
        await ctx.message.delete()
        keystores = sqlite3.connect('dbs/keystore.db')
        pull = keystores.cursor()
        users = sqlite3.connect('dbs/registered.db')
        pull2 = users.cursor()
        pull.execute(f'''SELECT owner_key FROM data WHERE guild_id = {ctx.guild.id}''')
        api_key = str(pull.fetchone()[0])
        if api_key is None:
            await ctx.send('Unable to retrieve the api key.')
        else:
            pull2.execute(f'''SELECT discord_id FROM data WHERE discord_id = {ctx.message.author.id}''')
            discord_id = pull2.fetchone()
            pull2.execute(f'''SELECT score FROM data WHERE discord_id = {ctx.message.author.id}''')
            score_check = pull2.fetchone()
        if discord_id is None and score_check is None:
            await ctx.send('You are not registered')
        else:
            pull.execute(f'''SELECT commands_role FROM data WHERE guild_id = {ctx.guild.id}''')
            get_role = pull.fetchall()[0]
            role = ctx.message.guild.get_role(int(get_role[0]))
        if role not in ctx.author.roles:
            await ctx.send(f'You do not have the role : {role}.')
        else:
            pull.execute(f'''SELECT commands_channel FROM data WHERE guild_id = {ctx.guild.id}''')
            get_channel = pull.fetchone()
            white_channel = str(get_channel[0])
        if white_channel != str(ctx.channel.id):
            await ctx.send(f'Run the comamnds in the channel : <#{white_channel}>.')
        else:
            score = str(score_check[0])
            remove_this = "()'',"
            for rt in remove_this:
                score = score.replace(rt, "")
            low_score = float(score) * 0.75
            high_score = float(score) * 1.75
            await ctx.send('Please wait...')
            query = f"""
     {{
      nations(first:30, alliance_id:{arg}, min_score:{low_score}, max_score:{high_score}){{
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
            await ctx.send('Invalid alliange id.')
        elif isinstance(error, commands.CommandError):
            await ctx.send(f'The bot encountered the following error : {error}')


def setup(bot):
    bot.add_cog(Damage(bot))
