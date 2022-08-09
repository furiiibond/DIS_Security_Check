from utils import getAllHostsOnNetwork, getOSOfHost


class CriticalEquipment:
    def __init__(self, commadeProcessor, document):
        self.commadeProcessor = commadeProcessor
        self.document = document
        self.init()
        self.oldWindows = []
        self.oldWindowsList = []
        self.wifi = []
        self.brutex = []
        while self.menu():
            pass

    def init(self): # explanations of the program
        print("-----------------Identification des équipements critiques-----------------")

    def menu(self):
        print("1. Detection des anciennes versions de Windows")
        print("2. Analyse de la sécurité du wifi avec Wifite")
        print("3. Attaque par brutforce et detection des mot de passes simple (ftp, smb ...) avec Brutex")
        print("4. Quitter et sauvgarder le document")
        choix = input("Votre choix : ")
        if choix == "1":
            self.detectionAnciennesVersionsWindows()
            return True
        elif choix == "2":
            self.analyseSecuriteWifi()
            return True
        elif choix == "3":
            self.attaqueBrutforce()
            return True
        elif choix == "4":
            self.toDocument()
            print("\033[1;32m Au revoir ! \n")
            return False

    def detectionAnciennesVersionsWindows(self):
        self.readFromFileOldOS()
        print("-------------------------------------------------")
        print("\033[1;32m Detection des anciennes versions de Windows \n")
        print("La detection des anciennes versions de windows permet d'identifier les machines sous des versions de windows obsolètes ou à sécurité faible.")
        print("Pour cela, nous utilisons la commande 'sudo nmap [adresse] -O --osscan-guess --fuzzy -Pn'")
        print("cette operation est longue et peut prendre du temps")
        yn = input("voulez vous continuer ? (y/n)")
        if yn == "y" or yn == "Y":
            ip = input("Saisisez l'adresse de la machine ou du réseau à scanner exemple : [192.168.0.*] => ")
            if "*" or "-" in ip: # networkMode
                hosts = getAllHostsOnNetwork(ip)
                for i, host in enumerate(hosts):
                    print("Progression : {}/{}".format(i, len(hosts)))
                    self.oldWindows.append(self.detectOsProblem(host))
            else: # singleMachine
                self.oldWindows.append(self.detectOsProblem(ip))
            print("\033[1;32m L'analyse des anciennes versions de Windows est terminée \n")

    def readFromFileOldOS(self):
        try:
            # read old windows name from file oldWindows.txt
            with open("oldWindows.txt", "r") as file:
                for line in file:
                    self.oldWindowsList.append(line.strip())
        except FileNotFoundError:
            print("\033[1;31m Le fichier oldWindows.txt n'existe pas \n")
            exit()

    def detectOsProblem(self, host):
        (os, acuracy) = getOSOfHost(host)
        if any(osName in os for osName in self.oldWindowsList): # if os is in oldWindowsList
            print("\033[1;32m La machine suivante semble avoir une version de windows obsoletes : \n")
            self.oldWindows.append([host, os, acuracy])
            print("Ipv4 : " + host)
            print("OS : " + os)
            print("fiabilité : " + acuracy + " %\n")
            return [host, os, acuracy]
        else:
            print("Os : " + os + " - fabilité " + acuracy + " %\n" + "La version de la machine n'est pas obsolète")

    def analyseSecuriteWifi(self):
        print("-------------------------------------------------")
        print("\033[1;32m Analyse de la sécurité du wifi avec Wifite \n")
        print("L'analyse de la sécurité du wifi permet de déterminer si le réseau est vulnerable à une attaque simple par dictionnaire")
        print("Pour cela, nous utilisons la commande 'sudo wifite'")
        print("Wifite est automatisé neanmoins, il est possible de passer les premières analyses qui donnent raraementr suite au déchiffrage de clé")
        print("Veuillez installer une interface wifi compatible 'monitor mode' pour pouvoir utiliser Wifite")
        yn = input("voulez vous continuer ? (y/n)")
        if yn == "y" or yn == "Y":
            results = self.commadeProcessor.execute("sudo wifite")
            print("\033[1;32m L'analyse de la sécurité du wifi est terminée \n")
            yn = input("Le mot de passe du wifi à t'il été déchiffré ? (y/n)")
            if yn == "y" or yn == "Y":
                print("\033[1;32m Le mot de passe du wifi à été déchiffré \n")
                ssid = input("Saisisez le nom du réseau wifi : ")
                password = input("Saisisez le mot de passe du réseau wifi : ")
                self.wifi.append([ssid, password, results])
            else:
                print("\033[1;32m Le mot de passe du wifi n'a pas été déchiffré \n")
                ssid = input("Saisisez le nom du réseau wifi : ")
                self.wifi.append([ssid, False, False])

    def attaqueBrutforce(self):
        print("-------------------------------------------------")
        print("\033[1;32m Attaque par brutforce et detection des mot de passes simple (ftp, smb ...) avec Brutex \n")
        print("L'attaque par brutforce permet de déterminer si les machines du réseau sont sensibles à des attaque simple par dictionnaire")
        print("Pour cela, nous utilisons la commande 'sudo brutex'")
        yn = input("voulez vous continuer ? (y/n)")
        if yn == "y" or yn == "Y":
            ip = input("Saisisez l'adresse de la machine ou du réseau à scanner exemple : [192.168.0.*] => ")
            if "-" or "*" in ip: # network scan
                hosts = getAllHostsOnNetwork(ip)
                for i, host in enumerate(hosts):
                    print("----------------------------------------------------")
                    print("\033[1;32m Analyse de la machine : " + host + " \n")
                    print("état d'avancement : " + str(i) + "/" + str(len(hosts)) + " machine(s) analysée(s)")
                    result = self.commadeProcessor.execute("sudo brutex " + host)
                    if "valid password found" in result:
                        lines = result.split("\n")
                        for line in lines:
                            if "login:" and "password:" in line:
                                self.brutex.append([ip, line])
                                print("\033[1;32m Un mot de passe de la machine " + host + " a été trouvé \n")
                                print(line)
            else: # single host scan
                result = self.commadeProcessor.execute("sudo brutex" + ip)
                if "valid password found" in result:
                    lines = result.split("\n")
                    for line in lines:
                        if "login:" and "password:" in line:
                            self.brutex.append([ip, line])
                    print("\033[1;32m Un mot de passe d'une machine à été déchiffré \n")
            print("\033[1;32m L'attaque par brutforce est terminée \n")



    def toDocument(self):
        self.document.headerOne("équipements critiques")
        self.document.headerTwo("Anciennes versions de Windows")
        for [host, os, acuracy] in self.oldWindows:
            self.document.writeTextLine("La machine suivante semble avoir des anciennes versions de windows : ")
            self.document.writeTextLine("Ipv4 : " + host)
            self.document.writeTextLine("OS : " + os)
            self.document.writeTextLine("fiabilité : " + acuracy + " %\n")
        self.document.headerTwo("Sécurité du wifi")
        for [network, password, details] in self.wifi:
            if password:
                self.document.writeTextLine("Le réseau " + network + " a été déchiffré avec le mot de passe : " + password)
                self.document.writeTextLine("Les détails de l'attaque : ")
                self.document.addCode(details)
            else:
                self.document.writeTextLine("Le réseau " + network + " n'a pas été déchiffré")
        self.document.headerTwo("Attaque par brutforce et detections des mots de passes simples des machines du réseau")
        for [ip, details] in self.brutex:
            self.document.writeTextLine("Un des services de la machine " + ip + " a été déchiffré : ")
            self.document.addCode(details)


