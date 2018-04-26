def localization(self):
    """ French internationalization """

    self.name = "FactoQuizBot"
    self.dateTimeFormat = "%d/%m/%Y à %H:%M:%S"

    # Support command ==============================================
    self.cmdHelp_details = "= Liste des commandes =\n\n[{0}help <commande> pour plus de détails]\n"
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
    self.cmdHelp_startQuiz = "Démarre le quiz d'entraînement."
    self.cmdHelp_startQuizExt = "usage   :: startquiz#\ndétails :: Cette commande permet de démarrer un quiz " \
                                "d'entraînement. Tout le monde peut y participer, mais seul le plus rapide pourra " \
                                "y répondre."
    self.cmdHelp_startExam = "Démarre la session d'examen."
    self.cmdHelp_startExamExt = "usage   :: startExam#\ndétails :: Cette commande permet de démarrer la session " \
                                "d'examen. Cet examen est individuel et le participant peut évaluer ses connaissances" \
                                " sur le jeu Factorio."

    # help / Admin
    self.cmdHelp_config = "Affiche la configuration du serveur."
    self.cmdHelp_configExt = "usage   :: config#\ndétails :: Cette commande permet d'afficher la configuration du " \
                             "serveur."
    self.cmdHelp_edit = "Edite al configuration du serveur."
    self.cmdHelp_editExt = "usage   :: edit <option>#\ndétails :: Cette commande permet de modifier la configuration " \
                           "du serveur."

    # help / Factorio
    self.cmdHelp_linkmod = "Donne un lien vers un mod spécifié."
    self.cmdHelp_linkmodExt = "usage   :: linkmod <nom du mod>#\ndétails :: Cette commande permet de donner un lien " \
                              "vers un mod spécifié."
    self.cmdHelp_wiki = "Effectue une recherche dans le Wiki de Factorio."
    self.cmdHelp_wikiExt = "usage   :: wiki <mots clés>#\ndétails :: Cette commande permet d'effectuer une recherche " \
                           "dans le wiki de Factorio et affiche les liens en rapport avec la recherche."

    # help / FAQ
    self.cmdHelp_faq = "Montre la liste des tags FAQ."
    self.cmdHelp_faqExt = "usage   :: faq [tag]#\ndétails :: Cette commande permet d'afficher la liste de tag " \
                          "disponible. Si un tag est spécifié, alors affiche les information concernant ce tag."

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
    self.cmdUserInfo_created = "Compte créé le"
    self.cmdUserInfo_joined = "Membre depuis le"
    self.cmdUserInfo_footer = "Information utilisateur"
    self.cmdUserInfo_day = "{0} (Il y a {1} jours)"
    self.cmdUserInfo_score = "Meilleur score"
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

    # quiz =============================================================
    # start_quiz
    self.cmdStartTrain_started = "Le quiz est déjà lancé!"
    self.cmdStartTrain_pass = "Bravo!!! {0} était bien la bonne réponse."
    self.cmdStartTrain_wrong = "Dommage!!! La bonne réponse était"
    self.cmdStartTrain_stop = "Le quiz est désormais stoppé."

    # start_exam
    self.cmdStartExam_title = "Voici quelques règles et informations concernant cet examen:"
    self.cmdStartExam_desc = "Cet examen sert uniquement à tester tes connaissances du jeu Factorio. En aucun cas " \
                             "réussir ce test ne fera de toi un meilleur joueur de Factorio car il y a autant de " \
                             "façon de jouer qu'il y a de joueurs."
    self.cmdStartExam_workflow = "Fonctionnnement:"
    self.cmdStartExam_workflowDesc = "A chaque question posée, le bot va afficher des réactions. En cliquant sur ces " \
                                     "réactions, tu pourras répondre aux questions. La première réaction cliquée " \
                                     "validera la question, alors fais attention. Une fois la question validée, " \
                                     "la question s'effacera et une nouvelle question s'affichera. A n'importe quel " \
                                     "moment tu pourras cliquer sur \U0000274C pour arrêter l'examen si tu le  " \
                                     "souhaites."
    self.cmdStartExam_score = "Score:"
    self.cmdStartExam_scoreDesc = "Il y aura au total 20 questions pour un maximum de 20 points. Toutes les " \
                                  "questions valent le même nombre de points."
    self.cmdStartExam_time = "Temps:"
    self.cmdStartExam_timeDesc = "Il n'y a pas de limite de temps."
    self.cmdStartExam_note = "Remarques:"
    self.cmdStartExam_noteDesc = "Il peut arriver que tu répondes trop vite à une question et que le bot reste " \
                                 "bloqué. Pour le débloquer, il faut que tu enlèves et remettes ta réponse. Pour " \
                                 "éviter pareil cas, attend bien que toutes les réactions s'affichent avant de " \
                                 "répondre. Pour tout problème, n'hésites pas à contacter RaideOne."
    self.cmdStartExam_ResultTitle = "Résultat:"
    self.cmdStartExam_better = "Ton score pour cette session est de {0}/20. Tu as battu ton précédent meilleur score " \
                               "de {1}/20."
    self.cmdStartExam_bad = "Ton score pour cette session est de {0}/20. Tu n'as pas battu ton meilleur score de " \
                            "{1}/20."
    self.cmdStartExam_best = "Félicitations!!! Tu as réalisé un score parfait de {0}/20. Factorio n'a plus de secret " \
                             "pour toi désormais. Ton précédent meilleur score était de {1}/20."

    # quizList
    self.cmdQuizList_difficulty = "Difficulté"

    # admin ============================================================
    # show_config

    # edit_config
    self.cmdEditConfig_syntaxError = "n'est pas un élément de la config. Veuillez vérifier la syntaxe!"
    self.cmdEditConfig_alrdyConfigured = "est déjà configuré en"
    self.cmdEditConfig_unSupportedLang = "n'est pas un langage supporté.\nSont supportés:"
    self.cmdEditConfig_configured = "est désormais configuré en"
