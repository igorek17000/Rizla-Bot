import discord
from discord.ext import commands

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='-', intents=intents, help_command=None)
bot.load_extension("cogs.damage")
bot.load_extension("cogs.fastbeige")
bot.load_extension("cogs.help")
bot.load_extension("cogs.keystore")
bot.load_extension("cogs.listener")
bot.load_extension("cogs.loot")
bot.load_extension("cogs.me")
bot.load_extension("cogs.raid")
bot.load_extension("cogs.register")
bot.load_extension("cogs.reminder")
bot.load_extension("cogs.spies")
bot.load_extension("cogs.sync")
bot.load_extension("cogs.taskloop")
bot.load_extension("cogs.value")


@bot.command()
@commands.is_owner()
async def reload(ctx, arg):
    await ctx.message.delete()
    bot.reload_extension(f'cogs.{arg}')
    await ctx.send(f'The cog {arg}.py has been reloaded.')


@reload.error
async def reload_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.message.delete()
        await ctx.send('No Permission.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        embed = discord.Embed(title='Cogs Options', color=discord.Colour.from_rgb(58, 194, 243))
        embed.add_field(name='damage', value='This cog contain the damage commands.', inline=True)
        embed.add_field(name='fastbeige', value='This cog contain the fastbeige command.', inline=True)
        embed.add_field(name='help', value='This cog contain the help command.', inline=True)
        embed.add_field(name='listener', value='This cog contain the background operation.', inline=True)
        embed.add_field(name='loot', value='This cog contain the loot commands.', inline=True)
        embed.add_field(name='me', value='This cog contain the me command.', inline=True)
        embed.add_field(name='raid', value='This cog contain the raid commands.', inline=True)
        embed.add_field(name='register', value='This cog contain the register commands.', inline=True)
        embed.add_field(name='reminder', value='This cog contain the reminder commands.', inline=True)
        embed.add_field(name='spies', value='This cog contain the spies commands.', inline=True)
        embed.add_field(name='sync', value='This cog contain the sync command.', inline=True)
        embed.add_field(name='taskloop', value='This cog contain the background api operation.', inline=True)
        embed.add_field(name='value', value='This cog contain the value commands.', inline=True)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandError):
        await ctx.message.delete()
        await ctx.send(f'The bot encountered the following error : {error}')


bot.run('') #Use your own bot token.

