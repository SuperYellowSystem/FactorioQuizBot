# ======================================================================
# imports
# ======================================================================
from discord.ext import commands as cmds

from cogs.utils import checks
from language.i18n import I18N, supported_language

import config
import logging
logger = logging.getLogger(__name__)


# ======================================================================
class Admin:
    """Admin-only commands that guild owner can use for modify settings."""

    def __init__(self, bot):
        self.bot = bot

    @checks.is_admin()
    @checks.is_not_dm()
    @cmds.command(name="config", aliases=["show", "showConfig"])
    async def show_config(self, ctx):
        try:
            guild_config = next(cfg for cfg in self.bot.db.configs if cfg["guild_id"] == ctx.guild.id)
            msg = ""
            for key, value in guild_config.items():
                if key == "guild_id" or key == "isQuizStarted" or key == "questions":
                    continue
                elif key == "language":
                    msg += f'{key} :: {value.get_language()}\n'
                else:
                    msg += f'{key} :: {value}\n'
            await ctx.send(f'```asciidoc\n== {ctx.guild.name} ==\n{msg}```')
        except StopIteration as stopItE:
            logger.error(f'Error: cannot find a config for guild {ctx.guild.name}', stopItE)
        except Exception as e:
            logger.error("Error while displaying config", e)

    @checks.is_admin()
    @checks.is_not_dm()
    @cmds.command(name="edit", aliases=["editConfig"])
    async def edit_config(self, ctx, arg: str, value: str):
        try:
            guild_config = next(cfg for cfg in self.bot.db.configs if cfg["guild_id"] == ctx.guild.id)
            if arg == "guild_id" or arg == "isQuizStarted" or arg == "questions":
                return
            elif arg == "language":
                if value not in supported_language:
                    await ctx.send(f'**{value}** {guild_config["language"].cmdEditConfig_unsupportedLang} '
                                   f'{supported_language}')
                elif value == guild_config["language"].get_language():
                    await ctx.send(f'**{arg}** {guild_config["language"].cmdEditConfig_alrdyConfigured} **{value}**.')
                else:
                    guild_config[arg] = I18N(value)
                    self.bot.db.edit_config(arg, value, guild_config["guild_id"])
                    await ctx.send(f'**{arg}** {guild_config["language"].cmdEditConfig_configured} **{value}**')
            else:
                if value == guild_config[arg]:
                    await ctx.send(f'**{arg}** {guild_config["language"].cmdEditConfig_alrdyConfigured} **{value}**.')
                elif arg in guild_config:
                    guild_config[arg] = value
                    self.bot.db.edit_config(arg, value, guild_config["guild_id"])
                    await ctx.send(f'**{arg}** {guild_config["language"].cmdEditConfig_configured} **{value}**')
                    if arg == "prefix":
                        await ctx.guild.get_member(config.BOT_ID).edit(nick=f'[{guild_config["prefix"]}] FactorioBot',
                                                                       reason="FactorioBot's prefix has changed")
                else:
                    await ctx.send(f'**{arg}** {guild_config["language"].cmdEditConfig_syntaxError}')
        except StopIteration as stopItE:
            logger.error(f'Error: cannot find a config for guild {ctx.guild.name}', stopItE)
        except Exception as e:
            logger.error("Error while editing config", e)


# ======================================================================
def setup(bot: cmds.Bot):
    bot.add_cog(Admin(bot))
