from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            return await ctx.send(f"You are missing the {error.missing_roles} role")
        
        # elif isinstance(error, commands.MissingRequiredArgument):
        #     return await ctx.send(f"Please pass in the `{error.param}` argument. (`+help` for more help)")

        else:
            return await ctx.send(error)

def setup(bot):
    bot.add_cog(Utility(bot))