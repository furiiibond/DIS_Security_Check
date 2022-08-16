class ActiveDirectory:
    def __init__(self, commadeProcessor, document):
        self.commadeProcessor = commadeProcessor
        self.document = document
        self.init()
        self.askCredentials()
        self.shares = None
        self.users = None
        self.groups = None
        self.passPol = None
        self.sessions = None
        while self.menu():
            pass
        self.toDocument()


    def init(self):
        print("\n")
        print(
            "\033[1;32m-----------------[5] Active Directory : Politique des mots de passes et GPO-----------------\n")

    def menu(self):
        self.init()
        print("1 - Lister toutes les partages samba du server\n")
        print("2 - Lister les utilisateurs Active Directory\n")
        print("3 - Lister les groupes Active Directory\n")
        print("4 - Politique de mots de passe Active Directory\n")
        print("5 - Executer une commande cmd sur le serveur\n")
        print("6 - Executer une commande PowerShell sur le serveur\n")
        print("7 - Voir les sessions actives\n")
        print("8 - Deconnecter un utilisateur\n")
        print("9 - Activer/Desactiver le rdp\n")
        print("10 - Changer les identifiants de connection Active Directory\n")
        print("11 - Quitter et sauvgarder le document\n")
        choice = input("Saisissez votre choix : ")
        if choice == "1":
            self.listShares()
            return True
        elif choice == "2":
            self.listUsers()
            return True
        elif choice == "3":
            self.listGroups()
            return True
        elif choice == "4":
            self.passwordPolicy()
            return True
        elif choice == "5":
            self.sendCmd()
            return True
        elif choice == "6":
            self.powershell()
            return True
        elif choice == "7":
            self.listSessions()
            return True
        elif choice == "8":
            self.disconnectUser()
            return True
        elif choice == "9":
            self.rdp()
            return True
        elif choice == "10":
            self.askCredentials()
            return True
        elif choice == "11":
            return False
        else:
            print("\033[1;31mChoix invalide\033[1;m")
            return True

    def listShares(self):
        self.shares = self.crackmapexec("--shares")

    def listUsers(self):
        self.users = self.crackmapexec("--users")

    def listGroups(self):
        self.groups = self.crackmapexec("--group")

    def passwordPolicy(self):
        self.passPol = self.crackmapexec("--pass-pol")


    def askCredentials(self):
        """ Ask the user for the credentials to connect to the Active Directory """
        print("Veuillez saisir vos identifiants Active Directory\n")
        self.serverIP = input("Adresse IP du serveur : ")
        self.username = input("Nom d'utilisateur : ")
        self.password = input("Mot de passe : ")

    def crackmapexec(self, parameters, noWait=False):
        """ Launch crackmapexec with the given parameters """
        self.commadeProcessor.execute("crackmapexec smb {} -u {} -p {} {}".format(self.serverIP, self.username, self.password, parameters), noWait, True)

    def executeCmd(self, cmd, noWait=False):
        """ Execute a command on the server """
        self.crackmapexec('-x "{}"'.format(cmd), noWait)

    def sendCmd(self):
        """ Send a cmd command to the server """
        cmd = input("Saisissez votre commande : ")
        self.executeCmd(cmd)

    def powershell(self):
        """" Send a powershell command to the server """
        cmd = input("Saisissez votre commande : ")
        self.crackmapexec(self.crackmapexec('-X "{}"'.format(cmd)))

    def listSessions(self):
        """ List all the active sessions on the server """
        self.sessions = self.executeCmd('quser')

    def disconnectUser(self):
        """ Disconnect a user from the server """
        self.listSessions() # List all the active sessions
        num = input("Saisissez le numero de session a deconnecter : ")
        self.executeCmd("logoff {}".format(num), True)

    def rdp(self):
        """ Enable/Disable RDP """
        endi = input("Voulez vous activer le RDP ? (a/d) : ")
        if endi == "a":
            self.crackmapexec("-M rdp -o ACTION=enable")
        elif endi == "d":
            self.crackmapexec("-M rdp -o ACTION=disable")
        else:
            print("\033[1;31mChoix invalide\033[1;m")

    def toDocument(self):
        print("-----------------Sauvgarde du document-----------------")
        self.document.headerOne("Active Directory")
        self.document.writeTextLine("IP du serveur : {}".format(self.serverIP))
        if self.shares is not None:
            self.document.addCode("Partages samba", self.shares)
        if self.users is not None:
            self.document.addCode("Utilisateurs Active Directory", self.users)
        if self.groups is not None:
            self.document.addCode("Groupes Active Directory", self.groups)
        if self.passPol is not None:
            self.document.addCode("Politique de mots de passe Active Directory", self.passPol)
        if self.sessions is not None:
            self.document.addCode("Sessions actives", self.sessions)


