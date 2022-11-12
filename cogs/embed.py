import discord
from discord import app_commands
from discord.ext.commands import Cog, Bot, Context, hybrid_command

# you can set this to False if you want everyone to be able to use this command
ADMINISTRATOR_ONLY = True


# defining cog class
class EmbedCog(Cog):
    # rewriting init function to take a bot parameter
    def __init__(self, bot: Bot):
        self.bot = bot

    # creating a hybrid command (can be invoked by text AND slash) inside the cog
    @hybrid_command(description="Say what I tell you to say !")
    # describing the user inputs (text will be displayed when using the slash command)
    @app_commands.describe(message="The message to send")
    async def embed(self, ctx: Context, *, message: str):
        # some guard clauses to make sure everything is ok and legal :)

        # checking if the bot has permissions
        if not ctx.channel.permissions_for(ctx.me).send_messages:
            # we won't send error message because obviously we can't :)
            return

        # checking if the author has permissions (can be removed with the above ADMINISTRATOR_ONLY variable)
        if ADMINISTRATOR_ONLY and not ctx.author.guild_permissions.administrator:
            embed = discord.Embed(
                color=discord.Colour.red(), description="You do not have the permission to use this command")
            await ctx.send(embed=embed)
            return

        # creating the embed
        embed = discord.Embed(color=discord.Color.blue(), description=message)

        # sending the message
        await ctx.send(embed=embed)


# the cog setup function which is used to load the cog or cogs
async def setup(bot: Bot):
    await bot.add_cog(EmbedCog(bot))
