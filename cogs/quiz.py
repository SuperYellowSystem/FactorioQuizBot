# ======================================================================
# imports
# ======================================================================
from discord.ext import commands as cmds

from cogs.utils.quizList import QuizList, solution_index

import config
from language.i18n import I18N

import logging
logger = logging.getLogger(__name__)


# ======================================================================
class Quiz:
    def __init__(self, bot):
        self.bot = bot
        self.i18n = I18N(config.LANGUAGE)
        self.started = False
        self.quizList = QuizList()

    @cmds.command(name="startQuiz", aliases=["train", "quiz", "trial"])
    async def start_quiz(self, ctx):
        if self.started:
            await ctx.send(self.i18n.cmdStartTrain_started)
            return

        # start quiz
        self.started = True
        while self.started:
            item = self.quizList.select_next_item()
            solution = item.get_solution()
            last_msg = await ctx.send(embed=item.create_item_embed())
            for i in range(item.get_nb_answers()):
                await last_msg.add_reaction(str(solution_index.get(i+1)))
            await last_msg.add_reaction('\U0000274C')

            def check(r, u):
                return (str(r.emoji) == '\U0001F1E6' or str(r.emoji) == '\U0001F1E7' or str(r.emoji)
                        == '\U0001F1E8' or str(r.emoji) == '\U0001F1E9' or str(r.emoji) == '\U0000274C') \
                       and u is not last_msg.author

            reaction, user = await self.bot.wait_for('reaction_add', check=check)
            if str(reaction.emoji) == solution:
                await ctx.send(self.i18n.cmdStartTrain_pass. format(solution))
            elif str(reaction.emoji) == '\U0000274C':
                self.started = False
                await ctx.send(self.i18n.cmdStartTrain_stop)
            else:
                await ctx.send(self.i18n.cmdStartTrain_wrong.format(solution))

        # Quiz stopped, Time to delete messages if wanted
        if config.DELETE_MESSAGES:
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
        self.quizList.shuffle_list()


# ======================================================================
def setup(bot: cmds.Bot):
    bot.add_cog(Quiz(bot))
