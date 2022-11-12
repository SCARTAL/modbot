import discord
from discord import app_commands
from discord.ext.commands import Cog, Bot, Context, hybrid_command


# defining cog class
class RoleCog(Cog):
    # rewriting init function to take a bot parameter
    def __init__(self, bot: Bot):
        self.bot = bot

    # creating a hybrid command (can be invoked by text AND slash) inside the cog
    @hybrid_command(description="Give a role to a member in the server", aliases=['gr', 'grole'])
    # describing the user inputs (text will be displayed when using the slash command)
    @app_commands.describe(role="The role to give", member="The member to give the role to")
    async def give_role(self, ctx: Context, role: discord.Role, member: discord.Member):
        # some guard clauses to make sure everything is ok and legal :)

        # checking if the bot has permissions
        if not ctx.me.guild_permissions.manage_roles:
            embed = discord.Embed(
                color=discord.Colour.red(), description="I do not have the permission to give roles :)")
            await ctx.send(embed=embed)
            return

        # checking if the author has permissions
        if not ctx.author.guild_permissions.manage_roles:
            embed = discord.Embed(
                color=discord.Colour.red(), description="You do not have the permission to use this command")
            await ctx.send(embed=embed)
            return

        # checking if the author has the permission to give the role
        if role.position >= ctx.author.top_role.position and ctx.author is not ctx.guild.owner:
            embed = discord.Embed(
                color=discord.Colour.red(), description=f"You do not have the permission to give {role.mention} to anyone")
            await ctx.send(embed=embed)
            return

        # checking if the member does not have the role
        if role in member.roles:
            embed = discord.Embed(
                color=discord.Colour.red(), description=f"{member} already has the {role.mention} role")
            await ctx.send(embed=embed)
            return

        # finaly giving the role
        await member.add_roles(role)
        embed = discord.Embed(color=discord.Colour.green(
        ), description=f"{role.mention} has been successfully given to {member}")
        await ctx.send(embed=embed)

    # creating a hybrid command (can be invoked by text AND slash) inside the cog

    @hybrid_command(description="Take a role from a member in the server", aliases=['tr', 'trole'])
    # describing the user inputs (text will be displayed when using the slash command)
    @app_commands.describe(role="The role to take", member="The member to take the role from")
    async def take_role(self, ctx: Context, role: discord.Role, member: discord.Member):
        # some guard clauses to make sure everything is ok and legal :)

        # checking if the bot has permissions
        if not ctx.me.guild_permissions.manage_roles:
            embed = discord.Embed(
                color=discord.Colour.red(), description="I do not have the permission to take roles :)")
            await ctx.send(embed=embed)
            return

        # checking if the author has permissions
        if not ctx.author.guild_permissions.manage_roles:
            embed = discord.Embed(
                color=discord.Colour.red(), description="You do not have the permission to use this command")
            await ctx.send(embed=embed)
            return

        # checking if the author has the permission to take the role
        if role.position >= ctx.author.top_role.position and ctx.author is not ctx.guild.owner:
            embed = discord.Embed(
                color=discord.Colour.red(), description=f"You do not have the permission to take {role.mention} from anyone")
            await ctx.send(embed=embed)
            return

        # checking if the member does have the role
        if not role in member.roles:
            embed = discord.Embed(
                color=discord.Colour.red(), description=f"{member} already does not have the {role.mention} role")
            await ctx.send(embed=embed)
            return

        # finaly giving the role
        await member.remove_roles(role)
        embed = discord.Embed(color=discord.Colour.green(
        ), description=f"{role.mention} has been successfully taken from {member}")
        await ctx.send(embed=embed)


# the cog setup function which is used to load the cog or cogs
async def setup(bot: Bot):
    await bot.add_cog(RoleCog(bot))
