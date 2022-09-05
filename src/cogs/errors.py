import time
import discord
from discord.ext import commands
from helpers import utils

class errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            after = time.gmtime(error.retry_after)
            res = time.strftime('%H:%M:%S', after)
            em = discord.Embed(
                description=f'Command on cooldown\ntry again in: {res}',
                colour=discord.Colour.red())
            await ctx.send(embed=em)
            
        elif isinstance(error, commands.CommandNotFound):
            em = discord.Embed(
                    title='Command not found',
                    description=f'Command {ctx.invoked_with} not found',
                    colour=discord.Colour.red())
            await ctx.send(embed=em)

        elif isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(
                title='Error',
                description=f'Missing required argument: `{error.param.name}`',
                colour=discord.Colour.red())
            await ctx.send(embed=em)

        elif isinstance(error, commands.MissingRole):
            em = discord.Embed(
                title='Error',
                description=f'Missing required role: `{error.missing_role}`',
                colour=discord.Colour.red())
            await ctx.send(embed=em)
            
        elif isinstance(error, commands.MemberNotFound):
            em = discord.Embed(
                title='Error',
                description=f'Cannot find member: `{error.argument}`',
                colour=discord.Colour.red())
            await ctx.send(embed=em)
            
        else:
            errorEmbed = discord.Embed(
                title='An error has occured',
                description=f'idk what happened\ntraceback:\n{error}',
                colour=discord.Colour.red())
            await ctx.send(embed=errorEmbed)


def setup(bot):
    bot.add_cog(errors(bot))
