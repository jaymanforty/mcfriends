import disnake 
import ftplib
import json
import requests
import os

from enum import Enum
from ftplib import FTP
from io import BytesIO
from disnake import Embed
from disnake.ext import commands
from disnake import Member
from disnake.ext.commands.slash_core import slash_command

#Enum Class used for choices since a category is required
class Category(str, Enum):
    killed_by = 'killed_by'
    killed = 'killed'
    crafted = 'crafted'
    picked_up = 'picked_up'
    mined = 'mined'
    custom = 'custom'
    used = 'used'
    dropped = 'dropped'
    broken = 'broken'

class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def get_mc_uuid(self, name: str):
        return requests.get(f'https://minecraft-api.com/api/uuid/{name}').text
    
    @commands.slash_command(name="stats")
    async def stats(
        self, 
        ctx: disnake.ApplicationCommandInteraction, 
        mc_nickname: str, 
        stat_category: Category, 
        item: str = ""):
        """
        Query stats from the minecraft server
        
        
        Parameters
        ----------
        mc_nickname: The user to query Minecraft stats for (must be exact)
        stat_category: The category of Minecraft stat you want
        item: The Minecraft item you want the stat of (must be exact)
        """
        #defer the interaction so that it gives us time to query all the data
        await ctx.response.defer()

        #Get the minecraft uuid given the nickname
        uuid = self.get_mc_uuid(mc_nickname)

        #Handle if the nickname wasn't a valid player
        if uuid.lower().replace(' ', '') == 'playernotfound!':
            await ctx.send("Player could not be found via UUID api!")
            return

        #Rebuild the UUID to have dashes to match file names on the server 
        minecraft_uuid = f'{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}.json'

        #Create connection to the minecraft ftp server
        with FTP(os.getenv('FTP_HOST')) as ftp:

            #login to the ftp server
            ftp.login(user=os.getenv('FTP_USER'), passwd=os.getenv("FTP_PSSWD"))

            #change the directory to where stats are saved for players
            ftp.cwd('world/stats')

            #create a reader object
            r = BytesIO()

            #Load the file into the reader object
            try:
                ftp.retrbinary('RETR '+minecraft_uuid, r.write)
            except ftplib.error_perm:
                await ctx.send("Player could not be found in stat files!")
                return
            
            stats = json.loads(r.getvalue())
            
        stats = stats['stats']
        

        #fix the stat_category defined by the user
        stat_category = f'minecraft:{stat_category}'

        #Handle invalid category
        try:
            stats[stat_category]
        except KeyError:
            await ctx.send("Invalid category!")
            return

        #Handle invalid item if specified
        if item:
            item = f'minecraft:{item}'
            try:
                stats[stat_category][item]
            except KeyError:
                await ctx.send("Invalid minecraft item!")
                return

        #Display the number for specific category/item otherwise display all items for specified category
        if item:
            num = stats[stat_category][f'{item}']

            #remove ugly 'minecraft:' from everything
            stat_category = stat_category.replace('minecraft:', '')
            item = item.replace('minecraft:', '')

            # send off the embed with info
            e = Embed(
                title = f'{mc_nickname} {stat_category}', 
                description = f'`{item} - {num}`'
                )


            await ctx.send(embed=e)
            return

        else:
            #Display all items for the category
            list_str = ""
            for i in stats[stat_category]:
                list_str += f'`{i} - {stats[stat_category][i]}`\n'
            
            #remove ugly 'minecraft:' from everything
            stat_category = stat_category.replace('minecraft:', '')
            list_str = list_str.replace('minecraft:', '')

            #Send the embed with info
            e = Embed(
                title =f'{mc_nickname} {stat_category}', 
                description=list_str
                )

            await ctx.send(embed=e)
            return


def setup(bot):
    bot.add_cog(Stats(bot))