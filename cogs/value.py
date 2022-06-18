import sqlite3

import discord
import requests
from discord.ext import commands


class Value(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='value', invoke_without_command=True)
    async def value(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title='Value Options', color=discord.Colour.from_rgb(58, 194, 243))
        embed.add_field(name='-value help ',
                        value='Display the guide for the value command.', inline=True)
        embed.add_field(name='-value convert <values>',
                        value='Convert resources into a monetary value.', inline=True)
        embed.add_field(name='-value rss <values>',
                        value='Display full information about convert process.', inline=True)
        await ctx.send(embed=embed)

    @value.error
    async def convert_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send(f'{error}')

    @value.command()
    async def help(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="Value Information",
                              description='The command accept the order from money to credits and accept only numbers, for set a resource to false use 0.\n Example : -value convert 10 50 15...',
                              color=discord.Colour.from_rgb(58, 194, 243))
        await ctx.send(embed=embed)

    @help.error
    async def convert_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send(f'{error}')

    @value.command()
    async def convert(self, ctx, arg, arg2=None, arg3=None, arg4=None, arg5=None, arg6=None, arg7=None, arg8=None,
                      arg9=None, arg10=None, arg11=None, arg12=None, arg13=None):
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
 tradeprices(first:1){{
  data{{
   food
   aluminum
   steel
   munitions
   gasoline
   bauxite
   iron
   lead
   uranium
   oil
   coal
   credits
  }}
  }}
  }}
 """
            r = requests.post(f"https://api.politicsandwar.com/graphql?api_key={api_key}", json={"query": query})
            data = r.json()["data"]["tradeprices"]["data"]
            for trade in data:
                money = 1
                food = trade['food']
                aluminum = trade['aluminum']
                steel = trade['steel']
                munitions = trade['munitions']
                gasoline = trade['gasoline']
                bauxite = trade['bauxite']
                iron = trade['iron']
                lead = trade['lead']
                uranium = trade['uranium']
                oil = trade['oil']
                coal = trade['coal']
                credits = trade['credits']
            formula = (money * int(arg) + food * int(arg2) + aluminum * int(arg3) + steel * int(arg4) + munitions * int(
                arg5) + gasoline * int(arg6) + bauxite * int(arg7) + iron * int(arg8) + lead * int(
                arg9) + uranium * int(arg10) + oil * int(arg11) + coal * int(arg12) + credits * int(arg13))
            total = round(int(formula) / 0.14)
            loot = round(int(total - formula) / 14)
            await ctx.send(f'Value: ${formula:,}\nTotal Stored : ${total:,}\nEstimated Loot: ${loot:,}')

    @convert.error
    async def convert_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{error}')
        elif isinstance(error, commands.CommandError):
            await ctx.send(f'{error}')

    @value.command()
    async def rss(self, ctx, arg, arg2=None, arg3=None, arg4=None, arg5=None, arg6=None, arg7=None, arg8=None,
                  arg9=None, arg10=None, arg11=None, arg12=None, arg13=None):
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
 tradeprices(first:1){{
  data{{
   food
   aluminum
   steel
   munitions
   gasoline
   bauxite
   iron
   lead
   uranium
   oil
   coal
   credits
  }}
  }}
  }}
 """
            r = requests.post(f"https://api.politicsandwar.com/graphql?api_key={api_key}", json={"query": query})
            data = r.json()["data"]["tradeprices"]["data"]
            for trade in data:
                money = 1
                food = trade['food']
                aluminum = trade['aluminum']
                steel = trade['steel']
                munitions = trade['munitions']
                gasoline = trade['gasoline']
                bauxite = trade['bauxite']
                iron = trade['iron']
                lead = trade['lead']
                uranium = trade['uranium']
                oil = trade['oil']
                coal = trade['coal']
                credits = trade['credits']
            formula = (money * int(arg) + food * int(arg2) + aluminum * int(arg3) + steel * int(arg4) + munitions * int(
                arg5) + gasoline * int(arg6) + bauxite * int(arg7) + iron * int(arg8) + lead * int(
                arg9) + uranium * int(arg10) + oil * int(arg11) + coal * int(arg12) + credits * int(arg13))
            total = round(int(formula) / 0.14)
            loot = round(int(total - formula) / 14)
            await ctx.send(
                f'```Money:${(format(int(arg), ","))} Food:{(format(int(arg2), ","))} Aluminum:{(format(int(arg3), ","))} Steel:{(format(int(arg4), ","))} Munitions:{(format(int(arg5), ","))} Gasoline:{(format(int(arg6), ","))} Bauxite:{(format(int(arg7), ","))} Iron:{(format(int(arg8), ","))} Lead:{(format(int(arg9), ","))} Uranium:{(format(int(arg10), ","))} Oil:{(format(int(arg11), ","))} Coal:{(format(int(arg12), ","))} Credits:{arg13}``` Value: ${formula:,}\n\nTotal Stored : ```Money:${(format(round(int(arg) / 0.14), ","))} Food:{(format(round(int(arg2) / 0.14), ","))} Aluminum:{(format(round(int(arg3) / 0.14), ","))} Steel:{(format(round(int(arg4) / 0.14), ","))} Munitions:{(format(round(int(arg5) / 0.14), ","))} Gasoline:{(format(round(int(arg6) / 0.14), ","))} Bauxite:{(format(round(int(arg7) / 0.14), ","))} Iron:{(format(round(int(arg8) / 0.14), ","))} Lead:{(format(round(int(arg9) / 0.14), ","))} Uranium:{(format(round(int(arg10) / 0.14), ","))} Oil:{(format(round(int(arg11)/ 0.14), ","))} Coal:{(format(round(int(arg12) / 0.14), ","))} Credits:{arg13}``` Value : ${total:,}\n\nYou can loot : ```Money:${(format(round(int(arg) / 0.14 / 14), ","))} Food:{(format(round(int(arg2) / 0.14 / 14), ","))} Aluminum:{(format(round(int(arg3) / 0.14 / 14), ","))} Steel:{(format(round(int(arg4) / 0.14 / 14), ","))} Munitions:{(format(round(int(arg5) / 0.14 / 14), ","))} Gasoline:{(format(round(int(arg6) / 0.14 / 14), ","))} Bauxite:{(format(round(int(arg7) / 0.14 / 14), ","))} Iron:{(format(round(int(arg8) / 0.14 / 14), ","))} Lead:{(format(round(int(arg9) / 0.14 / 14), ","))} Uranium:{(format(round(int(arg10) / 0.14 / 14), ","))} Oil:{(format(round(int(arg11) / 0.14 / 14), ","))} Coal::{(format(round(int(arg12) / 0.14 / 14), ","))} Credits:{arg13}``` Value : ${loot:,}')

    @rss.error
    async def rss_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{error}')
        elif isinstance(error, commands.CommandError):
            await ctx.send(f'{error}')


def setup(bot):
    bot.add_cog(Value(bot))
