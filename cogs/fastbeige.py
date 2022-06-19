import sqlite3
from discord.ext import commands
from itertools import *


class Fastbeige(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fastbeige(self, ctx, arg):
        await ctx.message.delete()
        conn = sqlite3.connect('dbs/keystore.db')
        cur = conn.cursor()
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
        if discord_id is None:
            await ctx.send('You are not registered.')
        elif role not in ctx.author.roles:
            await ctx.send(f'You do not have the role : {role}')
        elif str(ctx.channel.id) != channel:
            await ctx.send(f'Please run the command in <#{channel}>')
        elif int(arg) > 100:
            await ctx.send('Insert a value between 1 to 100.')
        elif int(arg) <= 0:
            await ctx.send('Insert a value between 1 to 100.')
        else:
            ground = 0
            naval = 0
            attacks = [(10, 10), (10, 14)]
            all_attacks = [n for a, b in attacks for n in [b] * a]
            combs = {sum(x): x for i in range(1, 10) for x in combinations(all_attacks, i)}
            for i in sorted(combs):
                if i >= int(arg):
                    break
            for x in combs[i]:
                if x == 10:
                    ground += 1
                elif x == 14:
                    naval += 1
            await ctx.send(
                f'The fastest way to beige a target with {arg}% resistance is {ground} ground attacks and {naval} naval attacks.')

    @fastbeige.error
    async def fastbeige_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'Invalid resistance.')
        elif isinstance(error, commands.CommandError):
            await ctx.send(f'The bot encountered the following error : {error}')


def setup(bot):
    bot.add_cog(Fastbeige(bot))
