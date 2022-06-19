import discord
from discord.ext import commands


class Menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title='Rizla Commands', color=discord.Colour.from_rgb(58, 194, 243))
        embed.add_field(name='-keystore', value='Display keystore commands information.', inline=True)
        embed.add_field(name='-register', value='Display register commands information.', inline=True)
        embed.add_field(name='-me', value='Display information about yourself.', inline=True)
        embed.add_field(name='-sync', value='Sync your nation information.', inline=True)
        embed.add_field(name='-fastbeige <resistance>', value='Display the best way for beige a enemy.', inline=True)
        embed.add_field(name='-remind', value='Display remind commands information.', inline=True)
        embed.add_field(name='-spies', value='Display spies commands information.', inline=True)
        embed.add_field(name='-value', value='Display value commands information.', inline=True)
        embed.add_field(name='-loot', value='Display loot commands information.', inline=True)
        embed.add_field(name='-raid', value='Display raid commands information.', inline=True)
        embed.add_field(name='-damage', value='Display damage commands information.', inline=True)
        await ctx.send(embed=embed)

    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send(f'The bot encountered the following error : {error}')


def setup(bot):
    bot.add_cog(Menu(bot))
