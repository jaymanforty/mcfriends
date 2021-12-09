import disnake 

from disnake.ext import commands
from disnake import Member
from disnake.ext.commands.slash_core import slash_command

class Hello(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self._last_member = None


    @commands.command(name="hello")
    async def hello(self, ctx, *, member: Member = None):
        """Says Hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}')
        else:
            await ctx.send(f'Hello {member.name}... This feels familiar.')
        self._last_member = member


    @commands.slash_command(description="Says Hello!", name="hello")
    async def slash_hello(self, ctx: disnake.ApplicationCommandInteraction, member: Member = None):
        """Says hello but with slash command!"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}')
        else:
            await ctx.send(f'Hello {member.name}... This feels familiar.')
        self._last_member = member


def setup(bot):

    bot.add_cog(Hello(bot))