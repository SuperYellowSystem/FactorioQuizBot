# ======================================================================
# imports
# ======================================================================
import importlib

import logging
logger = logging.getLogger(__name__)

supported_language = ["fr"]


class I18N:
    """ Internationalization """

    def __init__(self, lang):
        self.name = None
        self.dateTimeFormat = None

        # Attributes declaration
        self.cmdHelp_alias = None
        self.cmdHelp_load = None
        self.cmdHelp_unload = None
        self.cmdHelp_reload = None
        self.cmdHelp_ping = None
        self.cmdHelp_serverInfo = None
        self.cmdHelp_userInfo = None
        self.cmdHelp_botInfo = None
        self.cmdHelp_startQuiz = None

        self.cmdHelp_loadExt = None
        self.cmdHelp_unloadExt = None
        self.cmdHelp_reloadExt = None
        self.cmdHelp_pingExt = None
        self.cmdHelp_serverInfoExt = None
        self.cmdHelp_userInfoExt = None
        self.cmdHelp_botInfoExt = None
        self.cmdHelp_startQuizExt = None

        self.cmdPing_ping = None
        self.cmdPing_pong = None
        self.cmdPing_roundtrip = None

        self.cmdServerInfo_desc = None
        self.cmdServerInfo_memCount = None
        self.cmdServerInfo_location = None
        self.cmdServerInfo_created = None
        self.cmdServerInfo_roles = None

        self.cmdUserInfo_name = None
        self.cmdUserInfo_created = None
        self.cmdUserInfo_joined = None
        self.cmdUserInfo_footer = None
        self.cmdUserInfo_day = None

        self.cmdBotInfo_title = None
        self.cmdBotInfo_desc = None
        self.cmdBotInfo_status = None
        self.cmdBotInfo_statusVal = None
        self.cmdBotInfo_uptime = None
        self.cmdBotInfo_latency = None
        self.cmdBotInfo_guilds = None
        self.cmdBotInfo_members = None
        self.cmdBotInfo_membersVal = None
        self.cmdBotInfo_channels = None
        self.cmdBotInfo_ram = None
        self.cmdBotInfo_cpu = None
        self.cmdBotInfo_lib = None

        self.cmdStartTrain_started = None
        self.cmdStartTrain_pass = None
        self.cmdStartTrain_wrong = None
        self.cmdStartTrain_stop = None

        self.cmdQuizList_difficulty = None

        # language selection
        if self._is_supported(lang):
            selected_lang = importlib.import_module("language."+lang)
            selected_lang.localization(self)
        else:
            raise NotImplementedError('Unsupported language.')

    @staticmethod
    def _is_supported(lang):
        for language in supported_language:
            if lang == language:
                return True
        return False
