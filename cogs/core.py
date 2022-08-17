from discord.ext import commands
import discord

from database import Database

class Core(commands.Cog):
  def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.db: Database = Database()
        self.cache = {}

  @commands.Cog.listener()
  async def on_message(self, msg: discord.Message):
    if msg.author == self.bot.user:
      return
    

  # def create_embed(self, msg: discord.Message) -> discord.Embed:
  #   embed = discord.Embed(title="New deal detected..!", description=msg.content, color=discord.Color.random(),
  #             timestamp=datetime.now())
  #   if msg.attachments:
  #     embed.set_image(url=msg.attachments[0].url)
  #   embed.set_footer(text="Deal provided by CrystalStar#5396")
  #   return embed

    if not self.db.check_input_channel(msg.channel.id):
      return
    
    await msg.add_reaction("✅")
    def check(reaction, user):
        return str(reaction.emoji) == "✅" and user != self.bot.user
    reaction, user = await self.bot.wait_for("reaction_add", check=check)
      

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
    if not str(payload.emoji) == "✅" or payload.user_id == self.bot.user.id:
      return

    guild = self.bot.get_guild(payload.guild_id)
    che = guild.get_channel(payload.channel_id)
    channels = self.db.get_channel_by_type(che.name.split("-")[0] or che.name)
    msg = self.bot.get_message(payload.message_id)

    if len(channels) == 0:
      return await che.send(f"No channels registered for `{che.name}`")

    self.cache[msg.id] = []

    await che.send(f":white_check_mark: Sending deal to {len(channels)} channels")
    for channel in channels:
      try:
        ch = self.bot.get_guild(channel.guild_id).get_channel(channel.channel_id)
        sent = await ch.send(msg.content, files=[await attachment.to_file() for attachment in msg.attachments] if msg.attachments else None)
        await msg.channel.send(f"Sent deal to `{ch.name}` in `{self.bot.get_guild(channel.guild_id).name}`")

        if len(self.cache.items()) >= 10:
          self.cache.pop(list(self.cache.keys())[0])
        self.cache[msg.id].append(sent.id)
      except Exception as e:
        await che.send(e)

  @commands.Cog.listener()
  async def on_message_edit(self, before: discord.Message, after: discord.Message):
    try:
      if before.id in self.cache:
        for msg_id in self.cache[before.id]:
          msg = self.bot.get_message(msg_id)
          await msg.edit(content=after.content)
    except Exception as e:
      await before.channel.send(e)


  @commands.command()
  async def cache(self, ctx:commands.Context):
    await ctx.send(self.cache)


def setup(bot):
    bot.add_cog(Core(bot))