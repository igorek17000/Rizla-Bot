from itertools import *

from discord.ext import commands


class Fastbeige(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fastbeige(self, ctx, arg):
        await ctx.message.delete()
        if int(arg) > 100:
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
            await ctx.send(f'{error}')
        elif isinstance(error, commands.CommandError):
            await ctx.send(f'{error}')


def setup(bot):
    bot.add_cog(Fastbeige(bot))
