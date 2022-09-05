import os
import discord
from discord.ext import commands


class ModHelp(commands.HelpCommand):
    @staticmethod
    def get_doc(command):
        return command.description or command.help or 'This command has no description'

    async def send_bot_help(self, mapping):
        ctx = self.context
        bot = ctx.bot
        cogs = sorted([
            f'`{cog[:-3]}`' for cog in os.listdir('cogs')
            if cog.endswith('.py')
        ])
        remove_ = ('`help`', '`welcome`', '`errors`', '`starboard`')
        for cog in remove_:
            cogs.remove(cog)
        commands = [f'`{cmd.name}`' for cmd in bot.commands if cmd.cog is None]
        helpEmbed = discord.Embed(
            description=
            f"cogs: {'; '.join(cogs)}\n\nType `{ctx.prefix}help [command | cog]` for more info on a cog"
        )
        helpEmbed.set_author(
            name=f'{ctx.author.name}#{ctx.author.discriminator}',
            icon_url=ctx.author.avatar_url)
        helpEmbed.set_footer(text='<> - Required & [] - Optional')
        channel = self.get_destination()
        await channel.send(embed=helpEmbed)

    async def send_cog_help(self, cog):
        ctx = self.context
        cmds = await self.filter_commands(cog.walk_commands(), sort=True)
        commands = [f'`{c.name}`' for c in cmds if not c.parent]
        helpEmbed = discord.Embed(title=f'{cog.qualified_name} commands',
                                  description='; '.join(commands))
        helpEmbed.set_footer(text='<> - Required & [] - Optional')
        helpEmbed.set_author(
            name=f'{ctx.author.name}#{ctx.author.discriminator}',
            icon_url=ctx.author.avatar_url)
        channel = self.get_destination()
        await channel.send(embed=helpEmbed)

    async def send_group_help(self, group):
        ctx = self.context
        _ = await self.filter_commands(group.commands, sort=True)
        all_subs = [f'`{cmd}`' for cmd in _]
        helpEmbed = discord.Embed(title=f'{group.qualified_name} commands',
                                  description='; '.join(list(all_subs)))
        helpEmbed.set_footer(text='<> - Required & [] - Optional')
        helpEmbed.set_author(
            name=f'{ctx.author.name}#{ctx.author.discriminator}',
            icon_url=ctx.author.avatar_url)
        channel = self.get_destination()
        await channel.send(embed=helpEmbed)

    async def send_command_help(self, command):
        ctx = self.context
        helpEmbed = discord.Embed(title='Help command')
        helpEmbed.add_field(
            name=command,
            value=
            f"{self.get_doc(command)}\n`{ctx.prefix}{command.name} {command.signature}`\naliases: {', '.join(command.aliases)}"
        )
        helpEmbed.set_footer(text='<> - Required & [] - Optional')
        helpEmbed.set_author(
            name=f'{ctx.author.name}#{ctx.author.discriminator}',
            icon_url=ctx.author.avatar_url)
        channel = self.get_destination()
        await channel.send(embed=helpEmbed)
    
    async def send_error_message(self, error):
        embed = discord.Embed(title='Error', description=error)
        channel = self.get_destination()
        await channel.send(embed=embed)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        help_command = ModHelp()
        help_command.cog = self
        bot.help_command = help_command


def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))
