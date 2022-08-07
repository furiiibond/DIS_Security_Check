class CriticalEquipment:
    def __init__(self, commadeProcessor, document):
        self.commadeProcessor = commadeProcessor
        self.document = document
        self.init()
        while self.menu():
            pass

    def init(self): # explanations of the program
        print("-----------------Identification des équipements critiques-----------------")

    def menu(self):
        print("-------------------------------------------------")
        print("1. Detection des anciennes versions de Windows")
        print("2. Analyse de la sécurité du wifi avec Wifite")
        print("3. Attaque par brutforce et detection des mot de passes simple (ftp, smb ...) avec Brutx")
        print("4. Quitter et sauvgarder le document")
        choix = input("Votre choix : ")
        if choix == "1":
            self.detectionAnciennesVersionsWindows(commadeProcessor)
            return True
        elif choix == "2":
            self.analyseSecuriteWifi(commadeProcessor)
            return True
        elif choix == "3":
            self.attaqueBrutforce(commadeProcessor)
            return True
        elif choix == "4":
            self.toDocument(commadeProcessor)
            print("\033[1;32m Au revoir ! \n")
            return False

    def detectionAnciennesVersionsWindows(self):
        pass

    def analyseSecuriteWifi(self):
        pass

    def attaqueBrutforce(self):
        pass

    def toDocument(self):
        pass

