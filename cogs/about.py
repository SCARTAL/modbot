import discord
from discord.ext.commands import Cog, hybrid_command, Bot, Context


class MyCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @hybrid_command()
    async def about(self, ctx: Context):
        embed = discord.Embed(color=discord.Color.blue(),
                              title=f"About {self.bot.user.name}")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/680505880696848555/810455033719029760/sector-team.png")
        embed.add_field(name="Developed by :",
                        value="This bot made by `SCARTAL#2825` from [SECTOR Team](https://discord.gg/ERCvnAMVmX)", inline=False)
        embed.add_field(name="Developed with :",
                        value="This bot is made using python/discord.py library V 2.0", inline=False)
        embed.add_field(
            name="Github :", value="This bot is open source and available on [github](https://github.com/SCARTAL/modbot), you can use it to build your bot for your server", inline=False)
        embed.add_field(
            name="Contact us :", value="If you encountered a problem or a question or you just needed to contact me for some other reason; you can contact me via my dm (`SCARTAL#2825`) or my [discord server](https://discord.gg/ERCvnAMVmX)", inline=False)
        embed.set_footer(text=f"Version : {self.bot.version}")
        await ctx.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(MyCog(bot))
