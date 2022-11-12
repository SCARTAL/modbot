import discord
from discord import app_commands
from discord.ext.commands import Cog, Bot, Context, hybrid_command


# defining cog class
class ClearMessageCog(Cog):
    # rewriting init function to take a bot parameter
    def __init__(self, bot: Bot):
        self.bot = bot

    # creating a hybrid command (can be invoked by text AND slash) inside the cog
    @hybrid_command(description="Clear messages in this channel")
    # describing the user inputs (text will be displayed when using the slash command)
    @app_commands.describe(amount="The amount of meesages to clear")
    async def clear(self, ctx: Context, amount: int = 10):
        # some guard clauses to make sure everything is ok and legal :)

        # checking if the bot has permissions
        if not ctx.channel.permissions_for(ctx.me).manage_messages:
            embed = discord.Embed(
                color=discord.Colour.red(), description="I do not have the permission to delete messages :)")
            await ctx.send(embed=embed)
            return

        # checking if the author has permissions
        if not ctx.channel.permissions_for(ctx.author).manage_messages:
            embed = discord.Embed(
                color=discord.Colour.red(), description="You do not have the permission to use this command")
            await ctx.send(embed=embed)
            return

        # clearing messages
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(color=discord.Colour.green(
        ), description=f"{amount} messages has been successfully deleted")
        await ctx.send(embed=embed, delete_after=5)


# the cog setup function which is used to load the cog or cogs
async def setup(bot: Bot):
    await bot.add_cog(ClearMessageCog(bot))
