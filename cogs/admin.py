# NB: Based on the work of Rapptz on RoboDanny
# src: https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/admin.py
# ======================================================================
# imports
# ======================================================================
from discord.ext import commands as cmds
import traceback

import logging
logger = logging.getLogger(__name__)


# ======================================================================
class Admin:
    """Admin-only commands that make the bot dynamic."""

    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @cmds.command(hidden=True)
    async def load(self, ctx, *, module):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @cmds.command(hidden=True)
    async def unload(self, ctx, *, module):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @cmds.command(name='reload', hidden=True)
    async def _reload(self, ctx, *, module):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('\N{OK HAND SIGN}')


# ======================================================================
def setup(bot: cmds.Bot):
    bot.add_cog(Admin(bot))
