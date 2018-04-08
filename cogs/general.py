# ======================================================================
# imports
# ======================================================================
import datetime
from tzlocal import get_localzone

import psutil

import math

import discord
from discord.ext import commands as cmds

import logging
logger = logging.getLogger(__name__)


# ======================================================================
class General:
    def __init__(self, bot):
        self.bot = bot
        self.startTime = datetime.datetime.now(get_localzone())
        self.process = psutil.Process()
        self.process.cpu_percent()

    # misc functions ===================================================
    @staticmethod
    def _get_roundtrip(msg):
        return round(msg.edited_at.timestamp() - msg.created_at.timestamp(), 2)

    @staticmethod
    def _create_embed(title):
        return discord.Embed(title=title, colour=3447003)

    @staticmethod
    def _get_readable_time(first, last):
        # A helper function to make a readable string between two datetime
        delta = int((last - first).total_seconds())

        week_in_sec = 604800  # (7d*24h*60m*60s)
        day_in_sec = 86400
        hour_in_sec = 3600
        minute_in_sec = 60

        weeks = math.trunc(delta/week_in_sec)
        remainder = delta % week_in_sec
        days = math.trunc(remainder/day_in_sec)
        remainder %= day_in_sec
        hours = math.trunc(remainder/hour_in_sec)
        remainder %= hour_in_sec
        minutes = math.trunc(remainder/minute_in_sec)
        seconds = remainder % minute_in_sec

        if weeks is 0 and days is 0:
            return "{0}h {1}m {2}s".format(hours, minutes, seconds)
        elif weeks is 0:
            return "{0}d {1}h {2}m {3}s".format(days, hours, minutes, seconds)
        else:
            return "{0}w {1}d {2}h {3}m {4}s".format(weeks, days, hours, minutes, seconds)

    # ==================================================================
    @cmds.command(name="ping", aliases=["pong", "pingpong"])
    async def ping(self, ctx):
        """ Shows latency and API response times.
        usage:: ping
        details:: This command is a response test, it helps gauge if there is any latency (lag) in either the bots
        connections, or the API.
        """

        # retrieve guild config
        guild_config = next(cfg for cfg in self.bot.db.configs if cfg["guild_id"] == ctx.guild.id)

        # send 1st message as starting time
        embed = self._create_embed(guild_config["language"].cmdPing_ping)
        msg = await ctx.send(embed=embed)

        # send 2nd message as ending time
        embed = self._create_embed(guild_config["language"].cmdPing_pong)
        await msg.edit(embed=embed)

        # send 3rd message for display roundtrip time
        embed = self._create_embed(guild_config["language"].cmdPing_roundtrip.format(self._get_roundtrip(msg),
                                                                                     round(self.bot.latency, 2)))
        await msg.edit(embed=embed)

    # ==================================================================
    @cmds.command(name="serverInfo", aliases=["servInfo"])
    async def server_info(self, ctx):
        """ Displays server information & statistics.
        usage:: server_info
        details:: This command will return an organised embed with server information and statistics.
        """

        # retrieve guild config
        guild_config = next(cfg for cfg in self.bot.db.configs if cfg["guild_id"] == ctx.guild.id)

        # Prepare embed
        desc = guild_config["language"].cmdServerInfo_desc.format(ctx.guild.owner.display_name, ctx.guild.owner.id)
        time = datetime.datetime.now(get_localzone())
        created_at = ctx.guild.created_at.strftime(guild_config["language"].dateTimeFormat)
        bot_user = [m for m in ctx.guild.members if m.bot]
        true_member_count = ctx.guild.member_count - len(bot_user)
        member_count = '{0} + {1} bots'.format(true_member_count, len(bot_user))

        embed = discord.Embed(colour=3447003, description=desc, timestamp=time)
        embed.add_field(name=guild_config["language"].cmdServerInfo_memCount, value=member_count)
        embed.add_field(name=guild_config["language"].cmdServerInfo_location, value=ctx.guild.region)
        embed.add_field(name=guild_config["language"].cmdServerInfo_created, value=created_at)
        embed.add_field(name=guild_config["language"].cmdServerInfo_roles, value=str(len(ctx.guild.roles)))
        embed.add_field(name="\u200b", value="\u200b")
        embed.set_footer(text=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)

        # Send message
        await ctx.send(embed=embed)

    # ==================================================================
    @cmds.command(name="botInfo", aliases=["stat", "stats", "bot"])
    async def stats(self, ctx):
        """ Displays bot information & statistics.
        usage:: botInfo
        details:: This command will return an organised embed with bot information and statistics.
        """

        # retrieve guild config
        guild_config = next(cfg for cfg in self.bot.db.configs if cfg["guild_id"] == ctx.guild.id)

        # Prepare embed
        time = datetime.datetime.now(get_localzone())
        uptime = self._get_readable_time(self.startTime, time)
        chan_count = 0
        online_mem_count = 0
        total_mem_count = 0
        for guild in self.bot.guilds:
            chan_count += len([chan for chan in guild.channels if isinstance(chan.category, discord.CategoryChannel)])
            total_mem_count += guild.member_count
            online_mem_count += len([mem for mem in guild.members if mem.status == discord.Status.online])

        embed = discord.Embed(colour=3447003, title=guild_config["language"].cmdBotInfo_title,
                              description=guild_config["language"].cmdBotInfo_desc,
                              timestamp=time)
        embed.add_field(name=guild_config["language"].cmdBotInfo_status,
                        value=guild_config["language"].cmdBotInfo_statusVal)
        embed.add_field(name=guild_config["language"].cmdBotInfo_uptime, value=uptime)
        embed.add_field(name=guild_config["language"].cmdBotInfo_latency,
                        value="{0} ms".format(round(self.bot.latency, 2)))
        embed.add_field(name=guild_config["language"].cmdBotInfo_guilds, value="{0}".format(len(self.bot.guilds)))
        embed.add_field(name=guild_config["language"].cmdBotInfo_members,
                        value=guild_config["language"].cmdBotInfo_membersVal.format(online_mem_count, total_mem_count))
        embed.add_field(name=guild_config["language"].cmdBotInfo_channels, value="{0}".format(chan_count))
        embed.add_field(name=guild_config["language"].cmdBotInfo_ram,
                        value="{:.2f} MiB".format(self.process.memory_full_info().uss / 2 ** 20))
        embed.add_field(name=guild_config["language"].cmdBotInfo_cpu,
                        value="{:.2f}% CPU".format(self.process.cpu_percent()))
        embed.add_field(name=guild_config["language"].cmdBotInfo_lib, value="discord.py (rewrite)")
        embed.set_footer(text="Bot ID: {0}".format(self.bot.user.id))
        await ctx.send(embed=embed)

    # ==================================================================
    @cmds.command(name="userInfo", aliases=["user"])
    async def user_info(self, ctx, *, member: discord.Member=None):
        """ Get detailed info for a nominated user.
        usage:: user [@mention|userid]
        details:: This command will get information on either a nominated user, or yourself.
        """

        # retrieve guild config
        guild_config = next(cfg for cfg in self.bot.db.configs if cfg["guild_id"] == ctx.guild.id)

        # Check member
        if member is None:
            member = ctx.author

        # Prepare embed
        time = datetime.datetime.now(get_localzone())
        created = member.created_at.strftime(guild_config["language"].dateTimeFormat)
        account_seniority = (datetime.datetime.now() - member.created_at).days
        joined = member.joined_at.strftime(guild_config["language"].dateTimeFormat)
        guild_seniority = (datetime.datetime.now() - member.joined_at).days

        embed = discord.Embed(colour=member.top_role.colour, timestamp=time)
        embed.set_author(name=guild_config["language"].cmdUserInfo_name.format(member.display_name, member.id),
                         icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name=guild_config["language"].cmdUserInfo_created,
                        value=guild_config["language"].cmdUserInfo_day.format(created, account_seniority),
                        inline=False)
        embed.add_field(name=guild_config["language"].cmdUserInfo_joined,
                        value=guild_config["language"].cmdUserInfo_day.format(joined, guild_seniority),
                        inline=False)

        # Send embed
        await ctx.send(embed=embed)

    @user_info.error
    async def user_info_error(self, ctx, error):
        # retrieve guild config
        guild_config = next(cfg for cfg in self.bot.db.configs if cfg["guild_id"] == ctx.guild.id)

        if isinstance(error, cmds.BadArgument):
            await ctx.send(guild_config["language"].cmdUserInfo_badArgs)
        elif isinstance(error, cmds.MissingRequiredArgument):
            await ctx.send(guild_config["language"].cmdUserInfo_missArgs)
        else:
            print(error)


# ======================================================================
def setup(bot: cmds.Bot):
    bot.add_cog(General(bot))
