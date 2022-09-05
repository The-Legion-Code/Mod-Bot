from discord.ext import commands

class utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='get the bot\'s latency')
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    async def ping(self, ctx):
        latency = int(self.bot.latency * 1000)
        await ctx.send(f'🏓 pong! {latency}ms')

def setup(bot):
    bot.add_cog(utility(bot))
