# ======================================================================
# imports
# ======================================================================
import config

from discord.ext import commands

import os
import logging
import traceback
from cogs.utils.database import Database

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

        # Load database
        self.db = Database()
        self.db.create_tables()
        self.db.load_data()

        super().__init__(command_prefix=config.PREFIX, description=config.DESCRIPTION, pm_help=None)
        self.remove_command("help")

        # Load cogs
        for cog in initial_cogs:
            try:
                self.load_extension(cog)
                logger.info(f'{cog} successfully loaded.')
            except Exception as e:
                print(f'Failed to load extension {cog}.')
                traceback.print_exc(limit=-1)

    def create_config_guild(self, guild):
        for cfg in self.db.configs:
            if guild.id == cfg["guild_id"]:
                break
        else:
            # guild not found in database, then create config
            new_config = self.db.create_config(guild.id, config.PREFIX, config.LANGUAGE, config.DELETE_MESSAGES)
            self.db.configs.append(new_config)
            self.db.add_new_config(new_config)

    async def on_ready(self):
        """Event called when the bot is ready"""

        # Check if guilds were added while offline
        for guild in self.guilds:
            self.create_config_guild(guild)

        # Change name
        await self.user.edit(username=f'[{config.PREFIX}] FactorioBot')

    async def on_guild_join(self, guild):
        """Event called when client join a guild or client create a new guild"""

        # Create new config
        self.create_config_guild(guild)

    async def on_guild_remove(self, guild):
        """Event called when guild is removed from client"""

        # Remove config
        self.db.configs = [cfg for cfg in self.db.configs if guild.id != cfg["guild_id"]]
        self.db.delete_config(guild.id)


# ======================================================================
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
