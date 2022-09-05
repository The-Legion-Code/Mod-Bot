import os
import asyncio
import discord
from discord.ext import commands
from discord.utils import maybe_coroutine


class ListCall(list):
    def append(self, rhs):
        return super().append(rhs)

    def call(self, *args, **kwargs):
        return asyncio.gather(*(maybe_coroutine(func, *args, **kwargs)
                                for func in self))

to_call = ListCall()

class ModBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix='!', **kwargs)
        self.token = kwargs.pop('token', None)
        self.client = None

    async def on_ready(self):
        print('online')
        await self.change_presence(activity=discord.Game(f'{self.command_prefix}help'))

    def starter(self):
        self.loop.run_until_complete(self.after_ready())
        self.run(self.token)

    @to_call.append
    async def loading(self):
        for cog in os.listdir('cogs'):
            if cog.endswith('.py'):
                self.load_extension(f'cogs.{cog[:-3]}')
        self.load_extension('jishaku')
        print('all cogs loaded')

    async def after_ready(self):
        await to_call.call(self)

