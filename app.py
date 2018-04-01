# ======================================================================
# imports
# ======================================================================
import config

from discord.ext import commands

import os
import logging
import traceback

initial_cogs = {"cogs.admin", "cogs.general", "cogs.support", "cogs.quiz"}

# ======================================================================
logLevelDict = {
    0: logging.CRITICAL,
    1: logging.ERROR,
    2: logging.WARNING,
    3: logging.INFO,
    4: logging.DEBUG
}


class FactorioQuizBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=config.PREFIX, description=config.DESCRIPTION, pm_help=None)
        self.remove_command("help")
        for cog in initial_cogs:
            try:
                self.load_extension(cog)
                logger.info(f'{cog} successfully loaded.')
            except Exception as e:
                print(f'Failed to load extension {cog}.')
                traceback.print_exc(limit=-1)


# ======================================================================
# TODO: Create Database
# TODO: Create Exam mod (solo)
# TODO: Multiple Guild bot
if __name__ == '__main__':
    # set up logging
    logger = logging.getLogger('discord')
    logger.setLevel(logLevelDict.get(config.LOG_LEVEL, 3))
    path_to_dir = os.getcwd() + "/logs"
    if not os.path.exists(path_to_dir):
        os.makedirs(path_to_dir)
    handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    bot = FactorioQuizBot()
    bot.run(config.TOKEN)
