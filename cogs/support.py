# ======================================================================
# imports
# ======================================================================
import config
from language.i18n import I18N

from discord.ext import commands as cmds

import logging
logger = logging.getLogger(__name__)


# ======================================================================
class Support:
    def __init__(self, bot):
        self.bot = bot
        self.i18n = I18N(config.LANGUAGE)
        # TODO: Rework this dict for dynamic help info, when adding new commands
        self.cmdDict = {
            # Admin
            "load": self.i18n.cmdHelp_load,
            "loadExt": self.i18n.cmdHelp_loadExt,
            "unload": self.i18n.cmdHelp_unload,
            "unloadExt": self.i18n.cmdHelp_unloadExt,
            "reload": self.i18n.cmdHelp_reload,
            "reloadExt": self.i18n.cmdHelp_reloadExt,
            # General
            "ping": self.i18n.cmdHelp_ping,
            "pingExt": self.i18n.cmdHelp_pingExt,
            "serverInfo": self.i18n.cmdHelp_serverInfo,
            "serverInfoExt": self.i18n.cmdHelp_serverInfoExt,
            "userInfo": self.i18n.cmdHelp_userInfo,
            "userInfoExt": self.i18n.cmdHelp_userInfoExt,
            "botInfo": self.i18n.cmdHelp_botInfo,
            "botInfoExt": self.i18n.cmdHelp_botInfoExt,
            # Quiz
            "startQuiz": self.i18n.cmdHelp_startQuiz,
            "startQuizExt": self.i18n.cmdHelp_startQuizExt,
        }

    def _display_cmd_from_cog(self, ctx, cog_name, is_support):
        # get longest command name length
        longest = self._get_longest_name_length(ctx)
        # display command from a cog
        msg = f"\u200b\n== {cog_name} ==\n"
        cmd_list = ctx.bot.get_cog_commands(cog_name)
        for cmd in cmd_list:
            if is_support and cmd.name == "help":
                continue
            else:
                msg += f'{ctx.prefix}{cmd.name:<{longest}} :: {self.cmdDict.get(cmd.name,"undefined")}\n'
        return msg

    @staticmethod
    def _get_longest_name_length(ctx):
        cmd_list = ctx.bot.commands
        longest = 0
        for cmd in cmd_list:
            if len(cmd.name) > longest:
                longest = len(cmd.name)
        return longest

    @cmds.command(aliases=["commands", "cmd"])
    async def help(self, ctx, *, command: str=None):
        """Shows this message."""
        if command is None:
            # Displays help message
            msg = f"= Command List =\n\n[Use {ctx.prefix}help <commandname> for details]\n"
            for name in ctx.bot.cogs:
                # Do not display admin command if user is not owner
                if name == "Admin" and not ctx.bot.is_owner(ctx.author):
                    continue
                # Do not display help command
                elif name == "Support":
                    cmd_list = ctx.bot.get_cog_commands(name)
                    if len(cmd_list) == 1 and cmd_list.pop().name == "help":
                        continue
                    else:
                        msg += self._display_cmd_from_cog(ctx, name, True)
                else:
                    msg += self._display_cmd_from_cog(ctx, name, False)

            await ctx.send(f'```asciidoc\n{msg}\n```')
        else:
            # Display help for a specific command
            cmd = ctx.bot.get_command(command)
            if cmd is None:
                await ctx.send(ctx.bot.command_not_found.format(command))
                return

            msg = f'= {cmd.name} =\n{self.cmdDict.get(cmd.name, "undefined")}\n'
            details = self.cmdDict.get(cmd.name+"Ext", "undefined")
            if details != "undefined":
                aliases = ""
                if len(cmd.aliases) != 0:
                    aliases = self.i18n.cmdHelp_alias
                    for alias in cmd.aliases:
                        aliases += alias + ", "
                    aliases = aliases[:-2]
                # search splitter char
                index = details.find("#")
                # (index+1) for removing splitter char
                msg += details[:index] + aliases + details[index+1:]

            await ctx.send(f'```asciidoc\n{msg}\n```')


# ======================================================================
def setup(bot: cmds.Bot):
    bot.add_cog(Support(bot))
