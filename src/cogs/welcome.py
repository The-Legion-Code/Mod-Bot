import discord
from discord.ext import commands

from helpers import utils


class tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
        em = discord.Embed(
            description=
            f'{member.mention}, welcome to {member.guild}'
        )
        created = await utils.time_formatter(member.created_at)
        em.set_thumbnail(url=member.avatar_url)
        em.add_field(name='Current member count',
                     value=member.guild.member_count,
                     inline=False)
        em.add_field(name='Account created', value=created)
        channel = discord.utils.get(member.guild.text_channels, name='welcome')
        await channel.send(embed=em)
        await member.send(embed=em)


def setup(bot):
    bot.add_cog(tasks(bot))
