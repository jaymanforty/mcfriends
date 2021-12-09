import disnake 
import requests
import os

from disnake import Embed
from disnake.ext import commands
from disnake.ext.commands.slash_core import slash_command


class Info(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    @commands.slash_command(name='server_info')
    async def info(self, ctx: disnake.ApplicationCommandInteraction):
        """
        Get info about the Minecraft server via an API
        """ 

        r = requests.get(f'https://mcapi.us/server/status?ip={os.getenv("MC_IP")}&port={os.getenv("MC_PORT")}').json()

        try:
            max_players = r['players']['max']
            online_players = r['players']['now']
            version = r['server']['name']
            online = r['online']
            motd = r['motd']
        except KeyError:
            await ctx.send("Something went wrong with the query! :(")
            return

        e = Embed(
            title = motd,
            description=f"Online: {online}\nPlayers: {online_players}/{max_players}\nVersion: {version}\n"
        )

        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Info(bot))