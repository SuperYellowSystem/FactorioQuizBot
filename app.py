# ======================================================================
# imports
# ======================================================================
import config

import discord
from discord import Forbidden
from discord.ext import commands

import os
import logging
from cogs.utils.database import Database

initial_cogs = {"cogs.admin", "cogs.general", "cogs.support", "cogs.quiz", "cogs.owner"}

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
        self.prefix = config.PREFIX

        # Load database
        self.db = Database()
        self.db.create_tables()
        self.db.load_data()

        super().__init__(command_prefix=self.get_prefix, description=config.DESCRIPTION, pm_help=None)

    async def get_prefix(self, message):
        prefixes = set()
        if isinstance(message.channel, discord.abc.PrivateChannel):
            prefixes.add(self.prefix)
            return commands.when_mentioned_or(*prefixes)(bot, message)
        guild_config = next(cfg for cfg in self.db.configs if cfg["guild_id"] == message.guild.id)
        prefixes.add(guild_config["prefix"])
        return commands.when_mentioned_or(*prefixes)(bot, message)

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

        try:
            for g in self.guilds:
                guild_config = next(cfg for cfg in self.db.configs if cfg["guild_id"] == g.id)
                bot_member = g.get_member(config.BOT_ID)
                if bot_member is None:
                    print("ohlalala")
                else:
                    await bot_member.edit(nick=f'[{guild_config["prefix"]}] FactorioBot',
                                          reason="FactorioBot's prefix has changed")
        except Forbidden as forbidError:
            print(forbidError)

        # Load cogs
        self.remove_command("help")
        for cog in initial_cogs:
            try:
                self.load_extension(cog)
                logger.info(f'{cog} successfully loaded.')
            except Exception as e:
                logger.error(f'Failed to load extension {cog}.', e)

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
