from discord.ext import commands,tasks
import discord
import asyncio
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random
import re
import locale

import settings

class Main(commands.Cog):

    def __init__(self,bot):
        self.bot        = bot
        self.GUILD_ID   = int(settings.GUILD_ID)
        self.CHANNEL_ID = int(settings.CHANNEL_ID)
        self.MESSAGE_ID = int(settings.MESSAGE_ID)
        self.ROLE_ID    = int(settings.ROLE_ID)
        self.ARCHIVE_ID = int(settings.ARCHIVE_ID)
        self.VC_ID      = int(settings.VC_ID)

        self.loop.start()

    @commands.Cog.listener()
    async def on_ready(self):
        self.GUILD   = self.bot.get_guild(self.GUILD_ID)
        self.CHANNEL = self.GUILD.get_channel(self.CHANNEL_ID)
        self.ROLE    = self.GUILD.get_role(self.ROLE_ID)
        self.ARCHIVE = self.GUILD.get_channel(self.ARCHIVE_ID)
        self.VC      = self.GUILD.get_channel(self.VC_ID)

        locale.setlocale(locale.LC_ALL, '')
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

    @commands.command()
    async def random(self, ctx):
        members = self.VC.members
        if len(members) <= 10:
            await ctx.send("参加者が10人以下の場合は実行できません。")
        members = list(filter(lambda member: not member.bot, members))
        if len(members) > 10:
            members = random.sample(members, 10)
        await ctx.send("今回の参加者"+"\n"+"\n".join(list(map(lambda member: member.name, members))))

    @commands.command()
    async def create(self, ctx, date, start, end, *txt):
        date  = self.get_num(date)
        start = self.get_num(start)
        end   = self.get_num(end)
        now   = datetime.now().strftime('%Y%m%d')
        dt = datetime.strptime(date, '%Y%m%d')
        if len(date) == 8 and int(now) <= int(date) <= int(now) + 300:
            if len(start) == 4 and len(end) == 4:
                channel = await ctx.guild.create_text_channel(name=f"{date}{dt.strftime('%a')}_amongus")
                text = ""
                for i in txt:
                    text += i + "\n"
                msg = await channel.send(f"{ctx.guild.get_role(774631842770845717).mention}\n{dt.strftime('%Y/%m/%d(%a)')}\n{start[0:2]}:{start[2:4]}-{end[0:2]}:{end[2:4]}\n{text}")
                await msg.add_reaction("<:sanka:806135697513381900>")
                await msg.add_reaction("<:kikisen:806135784839053373>")
        else:
            self.send_msg(ctx, "開催日は今日から3ヵ月以内に設定してください")







    def get_num(self, nums):
        return re.sub("\D", "", nums)

    async def send_msg(self, ctx, msg):
        m = await ctx.send(msg)
        asyncio.sleep(5)
        m.delete()

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