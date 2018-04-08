# ======================================================================
# imports
# ======================================================================
from discord.ext import commands as cmds

from cogs.utils.quizList import QuizList, solution_index

import logging
logger = logging.getLogger(__name__)


# ======================================================================
class Quiz:
    def __init__(self, bot):
        self.bot = bot

    @cmds.command(name="startQuiz", aliases=["train", "quiz", "trial"])
    async def start_quiz(self, ctx):
        # retrieve guild config
        guild_config = next(cfg for cfg in self.bot.db.configs if cfg["guild_id"] == ctx.guild.id)

        if guild_config["isQuizStarted"]:
            await ctx.send(guild_config["language"].cmdStartTrain_started)
            return

        # create questions list if needed
        if guild_config["questions"] is None:
            guild_config["questions"] = QuizList(guild_config["language"])

        # start quiz
        guild_config["isQuizStarted"] = True
        while guild_config["isQuizStarted"]:
            item = guild_config["questions"].select_next_item()
            solution = item.get_solution()
            last_msg = await ctx.send(embed=item.create_item_embed())
            for i in range(item.get_nb_answers()):
                await last_msg.add_reaction(str(solution_index.get(i+1)))
            await last_msg.add_reaction('\U0000274C')

            def check(r, u):
                return (str(r.emoji) == '\U0001F1E6' or str(r.emoji) == '\U0001F1E7' or str(r.emoji)
                        == '\U0001F1E8' or str(r.emoji) == '\U0001F1E9' or str(r.emoji) == '\U0000274C') \
                       and u is not last_msg.author and r.message.id == last_msg.id

            reaction, user = await self.bot.wait_for('reaction_add', check=check)
            if str(reaction.emoji) == solution:
                await ctx.send(guild_config["language"].cmdStartTrain_pass. format(solution))
            elif str(reaction.emoji) == '\U0000274C':
                guild_config["isQuizStarted"] = False
                await ctx.send(guild_config["language"].cmdStartTrain_stop)
            else:
                await ctx.send(guild_config["language"].cmdStartTrain_wrong.format(solution))

        # Quiz stopped, Time to delete messages if wanted
        if guild_config["delete_msg"]:
            def is_me(m):
                if m.author == self.bot.user:
                    return True
                else:
                    for cmd in ctx.bot.commands:
                        if m.content == f'{ctx.prefix}{cmd.name}':
                            return True
                        for alias in cmd.aliases:
                            if m.content == f'{ctx.prefix}{alias}':
                                return True
                    return False
            await ctx.channel.purge(limit=100, check=is_me)

        # Change questions order
        guild_config["questions"].shuffle_list()


# ======================================================================
def setup(bot: cmds.Bot):
    bot.add_cog(Quiz(bot))
