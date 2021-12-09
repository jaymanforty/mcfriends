import disnake 

from disnake import Embed
from disnake.ext import commands
from disnake import Member
from disnake.ext.commands.slash_core import slash_command


class Ticks(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.slash_command(name="tick_convert", description="Convert Minecraft ticks to minutes/hours")
    async def ticks(    
        self, 
        ctx: disnake.ApplicationCommandInteraction, 
        ticks: int
        ):
        """
        Command to convert minecraft ticks to a comprehensive time
        
        
        Paramaters
        ----------
        ticks: The ticks you want to convert
        """

        # there are .05 seconds in one tick for minecraft meaning 1 second = 20 ticks
        seconds = ticks * .05
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)

        e = Embed(title = f"{ticks} *ticks* = {int(h)}h{int(m)}m{int(s)}s")

        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Ticks(bot))