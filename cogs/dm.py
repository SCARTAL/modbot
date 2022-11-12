import discord
from discord import app_commands
from discord.ext.commands import Cog, Bot, Context, hybrid_command


# defining cog class
class DmCog(Cog):
    # rewriting init function to take a bot parameter
    def __init__(self, bot: Bot):
        self.bot = bot

    # creating a hybrid command (can be invoked by text AND slash) inside the cog
    @hybrid_command(description="Say what I tell you to say !")
    # describing the user inputs (text will be displayed when using the slash command)
    @app_commands.describe(message="The message to send")
    async def dm(self, ctx: Context, member: discord.Member, *, message: str):
        # some guard clauses to make sure everything is ok and legal :)

        # checking if the author has permissions
        if not ctx.author.guild_permissions.administrator:
            embed = discord.Embed(
                color=discord.Colour.red(), description="You do not have the permission to use this command")
            await ctx.send(embed=embed)
            return

        # trying to send the message, if failed : print the error and send a fail message
        try:
            await member.send(message)
        except Exception as exc:
            print(exc)
            embed = discord.Embed(color=discord.Color.red(
            ), description="The bot failed to send the message")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=discord.Color.blue(
            ), description="The message has been successfully sent")
            await ctx.send(embed=embed)


# the cog setup function which is used to load the cog or cogs
async def setup(bot: Bot):
    await bot.add_cog(DmCog(bot))
