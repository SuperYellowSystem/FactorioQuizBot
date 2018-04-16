# ======================================================================
# imports
# ======================================================================
from discord.ext import commands as cmds

from cogs.utils.quizList import QuizList, solution_index
from cogs.utils import checks

import datetime
from tzlocal import get_localzone

from discord import Embed

import logging
logger = logging.getLogger(__name__)


# ======================================================================
class Quiz:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def is_quiz_running(ctx, check: bool, i18n):
        if check:
            await ctx.send(i18n.cmdStartTrain_started)
            return True
        return False

    async def launch_quiz(self, channel, data: dict, i18n, is_exam: bool):
        result = 0
        count = 0
        data["isQuizStarted"] = True
        while data["isQuizStarted"]:
            # Post new question
            item = data["questions"].select_next_item()
            solution = item.get_solution()
            last_msg = await channel.send(embed=item.create_item_embed())

            # Add reactions
            for i in range(item.get_nb_answers()):
                await last_msg.add_reaction(str(solution_index.get(i+1)))
            await last_msg.add_reaction('\U0000274C')

            # Wait for event on reaction
            def check(r, u):
                return (str(r.emoji) == '\U0001F1E6' or str(r.emoji) == '\U0001F1E7' or str(r.emoji)
                        == '\U0001F1E8' or str(r.emoji) == '\U0001F1E9' or str(r.emoji) == '\U0000274C') \
                       and u is not last_msg.author and r.message.id == last_msg.id
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
            if str(reaction.emoji) == solution:
                result += 1
                if is_exam: await last_msg.delete()
                else:       await channel.send(i18n.cmdStartTrain_pass.format(solution))
            elif str(reaction.emoji) == '\U0000274C':
                data["isQuizStarted"] = False
                if is_exam: await last_msg.delete()
                else:       await channel.send(i18n.cmdStartTrain_stop)
            else:
                if is_exam: await last_msg.delete()
                else:       await channel.send(f'{i18n.cmdStartTrain_wrong} {solution}')

            count += 1
            if is_exam and count == 20:
                data["isQuizStarted"] = False

        # Change questions order
        data["questions"].shuffle_list()
        return result

    async def remove_msg(self, ctx, delete: bool, i18n):
        if delete:
            def is_quiz_item(m):
                # Check if msg is part of quiz
                if m.author == self.bot.user:
                    if '\U0001F1E6' in m.content \
                            or '\U0001F1E7' in m.content \
                            or '\U0001F1E8' in m.content \
                            or '\U0001F1E9' in m.content:
                        return True
                    if i18n.cmdStartTrain_stop in m.content \
                            or i18n.cmdStartTrain_started in m.content:
                        return True
                    for embed in m.embeds:
                        if "/" in embed.title:
                            return True
                    return False
                # Else check if msg is the cmd which start quiz
                for cmd in ctx.bot.get_cog_commands("Quiz"):
                    if f'{ctx.prefix}{cmd.name}' in m.content:
                        return True
                    for alias in cmd.aliases:
                        if f'{ctx.prefix}{alias}' in m.content:
                            return True
                return False
            await ctx.channel.purge(limit=100, check=is_quiz_item)

    @checks.is_not_dm()
    @cmds.command(name="startQuiz", aliases=["train", "quiz", "trial"])
    async def start_quiz(self, ctx):
        # retrieve guild config
        guild_config = next(cfg for cfg in self.bot.db.configs if cfg["guild_id"] == ctx.guild.id)

        if await self.is_quiz_running(ctx, guild_config["isQuizStarted"], guild_config["language"]):
            return

        # prepare questions
        if guild_config["questions"] is None:
            guild_config["questions"] = QuizList(guild_config["language"], False)
        guild_config["questions"].shuffle_list()

        # start quiz
        await self.launch_quiz(ctx, guild_config, guild_config["language"], False)

        # Quiz stopped, Time to delete messages if wanted
        await self.remove_msg(ctx, guild_config["delete_msg"], guild_config["language"])

    @staticmethod
    def create_exam_rules(i18n):
        time = datetime.datetime.now(get_localzone())
        embed = Embed(title=i18n.cmdStartExam_title, description=i18n.cmdStartExam_desc, colour=3447003, timestamp=time)
        embed.add_field(name=i18n.cmdStartExam_workflow, value=i18n.cmdStartExam_workflowDesc)
        embed.add_field(name=i18n.cmdStartExam_score, value=i18n.cmdStartExam_scoreDesc)
        embed.add_field(name=i18n.cmdStartExam_time, value=i18n.cmdStartExam_timeDesc)
        embed.add_field(name=i18n.cmdStartExam_note, value=i18n.cmdStartExam_noteDesc)
        return embed

    @checks.is_not_dm()
    @cmds.command(name="startExam", aliases=["exam"])
    async def start_exam(self, ctx):
        await ctx.message.delete()

        # retrieve guild config
        guild_config = next(cfg for cfg in self.bot.db.configs if cfg["guild_id"] == ctx.guild.id)

        # retrieve score
        user_score = next(scr for scr in self.bot.db.scores
                          if scr["guild_id"] == ctx.guild.id and scr["user_id"] == ctx.author.id)

        if await self.is_quiz_running(ctx, user_score["isQuizStarted"], guild_config["language"]):
            return

        # prepare questions
        user_score["questions"] = QuizList(guild_config["language"], True)
        user_score["questions"].shuffle_list()

        # send exam workflow
        await ctx.author.send(embed=self.create_exam_rules(guild_config["language"]))

        # start quiz
        result = await self.launch_quiz(ctx.author, user_score, guild_config["language"], True)

        # store score in db
        last_result = user_score["score"]
        if last_result < result:
            user_score["score"] = result
            self.bot.db.save_score(user_score)

        # display result
        if last_result >= result:
            msg = guild_config["language"].cmdStartExam_bad
        elif result == 20:
            msg = guild_config["language"].cmdStartExam_best
        else:
            msg = guild_config["language"].cmdStartExam_better
        embed = Embed(title=guild_config["language"].cmdStartExam_ResultTitle, description=msg.format(result, last_result))
        await ctx.author.send(embed=embed)


# ======================================================================
def setup(bot: cmds.Bot):
    bot.add_cog(Quiz(bot))
