import asyncio
import discord
import humanize
from helpers import utils
from typing import Optional
from discord.ext import commands

class mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='lock/unlock (toggles) a channel')
    @commands.cooldown(1,3,commands.BucketType.user)
    @commands.has_guild_permissions(manage_channels=True)
    async def lock(self,ctx):
      channel = ctx.channel
      if (channel.overwrites[ctx.guild.default_role].send_messages == True
            or channel.overwrites[ctx.guild.default_role].send_messages is None):
        overwrites = channel.overwrites[ctx.guild.default_role]
        overwrites.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites, reason = f'action requested by {ctx.author.id}')
        em = discord.Embed(
                title='Channel locked',
                colour=discord.Colour.red())
        await ctx.send(embed=em)

      elif (channel.overwrites[ctx.guild.default_role].send_messages == False
          or channel.overwrites[ctx.guild.default_role].send_messages is None):
        overwrites = channel.overwrites[ctx.guild.default_role]
        overwrites.send_messages = None
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites, reason = f'action requested by {ctx.author.id}')
        em = discord.Embed(
                title='Channel unlocked',
                colour=discord.Colour.green())
        await ctx.send(embed=em)

    @commands.command(description='add/remove a role of a member')
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_role('staff')
    @commands.has_permissions(manage_roles=True)
    async def role(self,
                   ctx,
                   member: discord.Member = None,
                   role: discord.Role = None):
        if not member:
            await ctx.send('Please specify a (valid) member')
            return
        if not role:
            await ctx.send('Please specify a (valid) role')
            return
        if role in member.roles:
            await member.remove_roles(role)
            em = discord.Embed(
                description=f'Removed role {role.mention} from {member.mention}'
            )
        else:
            await member.add_roles(role)
            em = discord.Embed(
                description=f'Added role {role.mention} to {member.mention}')
        await ctx.send(embed=em)


    @commands.command(description='kick someone')
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_role('staff')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if not member:
            await ctx.send('Please specify a (valid) member')
            return
        try:
            await member.kick(
                reason=f'{reason} - action requested by {ctx.author.id}')
        except commands.BotMissingPermissions:
            await ctx.send('Couldn\'t kick member')
            return
        kick = discord.Embed(
            description=f'{member.mention} has  been kicked by {ctx.author.mention}\nReason: {reason}',
            colour=discord.Colour.red())
        kick.set_author(
            name=f'{ctx.author.name}#{ctx.author.discriminator}',
            icon_url=ctx.author.avatar_url)
        await ctx.send(embed=kick)

    @commands.command(description='ban someone')
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_role('staff')
    @commands.has_permissions(ban_members=True)
    async def ban(self,
                  ctx,
                  member: discord.Member,
                  delete: Optional[int],
                  *,
                  reason=None):
        if not member:
            await ctx.send('Please specify a (valid) member')
            return
        try:
            if isinstance(delete, int):
                await member.ban(
                    reason=f'{reason} - action requested by {ctx.author.id}',
                    delete_message_days=delete)
            else:
                await member.ban(
                    reason=f'{reason} - action requested by {ctx.author.id}'
                )
        except commands.BotMissingPermissions:
            await ctx.send('Couldn\'t ban member')
            return
        ban = discord.Embed(
            description=f'{member.mention} has  been banned by {ctx.author.mention}\nReason: {reason}',
            colour=discord.Colour.red())
        ban.set_author(
            name=f'{ctx.author.name}#{ctx.author.discriminator}',
            icon_url=ctx.author.avatar_url)
        await ctx.send(embed=ban)

    @commands.command(description='unban someone')
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_role('staff')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.Object, *, reason=None):
        await ctx.guild.unban(
            user, reason=f'{reason} - action requested by {ctx.author.id}')
        ban = discord.Embed(
            description=f'User `{user.id}` has been unbanned by {ctx.author.mention}\nReason: {reason}',
            colour=discord.Colour.green())
        ban.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}',
                       icon_url=ctx.author.avatar_url)
        await ctx.send(embed=ban)

    @commands.command(description='set a slowmode')
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_role('staff')
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        if not seconds and seconds != 0:
            await ctx.send('Please specify a slomode time')
            return
        await ctx.channel.edit(slowmode_delay=seconds,
                               reason=f'action requested by {ctx.author.id}')
        embed = discord.Embed(
            description=f'{ctx.author.mention} set a {seconds} second slowmode for {ctx.channel.mention}',
            colour=discord.Colour.blue())
        embed.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}',
                         icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)

    @commands.command(description='purge messages')
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_role('staff')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = None):
        if not amount:
            await ctx.message.reply('Must specify amount')
            return
        purged = await ctx.channel.purge(limit=amount + 1)
        purge = discord.Embed(
            description=f'{ctx.author.mention} has purged {len(purged)-1} messages in {ctx.channel.mention}',
            colour=discord.Colour.blue())
        purge.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}',
                         icon_url=ctx.author.avatar_url)
        await ctx.send(embed=purge)

    @purge.error
    async def purgeerror(self, ctx, error):
        pass

    @commands.command(description='mute a member\nformat: [time][duration type]\nif you run the command without passing a duration type, it is minutes by default\nif you run the command without passing a time & duration type, it 5 minutes by default\n```s - seconds\nm - minutes\nh - hours\nd - days\nw - weeks```\n note: you can\'t do something like 3w4d, you need to do 25d\nalso no space :)')
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_role('staff')
    async def mute(self,
                   ctx,
                   member: discord.Member,
                   duration: Optional[str] = '5m',
                   *,
                   reason=None):
        if not member:
            await ctx.send('Please specify a (valid) member')
            return
        duration = await utils.time_converter(duration)
        if duration == 0:
            await member.add_roles(
                discord.utils.get(ctx.guild.roles,name='muted'),
                reason=f'{reason} - action requested by {ctx.author.id}')
            muteEmbed = discord.Embed(
                description=f'{member.mention} has been muted by {ctx.author.mention}\nTime: forever\nReason: {reason}',
                colour=discord.Colour.red())
            muteEmbed.set_author(
                name=f'{ctx.author.name}#{ctx.author.discriminator}',
                icon_url=ctx.author.avatar_url)
            await ctx.send(embed=muteEmbed)
            return
        if duration < 0:
            await ctx.send('Duration must be positive')
            return
        await member.add_roles(
            discord.utils.get(ctx.guild.roles,name='muted'),
            reason=f'{reason} - action requested by {ctx.author.id}')
        muteEmbed = discord.Embed(
            description=f'{member.mention} has been muted by {ctx.author.mention}\nTime: {humanize.precisedelta(duration)}\nReason: {reason}',
            colour=discord.Colour.red())
        muteEmbed.set_author(
            name=f'{ctx.author.name}#{ctx.author.discriminator}',
            icon_url=ctx.author.avatar_url)
        await ctx.send(embed=muteEmbed)
        await asyncio.sleep(duration)
        if 'muted' in [role.name for role in member.roles]:
            reason = f'automatic unmute after {humanize.precisedelta(duration)}'
            await member.remove_roles(
                discord.utils.get(ctx.guild.roles,name='muted'),
                reason=reason)
            embed = discord.Embed(
                description=f'{member.mention} has been unmuted by {self.bot.user.mention}\nReason: {reason}',
                colour=discord.Colour.green())
            await ctx.send(embed=embed)
        current_roles = []

    @commands.command(description='unmute a member')
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_role('staff')
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        if not member:
            await ctx.send('Please specify a (valid) member')
            return
        await member.remove_roles(
            discord.utils.get(ctx.guild.roles,name='muted'),
            reason=f'{reason} - action requested by {ctx.author.id}')
        muteEmbed = discord.Embed(
            description=f'{member.mention} has been unmuted by {ctx.author.mention}\nReason: {reason}',
            colour=discord.Colour.green())
        muteEmbed.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}',
                             icon_url=ctx.author.avatar_url)
        await ctx.send(embed=muteEmbed)

    @commands.command(description='change a members nickname',
                      aliases=['nick'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_role('staff')
    @commands.has_guild_permissions(manage_nicknames=True)
    async def nickname(self, ctx, member: discord.Member, *, nickname):
        if not member:
            await ctx.send('Please specify a (valid) member')
            return
        await member.edit(nick=nickname,
                          reason=f'action requested by {ctx.author.id}')
        nick = discord.Embed(
            description=f'{member}\'s nickname has been changed to {nickname}',
            colour=discord.Colour.red())
        nick.set_author(
            name=f'{ctx.author.name}#{ctx.author.discriminator}',
            icon_url=ctx.author.avatar_url)
        await ctx.send(embed=nick)


def setup(bot):
    bot.add_cog(mod(bot))
