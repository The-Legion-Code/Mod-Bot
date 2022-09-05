import discord
from discord.ext import commands

from helpers import utils


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='get the info for the server')
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def serverinfo(self, ctx):
        em = discord.Embed(
            title='Server info',
            description=
            'note that some things might be slighty inaccurate due to cache')
        created = await utils.time_formatter(ctx.guild.created_at)
        em.add_field(name='Owner', value=ctx.guild.owner)
        em.add_field(name='Name', value=ctx.guild.name)
        em.add_field(name='Server created', value=created)
        em.add_field(name='Roles', value=len(ctx.guild.roles))
        em.add_field(
            name='Members',
            value=
            f'Total members: {ctx.guild.member_count}\nOnline: {sum(member.status!=discord.Status.offline for member in ctx.guild.members)}\nHumans: {len([member for member in ctx.guild.members if not member.bot])}\nBots: {len([member for member in ctx.guild.members if member.bot])}'
        )
        word = await utils.grammar(len(ctx.guild.stage_channels), 'channel')
        em.add_field(
            name='Channels',
            value=
            f'{len(ctx.guild.channels)} total channels\n{len(ctx.guild.categories)} total categories\n{len(ctx.guild.text_channels)} text channels\n{len(ctx.guild.voice_channels)} voice channels\n{len(ctx.guild.stage_channels)} stage {word}'
        )
        em.set_thumbnail(url=ctx.guild.icon_url)
        em.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}',
                      icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command(description='get the info for a role')
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def roleinfo(self, ctx, role: discord.Role):
        em = discord.Embed(title='Role info')
        em.add_field(name='Role name', value=role.name)
        em.add_field(name='Role id', value=role.id)
        em.add_field(name='Members with role', value=len(role.members))
        em.add_field(name='Mentionable', value=role.mentionable)
        em.add_field(name='Displayed separately', value=role.hoist)
        em.add_field(name='Colour', value=role.colour)
        em.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}',
                      icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command(description='get the info for a user', aliases=['ui'])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        created = await utils.time_formatter(member.created_at)
        joined = await utils.time_formatter(member.joined_at)
        em = discord.Embed(title='User info')
        em.add_field(name='Name', value=member.name)
        em.add_field(name='ID', value=member.id)
        em.add_field(name='Account created', value=created)
        em.add_field(name='Joined server', value=joined)
        em.add_field(name='Nickname', value=member.nick or 'None')
        em.add_field(name='Status', value=member.status)
        em.add_field(name='Activity', value=member.activity)
        all_members = ctx.guild.members
        all_members.sort(key=lambda m: m.joined_at)
        all_members = [mem.id for mem in all_members]
        joinpos = all_members.index(member.id) + 1
        em.add_field(name='Join position', value=joinpos)
        all_members = ctx.guild.members
        all_members.sort(key=lambda m: m.created_at)
        all_members = [mem.id for mem in all_members]
        createpos = all_members.index(member.id) + 1
        em.add_field(name='Account creation position', value=createpos)
        em.set_thumbnail(url=member.avatar_url)
        em.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}',
                      icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)


def setup(bot: commands.Bot):
    bot.add_cog(info(bot))
