import discord
import asyncio
from discord.ext import commands

async def create_pool(bot):
    return starboard(bot)


class starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cache = {}
        self.sent = []


    async def on_ready(self):
        asyncio.run(create_pool(self.bot))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, member):
        channel_name = reaction.message.channel.name
        msg_id = reaction.message.id
        if channel_name == 'starboard' or str(reaction.emoji) != '⭐':
            return

        try:
            self.cache[str(msg_id)] += 1
        except KeyError:
            self.cache[str(msg_id)] = 1

        if self.cache[str(msg_id)] >= 1:
            channel = discord.utils.get(member.guild.text_channels, name=channel_name)
            msg = await channel.fetch_message(msg_id)
            await self.send_star(discord.utils.get(member.guild.text_channels, name='starboard'), msg)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, member):
        msg_id = reaction.message.id
        if str(reaction.emoji) != '⭐':
            return
        self.cache[str(msg_id)] -= 1

    async def send_star(self, channel, message: discord.Message):
        if message.id in self.sent:
            return
        em = discord.Embed(
            description=
            f'[**Click to see message**]({message.jump_url})\n{message.content}',
            timestamp=message.created_at)
        em.set_author(
            name=f'{message.author.name}#{message.author.discriminator}',
            icon_url=message.author.avatar_url)
        if message.attachments:
            file = message.attachments[0]
            if 'image' in file.content_type:
                em.set_image(url=file)
        msg = await channel.send(content=f'⭐ | {message.channel.mention}',
                                 embed=em)
        await msg.add_reaction('⭐')
        self.sent.append(message.id)


def setup(bot):
    bot.add_cog(starboard(bot))
