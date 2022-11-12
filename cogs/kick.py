import discord
from discord import app_commands
from discord.ext.commands import Cog, Bot, Context, hybrid_command


# defining cog class
class KickCog(Cog):
    # rewriting init function to take a bot parameter
    def __init__(self, bot: Bot):
        self.bot = bot

    # creating a hybrid command (can be invoked by text AND slash) inside the cog
    @hybrid_command(description="Kick a member from the server")
    # describing the user inputs (text will be displayed when using the slash command)
    @app_commands.describe(member="A member to kick", reason="The reason for this action, will be displayed in logs")
    async def kick(self, ctx: Context, member: discord.Member, reason: str = None):
        # some guard clauses to make sure everything is ok and legal :)

        # checking if the bot has permissions
        if not ctx.me.guild_permissions.kick_members:
            embed = discord.Embed(
                color=discord.Colour.red(), description="I do not have the permission to kick anyone :)")
            await ctx.send(embed=embed)
            return

        # checking if the author has permissions
        if not ctx.author.guild_permissions.kick_members:
            embed = discord.Embed(
                color=discord.Colour.red(), description="You do not have the permission to use this command")
            await ctx.send(embed=embed)
            return

        # checking if the author has the permission to kick the member
        if not has_higher_role(ctx.author, member):
            embed = discord.Embed(
                color=discord.Colour.red(), description=f"You do not have the permission to kick {member}")
            await ctx.send(embed=embed)
            return

        # checking if the member is not the owner :)
        if member is ctx.guild.owner:
            embed = discord.Embed(
                color=discord.Colour.red(), description=f"You and me both do not have the permission to kick the owner of the server :)")
            await ctx.send(embed=embed)
            return

        # checking if the bot can kick the member
        if has_higher_role(member, ctx.me):
            embed = discord.Embed(
                color=discord.Colour.red(), description=f"I do not have the permission to kick {member}")
            await ctx.send(embed=embed)
            return

        # finaly kicking the member
        await member.kick(reason=f"{reason} | {ctx.author}")
        embed = discord.Embed(color=discord.Colour.green(
        ), description=f"{member} has been successfully kicked from the server with reason : {reason}")
        await ctx.send(embed=embed)


# a small function to check is member1 has a higher role than member2, if not : he can't kick member2
def has_higher_role(member1: discord.Member, member2: discord.Member):
    return member1.top_role.position > member2.top_role.position


# the cog setup function which is used to load the cog or cogs
async def setup(bot: Bot):
    await bot.add_cog(KickCog(bot))
