import sqlite3

import discord
from discord.ext import commands


class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(name='Use -help'))
        print('Rizla is online!')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        conn = sqlite3.connect('dbs/keystore.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS data
   (guild_id TEXT UNIQUE,
   owner_key TEXT,
   commands_channel TEXT,
   commands_role TEXT,
   dnr_list TEXT)''')
        cur.execute(f'''INSERT INTO data(guild_id) VALUES ({guild.id})''')
        cur.execute(f'''UPDATE data SET owner_key = ('') WHERE guild_id = ({guild.id})''')  # Insert your own api key.
        conn.commit()
        cur.close()
        conn.close()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        conn = sqlite3.connect('dbs/keystore.db')
        cur = conn.cursor()
        cur.execute(f'''DELETE FROM data WHERE guild_id = ({guild.id})''')
        conn.commit()
        cur.close()
        conn.close()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.message.delete()
            await ctx.send(f'{error}')


def setup(bot):
    bot.add_cog(Listener(bot))
