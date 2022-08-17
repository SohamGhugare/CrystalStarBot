from discord.ext import commands
from discord import Embed, Color

class CustomHelp(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.bot.remove_command('help')

  @commands.command()
  async def help(self, ctx):
    embed = Embed(
        title=":gear: Help",
        color = Color.yellow()
    )

    embed.add_field(name="`+register input`", value="Registers the channel as input channel", inline=False)
    embed.add_field(name="`+register [group]`", value="Registers the channel with the particular group \n(Example: `+register personal`)", inline=False)
    embed.add_field(name="`+delete [id]`", value="Deletes a channel from the list (Get the id of the channel from +list) \n(Example: `+delete 1`)", inline=False)
    embed.add_field(name="`+list`", value="Displays the list of all registered channels", inline=False)
    embed.add_field(name="`+deregister`", value="**(Only for input channels)** \nDe-register an input channel", inline=False)


    await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CustomHelp(bot))