def localization(self):
    """ French internationalization """

    self.name = "FactoQuizBot"
    self.dateTimeFormat = "%d/%m/%Y à %H:%M:%S"

    # Support command ==============================================
    self.cmdHelp_alias = "\nalias   :: "
    # help / Admin
    self.cmdHelp_load = "Active un module."
    self.cmdHelp_loadExt = "usage   :: load <command>#\ndétails :: Active un module."
    self.cmdHelp_unload = "Désactive un module."
    self.cmdHelp_unloadExt = "usage   :: unload <command>#\ndétails :: Désactive un module."
    self.cmdHelp_reload = "Met à jour un module."
    self.cmdHelp_reloadExt = "usage   :: reload <command>#\ndétails :: Met à jour un module."

    # help / General
    self.cmdHelp_ping = "Latence & temps de réponse de l'API."
    self.cmdHelp_pingExt = "usage   :: ping#\ndétails :: Cette commande aide à détecter s'il y a de la latence (" \
                           "lag) du coté de la connectivité du bot, ou de l'API."
    self.cmdHelp_serverInfo = "Infos & stats du serveur."
    self.cmdHelp_serverInfoExt = "usage   :: serverInfo#\ndétails :: Cette commande affiche diverses informations " \
                                 "et statistiques du serveur."
    self.cmdHelp_userInfo = "Infos détaillées pour un utilisateur donné."
    self.cmdHelp_userInfoExt = "usage   :: userInfo [@mention|userid]#\ndétails :: Cette commande affiche des " \
                               "informations sur un utilisateur en particulier ou sur vous-même."
    self.cmdHelp_botInfo = "Infos & stats du bot."
    self.cmdHelp_botInfoExt = "usage   :: botInfo#\ndétails :: Cette commande affiche diverses informations et " \
                              "statistiques du bot."

    # help / Support

    # help / Quiz
    self.cmdHelp_startQuiz = "Démarre le quiz d'entraînement"
    self.cmdHelp_startQuizExt = "usage   :: startquiz#\ndétails :: Cette commande permet de démarrer un quiz " \
                                "d'entraînement. Tout le monde peut y participer, mais seul le plus rapide pourra " \
                                "y répondre."

    # General command ==============================================
    # Ping command
    self.cmdPing_ping = "🏓 Ping!"
    self.cmdPing_pong = "🏓 Pong!"
    self.cmdPing_roundtrip = "🏓 Pong! (↔️: {0} ms. 💙: {1} ms.)"

    # server_info command
    self.cmdServerInfo_desc = "Propriétaire: {0} ({1})"
    self.cmdServerInfo_memCount = "Nombre de membres"
    self.cmdServerInfo_location = "Emplacement"
    self.cmdServerInfo_created = "Date de création"
    self.cmdServerInfo_roles = "Rôles"

    # user_info command
    self.cmdUserInfo_name = "{0}\n({1})"
    self.cmdUserInfo_created = "Compte créé le"
    self.cmdUserInfo_joined = "Membre depuis le"
    self.cmdUserInfo_footer = "Information utilisateur"
    self.cmdUserInfo_day = "{0}\n({1} jours auparavant)"
    self.cmdUserInfo_badArgs = "Je ne peux pas trouver ce membre..."
    self.cmdUserInfo_missArgs = "Euuuuuhhh... Ils sont où les paramètres?!?"

    # stats command
    self.cmdBotInfo_title = "Information diverses"
    self.cmdBotInfo_desc = "FactoQuizBot est un bot qui vous permets de tester vos connaissances sur le jeu " \
                           "Factorio."
    self.cmdBotInfo_status = "Status"
    self.cmdBotInfo_statusVal = "En ligne"
    self.cmdBotInfo_uptime = "En fonction depuis"
    self.cmdBotInfo_latency = "Latence"
    self.cmdBotInfo_guilds = "Serveurs"
    self.cmdBotInfo_members = "Utilisateurs"
    self.cmdBotInfo_membersVal = "{0}/{1} en ligne"
    self.cmdBotInfo_channels = "Salons"
    self.cmdBotInfo_ram = "RAM utilisé"
    self.cmdBotInfo_cpu = "CPU utilisé"
    self.cmdBotInfo_lib = "Bibliothèque"

    # quiz ============================================================
    # start_training_quiz
    self.cmdStartTrain_started = "Le quiz est déjà lancé!"
    self.cmdStartTrain_pass = "Bravo!!! {0} était bien la bonne réponse."
    self.cmdStartTrain_wrong = "Dommage!!! La bonne réponse était {0}"
    self.cmdStartTrain_stop = "Le quiz est désormais stoppé."

    # quizList
    self.cmdQuizList_difficulty = "Difficulté"