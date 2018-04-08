# ======================================================================
# imports
# ======================================================================
from discord.ext import commands as cmds
import traceback

from cogs.utils import checks

import logging
logger = logging.getLogger(__name__)


# ======================================================================
class Admin:
    """Admin-only commands that guild owner can use for modify settings."""

    def __init__(self, bot):
        self.bot = bot

    @checks.is_admin()
    @cmds.command(name="config")
    async def print_cfg(self, ctx):
        try:
            for config in self.bot.db.configs:
                if ctx.guild.id == config["guild_id"]:
                    await ctx.send(f'guild: {config["guild_id"]}\n'
                                   f'prefix: {config["prefix"]}\n'
                                   f'language: {config["language"].get_language()}\n'
                                   f'delete_msg: {config["delete_msg"]}')
                    break
            else:
                await ctx.send("Weird! There is no config for your guild.")
        except Exception as e:
            logger.error("Error while printing config", e)
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('\N{OK HAND SIGN}')


# ======================================================================
def setup(bot: cmds.Bot):
    bot.add_cog(Admin(bot))
