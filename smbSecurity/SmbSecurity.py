from utils import getSMBHostsOnNetwork, isNetwork

cmd_smb = "nmap --script smb-enum-shares.nse -p445 "
cmd_smb_connected = "smbmap -H "




class SmbSecurity:
    def __init__(self, commadeProcessor, document):
        self.commadeProcessor = commadeProcessor
        self.document = document
        self.smb_enums = []  # list of smb enum results
        self.connected_smb_enums = []  # list of smb enum results with username and password
        self.explain()
        while self.menu():  # display the menu to the user
            pass
        self.toDocument()
    def explain(self):
        print("----------------Explication du module de sécurité SMB-----------------")
        print("Ce module permet de determiner les machines qui sont accessible via SMB")
        print(
            "On peut découvrir les dossiers et élement partagées via ce protocole en étant connecté (login, mot de passe)"
            " ou non (sans login et mot de passe)")

    # Explain to the user the purpose SMB scan and enumeration
    def menu(self):
        print("\n")
        print("\033[1;32m-----------------[5] Menu de sécurité SMB-----------------")
        print(
            "1 - Lister toutes les machines du réseau avec le protocole samba(smb) actif et les dossiers partager disponible sans connexion")
        print("2 - Lister les répertoires partagés sur un hôte donné via une connection ou non")
        print("3 - Quitter et sauvgarder le document")
        choice = input("Saisissez votre choix : ")
        if choice == "1":
            self.smb_multi_scan()
            return True
        elif choice == "2":
            self.smb_connect_or_not_enum()
            return True
        elif choice == "3":
            return False
        else:
            print("\033[1;31m Choix invalide \n")
            return True

    def smb_multi_scan(self):
        print("\n-----------------SMB multi scan-----------------")
        print("Determination les machines qui sont accessible via SMB")
        # ask user for network adress
        network = input("Saisissez l'adresse du réseau à scanner : ")
        print("Scan en cours sur le réseau {}".format(network))
        if not isNetwork(network):
            print("Adresse d'une machine seule")
            self.smb_enum(network)
            return
        hosts = getSMBHostsOnNetwork(network)
        # for each host, list the share available
        for i, host in enumerate(hosts):
            print("\033[1;32m Progression : {}/{}".format(i, len(hosts)))
            self.smb_enum(host)
        print("\033[1;32m Le scan est terminé \n")

    def smb_enum(self, ip):
        result = self.commadeProcessor.execute(cmd_smb + ip)
        if doNeedAuth(result):
            self.smb_enums.append((ip, result))
            print("\033[1;31m {} n'est pas accessible via SMB sans connection préalable\n".format(ip))
        else:
            print("\033[1;32m {} est accessible via SMB \n".format(ip))
            self.smb_enums.append((ip, result))

    # execute smb enum and check if it as works by cheking if result contains at least two lines
    def smb_connect_or_not_enum(self):
        print("\n-----------------Lister les répertoires partagés sur un hôte donné-----------------")
        ip = input("Saisissez l'adresse de la machine à scanner : ")
        # ask connect or not using username and password
        yn = input(" Voulez vous connecter au partage en utilisent un nom d'utilisateur et un mot de passe (y/n) : ")
        if yn == "y" or yn == "Y":
            username = input("Saisissez le nom d'utilisateur : ")
            password = input("Saisissez le mot de passe : ")
            result = self.commadeProcessor.execute(cmd_smb_connected + ip + " -u " + username + " -p " + password)
            if doNeedAuth(result):
                print(
                    "\033[1;31m {} n'est pas accessible via SMB avec le nom d'utilisateur et le mot de passe \n".format(
                        ip))
            else:
                print("\033[1;32m {} est accessible via SMB avec le nom d'utilisateur et le mot de passe \n".format(ip))
                self.connected_smb_enums.append((ip, result, username, password))
        else:
            self.smb_enum(ip)

    def toDocument(self):
        print("-----------------Sauvgarder le document-----------------")
        self.document.headerOne("Sécurité SMB")
        self.document.writeTextLine("Ce module permet de determiner les machines qui sont accessible via SMB")
        self.document.writeTextLine(
            "On peut découvrir les dossiers et élement partagées via ce protocole en étant connecté (login, mot de passe)"
            " ou non (sans login et mot de passe)")
        self.document.headerTwo(
            "Liste de toutes les machines du réseau avec le protocole samba(smb) actives et les dossiers partager disponible sans connexion")
        for (ip, result) in self.smb_enums:
            if doNeedAuth(result):
                self.document.writeTextLine(
                    "{} n'est pas accessible via SMB sans connection préalable\n".format(ip))
            else:
                self.document.writeTextLine("{} est accessible via SMB \n".format(ip))
            self.document.addCodeBlock(result)
        self.document.headerTwo("Liste des répertoires partagés sur un hôte donné via une connection")
        for (ip, result, username, password) in self.connected_smb_enums:
            self.document.writeTextLine(" {} est accessible via SMB \n".format(ip))
            self.document.writeTextLine("Nom d'utilisateur : {}".format(username))
            self.document.writeTextLine("Mot de passe : {}".format(password))
            self.document.addCodeBlock(result)


def doNeedAuth(result):
    return "Host script results:" not in result and "Disk" not in result

