import discord
from discord import app_commands
from discord.ext.commands import Cog, Bot, Context, hybrid_command


# defining cog class
class BanCog(Cog):
    # rewriting init function to take a bot parameter
    def __init__(self, bot: Bot):
        self.bot = bot

    # creating a hybrid command (can be invoked by text AND slash) inside the cog
    @hybrid_command(description="Ban a member from the server")
    # describing the user inputs (text will be displayed when using the slash command)
    @app_commands.describe(member="A member to ban", reason="The reason for this action, will be displayed in logs")
    async def ban(self, ctx: Context, member: discord.Member, *, reason: str = None):
        # some guard clauses to make sure everything is ok and legal :)

        # checking if the bot has permissions
        if not ctx.me.guild_permissions.ban_members:
            embed = discord.Embed(
                color=discord.Colour.red(), description="I do not have the permission to ban anyone :)")
            await ctx.send(embed=embed)
            return

        # checking if the author has permissions
        if not ctx.author.guild_permissions.ban_members:
            embed = discord.Embed(
                color=discord.Colour.red(), description="You do not have the permission to use this command")
            await ctx.send(embed=embed)
            return

        # checking if the author has the permission to ban the member
        if not has_higher_role(ctx.author, member):
            embed = discord.Embed(
                color=discord.Colour.red(), description=f"You do not have the permission to ban {member}")
            await ctx.send(embed=embed)
            return

        # checking if the member is not the owner :)
        if member is ctx.guild.owner:
            embed = discord.Embed(
                color=discord.Colour.red(), description=f"You and me both do not have the permission to ban the owner of the server :)")
            await ctx.send(embed=embed)
            return

        # checking if the bot can ban the member
        if has_higher_role(member, ctx.me):
            embed = discord.Embed(
                color=discord.Colour.red(), description=f"I do not have the permission to ban {member}")
            await ctx.send(embed=embed)
            return

        # finaly banning the member
        await member.ban(reason=f"{reason} | {ctx.author}")
        embed = discord.Embed(color=discord.Colour.green(
        ), description=f"{member} has been successfully banned from the server with reason : {reason}")
        await ctx.send(embed=embed)

    # creating a hybrid command (can be invoked by text AND slash) inside the cog

    @hybrid_command(description="Ban a member from the server")
    # describing the user inputs (text will be displayed when using the slash command)
    @app_commands.describe(user="A user to unban", reason="The reason for this action, will be displayed in logs")
    async def unban(self, ctx: Context, user: discord.User, *, reason: str = None):
        # some guard clauses to make sure everything is ok and legal :)

        # checking if the bot has permissions
        if not ctx.me.guild_permissions.ban_members:
            embed = discord.Embed(
                color=discord.Colour.red(), description="I do not have the permission to ban anyone :)")
            await ctx.send(embed=embed)
            return

        # checking if the author has permissions
        if not ctx.author.guild_permissions.ban_members:
            embed = discord.Embed(
                color=discord.Colour.red(), description="You do not have the permission to use this command")
            await ctx.send(embed=embed)
            return

        # checking if the bot can unban the member
        if not ctx.me.guild_permissions.ban_members:
            embed = discord.Embed(
                color=discord.Colour.red(), description=f"I do not have the permission to unban {user}")
            await ctx.send(embed=embed)
            return

        # finaly unbanning the member
        # we use try and except to catch not found error
        try:
            await ctx.guild.unban(user, reason=f'{reason} | {ctx.author}')
        except discord.errors.NotFound:
            embed = discord.Embed(color=discord.Colour.red(
            ), description=f"{user} was not found in banned list")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=discord.Colour.green(
            ), description=f"{user} has been successfully banned from the server with reason : {reason}")
            await ctx.send(embed=embed)


# a small function to check is member1 has a higher role than member2, if not : he can't ban member2
def has_higher_role(member1: discord.Member, member2: discord.Member):
    return member1.top_role.position > member2.top_role.position


# the cog setup function which is used to load the cog or cogs
async def setup(bot: Bot):
    await bot.add_cog(BanCog(bot))
