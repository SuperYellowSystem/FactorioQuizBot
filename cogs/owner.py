# NB: Based on the work of Rapptz on RoboDanny
# src: https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/admin.py
# ======================================================================
# imports
# ======================================================================
from discord.ext import commands as cmds
import traceback

from cogs.utils import checks

import logging
logger = logging.getLogger(__name__)


# ======================================================================
class Owner:
    """Owner-only commands that make the bot easier to debug/manage."""

    def __init__(self, bot):
        self.bot = bot

    @checks.is_owner()
    @cmds.command(hidden=True)
    async def load(self, ctx, *, module):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            logger.error(f'Error while loading cog {module}', e)
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.message.add_reaction('\N{OK HAND SIGN}')

    @checks.is_owner()
    @cmds.command(hidden=True)
    async def unload(self, ctx, *, module):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            logger.error(f'Error while unloading cog {module}', e)
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.message.add_reaction('\N{OK HAND SIGN}')

    @checks.is_owner()
    @cmds.command(name='reload', hidden=True)
    async def _reload(self, ctx, *, module):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            logger.error(f'Error while reloading cog {module}', e)
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.message.add_reaction('\N{OK HAND SIGN}')


# ======================================================================
def setup(bot: cmds.Bot):
    bot.add_cog(Owner(bot))
