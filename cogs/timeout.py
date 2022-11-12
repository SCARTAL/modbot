import discord
from discord import app_commands
from discord.ext.commands import Cog, Bot, Context, hybrid_command
from datetime import timedelta


# defining cog class
class TimeoutCog(Cog):
    # rewriting init function to take a bot parameter
    def __init__(self, bot: Bot):
        self.bot = bot

    # creating a hybrid command (can be invoked by text AND slash) inside the cog
    @hybrid_command(description="Timeout a member from in server")
    # describing the user inputs (text will be displayed when using the slash command)
    @app_commands.describe(member="A member to timeout", day="The amount of days", hour="The amount of hours", minute="The amount of minutes")
    async def timeout(self, ctx: Context, member: discord.Member, day: int = 0, hour: int = 0, minute: int = 0):
        # some guard clauses to make sure everything is ok and legal :)

        # checking if the bot has permissions
        if not ctx.me.guild_permissions.moderate_members:
            embed = discord.Embed(
                color=discord.Colour.red(), description="I do not have the permission to timeout anyone :)")
            await ctx.send(embed=embed)
            return

        # checking if the author has permissions
        if not ctx.author.guild_permissions.moderate_members:
            embed = discord.Embed(
                color=discord.Colour.red(), description="You do not have the permission to use this command")
            await ctx.send(embed=embed)
            return

        # checking if the author has the permission to timeout the member
        if not has_higher_role(ctx.author, member):
            embed = discord.Embed(
                color=discord.Colour.red(), description=f"You do not have the permission to timeout {member}")
            await ctx.send(embed=embed)
            return

        # checking if the member is not the owner :)
        if member is ctx.guild.owner:
            embed = discord.Embed(
                color=discord.Colour.red(), description=f"You and me both do not have the permission to timeout the owner of the server :)")
            await ctx.send(embed=embed)
            return

        # checking if the bot can timeout the member
        if has_higher_role(member, ctx.me):
            embed = discord.Embed(
                color=discord.Colour.red(), description=f"I do not have the permission to timeout {member}")
            await ctx.send(embed=embed)
            return

        # checking if the author did input a time
        if not day and not hour and not minute:
            embed = discord.Embed(
                color=discord.Colour.red(), description=f"You need to specifie a time to timeout {member}")
            await ctx.send(embed=embed)
            return

        # creating the timedelta object
        time = timedelta(days=day, hours=hour, minutes=minute)

        # creating the max timeout timedelta object
        limit_time = timedelta(days=28)

        # checking if the author's requested time did not exceed the max limit if so : we change it to the limit
        if time > limit_time:
            time = limit_time

        # finaly timeouting the member
        await member.timeout(time, reason=f"By {ctx.author}")
        embed = discord.Embed(color=discord.Colour.green(
        ), description=f"{member} has been successfully timeouted for `{day}` days and `{hour}` hours and `{minute}` minutes in the server")
        await ctx.send(embed=embed)

    # creating a hybrid command (can be invoked by text AND slash) inside the cog

    @hybrid_command(description="Untimeout a member from in server")
    # describing the user inputs (text will be displayed when using the slash command)
    @app_commands.describe(member="A member to untimeout", reason="The reason for this action, will be displayed in logs")
    async def untimeout(self, ctx: Context, member: discord.Member, *, reason: str = None):
        # some guard clauses to make sure everything is ok and legal :)

        # checking if the bot has permissions
        if not ctx.me.guild_permissions.moderate_members:
            embed = discord.Embed(
                color=discord.Colour.red(), description="I do not have the permission to untimeout anyone :)")
            await ctx.send(embed=embed)
            return

        # checking if the author has permissions
        if not ctx.author.guild_permissions.moderate_members:
            embed = discord.Embed(
                color=discord.Colour.red(), description="You do not have the permission to use this command")
            await ctx.send(embed=embed)
            return

        # checking if the member is in timeout
        if not member.is_timed_out():
            embed = discord.Embed(
                color=discord.Colour.red(), description=f"No need for untimeout, {member} is not in timeout")
            await ctx.send(embed=embed)
            return

        # untimeouting the member
        await member.timeout(None, reason=f"{reason} | {ctx.author}")
        embed = discord.Embed(color=discord.Colour.green(
        ), description=f"{member} has been successfully untimeouted in the server")
        await ctx.send(embed=embed)


# a small function to check is member1 has a higher role than member2, if not : he can't kick member2
def has_higher_role(member1: discord.Member, member2: discord.Member):
    return member1.top_role.position > member2.top_role.position


# the cog setup function which is used to load the cog or cogs
async def setup(bot: Bot):
    await bot.add_cog(TimeoutCog(bot))
