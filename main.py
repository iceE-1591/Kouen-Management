from discord.ext import commands,tasks
import discord
import asyncio
from datetime import datetime

import settings

class Main(commands.Cog):

    def __init__(self,bot):
        self.bot        = bot
        self.GUILD_ID   = int(settings.GUILD_ID)
        self.CHANNEL_ID = int(settings.CHANNEL_ID)
        self.MESSAGE_ID = int(settings.MESSAGE_ID)
        self.ROLE_ID    = int(settings.ROLE_ID)
        self.ARCHIVE_ID = int(settings.ARCHIVE_ID)

        self.loop.start()

    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD   = self.bot.get_guild(self.GUILD_ID)
        self.CHANNEL = self.GUILD.get_channel(self.CHANNEL_ID)
        self.ROLE    = self.GUILD.get_role(self.ROLE_ID)
        self.ARCHIVE = self.GUILD.get_channel(self.ARCHIVE_ID)

        print("Ready")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.add_roles(self.ROLE)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return
        if payload.channel_id == self.CHANNEL_ID:
            if payload.message_id == self.MESSAGE_ID:
                await payload.member.remove_roles(self.ROLE)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if self.getMember(payload.user_id).bot:
            return
        if payload.channel_id == self.CHANNEL_ID:
            if payload.message_id == self.MESSAGE_ID:
                await self.getMember(payload.user_id).add_roles(self.ROLE)

    def getMember(self, id):
        return self.GUILD.get_member(id)

    @tasks.loop(seconds=59)
    async def loop(self):
        await self.bot.wait_until_ready()
        now = datetime.now().strftime('%H:%M')
        if now == "23:59":
            for channel in self.GUILD.text_channels:
                if channel.category == None:
                    try:
                        channel_name = int(channel.name[0:8])
                        today = int(datetime.now().strftime('%Y%m%d'))
                    except ValueError:
                        pass
                    else:
                        if channel_name <= today:
                            await channel.edit(category=self.ARCHIVE)

def setup(bot):
    return bot.add_cog(Main(bot))