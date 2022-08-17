from discord.ext import commands
import discord
from database import Database, OutputChannel
import asyncio
import json

class Commands(commands.Cog):
  def __init__(self, bot):
    self.bot: discord.Bot = bot
    self.db: Database = Database()

  @commands.command()
  @commands.is_owner()
  async def register(self, ctx: commands.Context, ch_type: str = None):
    if ch_type == None:
      return await ctx.send(":octagonal_sign: Please enter the channel type. Example `+register personal`")

    elif ch_type.lower() == "input":
      res = self.db.add_input_channel(ctx.channel.id)
      if not res:
        return await ctx.send(":octagonal_sign: This channel is already registered.")
      return await ctx.send(":white_check_mark: Successfully registered this channel as input channel")

    channel = OutputChannel(guild_id = ctx.guild.id, channel_id = ctx.channel.id, channel_type = ch_type)

    if not self.db.validate_channel(ctx.channel.id):
      return await ctx.send(":octagonal_sign: This channel is already registered.")

    self.db.add_channel(channel)
    await ctx.send(f":white_check_mark: Successfully registered {ctx.channel.mention} as **{ch_type}** channel..!")

  @commands.command()
  @commands.is_owner()
  async def delete(self, ctx: commands.Context, id: int):
    self.db.delete_channel(id)
    return await ctx.send(":white_check_mark: Successfully deleted channel.")

  @commands.command()
  @commands.is_owner()
  async def deregister(self, ctx: commands.Context):
    with open("data/channels.json", "r") as f:
      data = json.load(f)
    if str(ctx.channel.id) not in data["channels"]:
      return await ctx.send("This channel isn't registered as input channel.")
    data["channels"].remove(str(ctx.channel.id))
    with open("data/channels.json", "w") as f:
      json.dump(data, f)
    await ctx.send("Successfully de-registered this channel.")

  @commands.command()
  @commands.is_owner()
  async def list(self, ctx: commands.Context):
    channels = self.db.fetch_channels()
    
    embeds = []
    counter = 0
    fields = []

    for channel in channels:
      fields.append((
        f"Channel ID: {channel.id}",
        f"> Guild: `{self.bot.get_guild(channel.guild_id).name}` \n> Channel: `{self.bot.get_guild(channel.guild_id).get_channel(channel.channel_id).name}` \n> Type: `{channel.channel_type}`"
      ))

      counter += 1
      if counter == 5 or channel == channels[-1]:
        embed = discord.Embed(
          title = "Registered Channels:",
          color=discord.Color.gold()
        )
        for name, value in fields:
          embed.add_field(name=name, value=value, inline=False)
        embeds.append(embed)
        counter = 0
        fields.clear()

    current_em = 0
    reactions = ["⏪","◀️","▶️","⏩"]

    if not embeds:
      return await ctx.send("No channels found.")

    msg = await ctx.reply(embed=embeds[current_em].set_footer(text=f"Page {current_em+1}/{len(embeds)}"))

    for r in reactions:
        await msg.add_reaction(r)

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in reactions

    timed_out = False
    while not timed_out:
      try:

        reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout = 120)

        if str(reaction.emoji) == reactions[0]:
            current_em = 0
            await msg.edit(embed=embeds[current_em].set_footer(text=f"Page {current_em+1}/{len(embeds)}"))
            await msg.remove_reaction(reaction.emoji, user)

        elif str(reaction.emoji) == reactions[1]:
            if current_em != 0:
                current_em -= 1
                await msg.edit(embed=embeds[current_em].set_footer(text=f"Page {current_em+1}/{len(embeds)}"))
            await msg.remove_reaction(reaction.emoji, user)

        elif str(reaction.emoji) == reactions[2]:
            if current_em != len(embeds)-1:
                current_em += 1
                await msg.edit(embed=embeds[current_em].set_footer(text=f"Page {current_em+1}/{len(embeds)}"))
            await msg.remove_reaction(reaction.emoji, user)

        elif str(reaction.emoji) == reactions[3]:
            current_em = len(embeds)-1
            await msg.edit(embed=embeds[current_em].set_footer(text=f"Page {current_em+1}/{len(embeds)}"))
            await msg.remove_reaction(reaction.emoji, user)

      except asyncio.TimeoutError:
          await msg.clear_reactions()
          timed_out = True

  @commands.command()
  async def avatar(self, ctx: commands.Command):
    await ctx.send(embed=discord.Embed(
      title="avatar"
    ).set_image(url=ctx.author.avatar.url))


def setup(bot):
  bot.add_cog(Commands(bot))