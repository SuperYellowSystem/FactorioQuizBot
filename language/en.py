def localization(self):
    """ English internationalization """

    self.name = "FactoQuizBot"
    self.dateTimeFormat = "%d/%m/%Y à %H:%M:%S"

    # Support command ==============================================
    self.cmdHelp_details = "= Command List =\n\n[Use {0}help <commandname> for details]\n"
    self.cmdHelp_alias = "\naliases:: "

    # help / Admin
    self.cmdHelp_load = "Loads a module."
    self.cmdHelp_loadExt = "usage:: load <command>#\ndetails:: Loads a module."
    self.cmdHelp_unload = "Unloads a module."
    self.cmdHelp_unloadExt = "usage:: unload <command>#\ndetails:: Unloads a module."
    self.cmdHelp_reload = "Reloads a module."
    self.cmdHelp_reloadExt = "usage:: reload <command>#\ndetails:: Reloads a module."

    # help / General
    self.cmdHelp_ping = "Show latency & API response times."
    self.cmdHelp_pingExt = "usage:: ping#\ndetails:: This command is a response test, it helps gauge if there is " \
                           "any latency (lag) in either the bots connections, or the API."
    self.cmdHelp_serverInfo = "Displays server information & statistics."
    self.cmdHelp_serverInfoExt = "usage:: serverInfo#\ndetails:: This command will return an organised embed " \
                                 "with server information and statistics."
    self.cmdHelp_userInfo = "Get detailed info for a nominated user."
    self.cmdHelp_userInfoExt = "usage:: userInfo [@mention|userid]#\ndetails:: This command will get information " \
                               "on either a nominated user, or yourself."
    self.cmdHelp_botInfo = "Displays bot information & statistics."
    self.cmdHelp_botInfoExt = "usage:: botInfo#\ndetails:: This command will return an organised embed with bot " \
                              "information and statistics."

    # help / Support

    # General command ==============================================
    # Ping
    self.cmdPing_ping = "🏓 Ping!"
    self.cmdPing_pong = "🏓 Pong!"
    self.cmdPing_roundtrip = "🏓 Pong! (↔️: {0} ms. 💙: {1} ms.)"

    # server_info
    self.cmdServerInfo_desc = "Owner: {0} ({1})"
    self.cmdServerInfo_memCount = "Member Count"
    self.cmdServerInfo_location = "Location"
    self.cmdServerInfo_created = "Created at"
    self.cmdServerInfo_roles = "Role"

    # user_info
    self.cmdUserInfo_created = "Created at"
    self.cmdUserInfo_joined = "Member since"
    self.cmdUserInfo_footer = "User info"
    self.cmdUserInfo_day = "{0}\n({1} days ago)"
    self.cmdUserInfo_score = "Best score"
    self.cmdUserInfo_badArgs = "I could not find that member..."
    self.cmdUserInfo_missArgs = "Meehh... Where are the arguments?"

    # stats
    self.cmdBotInfo_title = "Bot Information"
    self.cmdBotInfo_desc = "FactoQuizBot is a bot that challenge your knowledges about the game Factorio."
    self.cmdBotInfo_status = "Current Status"
    self.cmdBotInfo_statusVal = "Online"
    self.cmdBotInfo_uptime = "Uptime"
    self.cmdBotInfo_latency = "Latency"
    self.cmdBotInfo_guilds = "Guilds"
    self.cmdBotInfo_members = "Users"
    self.cmdBotInfo_membersVal = "{0}/{1} online"
    self.cmdBotInfo_channels = "Channels"
    self.cmdBotInfo_ram = "RAM Usage"
    self.cmdBotInfo_cpu = "CPU Usage"
    self.cmdBotInfo_lib = "Library"

    # quiz ============================================================
    # start_quiz
    self.cmdStartTrain_started = "Quiz is already running!"
    self.cmdStartTrain_pass = "Congratulation!!! {0} is the correct answer"
    self.cmdStartTrain_wrong = "Bad answer! The correct one was"
    self.cmdStartTrain_stop = "Quiz is now stopped."

    # start_exam
    self.cmdStartExam_rules = "TODO: quiz begins"
    self.cmdStartExam_better = "Your score for this session is {0}/20. You don't beat your previous score of {1}/20."
    self.cmdStartExam_bad = "Your score for this session is {0}/20. You don't beat your previous score of {1}/20."
    self.cmdStartExam_best = "Congratulations!!! You make a perfect score of {0}/20. Factorio have no secret" \
                             "for you now. Your previous score was {1}/20."

    # quizList
    self.cmdQuizList_difficulty = "Difficulty"

    # admin ============================================================
    # show_config

    # edit_config
    self.cmdEditConfig_syntaxError = "is not an element of the config. Please check the syntax!"
    self.cmdEditConfig_alrdyConfigured = "is already configured to"
    self.cmdEditConfig_unSupportedLang = "is not a supported language.\nCurrently supported:"
    self.cmdEditConfig_configured = "is now configured to"

