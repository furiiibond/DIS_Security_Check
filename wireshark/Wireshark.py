from vulnerability import getNetbiosName
from wireshark.ProblemNetwork import ProblemNetwork


class Wireshark:
    def __init__(self, commadeProcessor, document):
        self.commadeProcessor = commadeProcessor
        self.start()
        self.init()
        self.isBroadcastStorm = False
        self.nbPb = 0
        self.equipmentList = list() # list of equipments names by ip adress
        self.broadcastStorm() # ask if there is a broadcast storm
        self.otherEquipmentProblem()    # ask if there is a problem with other equipment
        self.generateScanResult(document) # generate the scan result

    def start(self):
        print("--------------Démarrage de wireshark--------------")
        self.commadeProcessor.execute("sudo wireshark") # start wireshark
        print("-------------------------------------------------")
        print("si wireshark n'est pas lancé, il faut lancer en tapant la commande suivante : [sudo wireshark] dans un terminal")

    def init(self):
        print("WireShark est un outil de capture de paquets qui permet de visualiser les paquets réseau envoyés et reçus par le réseau.\n")
        print("Vous allez répondre aux questions suivantes afin de poser un diagnostic du réseau")

    def broadcastStorm(self):
        print("Une tempête de broadcast est un type de paquet réseau qui est envoyé par un équipement à tous les autres équipements du réseau.\n")
        print("Regardez sur Wireshark si vous voyez une présence abondante de paquets broadcast")
        yn = input("Y/N ? ")
        if yn == "y" or yn == "Y":
            self.isBroadcastStorm = True
            self.nbPb += 1
            ip = input("Ip de l'équipement qui semble posser probleme ? ")
            self.equipementName = getNetbiosName(self.commadeProcessor, ip)

    def otherEquipmentProblem(self):
        yn = "y"
        while yn == "y" or yn == "Y":
            print("Il y a un problème avec un autre équipement")
            yn = input("Y/N ? ")
            if yn == "y" or yn == "Y":
                self.nbPb += 1
                ip = input("Ip de l'équipement qui semble poser un problème ? ")
                commentaire = input("Commentaire supplémentaire ? ")
                if commentaire == '':
                    commentaire = None
                self.equipmentList.append(ProblemNetwork(ip, self.commadeProcessor, commentaire))



    def generateScanResult(self, document):
        print("Generation du rapport de wireshark")
        document.headerTwo("Rapport de scan de wireshark")
        # broadcast storm
        if self.isBroadcastStorm:
            document.writeTextLine("L'équipement suivent semble émetre de façon anormal des paquets broadcast. \n")
            document.addCode("nom de équipement problématique", self.equipementName)
        # other equipment problem
        if len(self.equipmentList) > 0:
            document.writeTextLine("Il y a un problème avec un ou plusieurs autres équipement")
            for equipment in self.equipmentList:
                equipment.toDocument(document)










