import discord
from discord.ext.commands import Bot, Context
import os
import json

# loading our config file
with open("config.json", "r", encoding='utf-8') as data:
    config = json.load(data)


# creating our bot class
class ModBot(Bot):
    # The Mod Bot version (this is not required for running a bot)
    version = "1.0.0"

    # rewriting the setup hook to load our cogs

    async def setup_hook(self):
        # taking all filenames at cogs folder
        for filename in os.listdir('cogs/'):
            # checking if it's a python file
            if filename.endswith('.py'):
                # trying to load the cog if not display the error
                try:
                    await self.load_extension(name=f'cogs.{filename[:-3]}')
                except Exception as exc:
                    print(f'Failed to load {filename[:-3]} cog')
                    print(f'Error :\n{exc}')
                else:
                    print(f'{filename[:-3]} cog has been loaded successfully')

    # rewriting the on ready to print when the bot caches is ready

    async def on_ready(self):
        print("-" * 100)
        print(f"{self.user.name} is ready")
        print(f"ID : {self.user.id} | Version : {self.version}")


# create a default intent object with the default privileges
intents = discord.Intents.default()
# setting members privilege to True
intents.members = True
# setting message content privilege to True (if you don't want to text command to work you can remove it)
intents.message_content = True


# creating our bot object
bot = ModBot(command_prefix=config["bot_prefix"], intents=intents)


# creating the sync command (to sync the bot app commands)
@bot.hybrid_command()
async def sync_commands(ctx: Context):
    # checking if the author has permissions to use the command
    if not ctx.author.guild_permissions.administrator:
        embed = discord.Embed(color=discord.Color.red(
        ), description="You do not have the permission to use this command")
        await ctx.send(embed=embed)
        return
    # syncing the bot commands
    await ctx.bot.tree.sync()
    embed = discord.Embed(color=discord.Color.blue(
    ), description="Bot commands has been successfully synced")
    await ctx.send(embed=embed)

# running the bot
bot.run(config["bot_token"], reconnect=True)
