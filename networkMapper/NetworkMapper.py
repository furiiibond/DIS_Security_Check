import webbrowser


class NetworkMapper:
    def __init__(self, commadeProcessor, document):
        self.commadeProcessor = commadeProcessor
        self.document = document
        self.init()
        self.start()
        self.addImage()

    def init(self):
        print("\n--------------Explications--------------\n")
        print("Zenmap est un outil de scan de réseau qui permet d'obtenir une vue d'ensemble du réseau.\n")
        print("Une fois lancé, ajoutez dans le champs Target l'ip du réseau que vous voulez scanner")
        print("Exemple : 192.168.0.* pour scanner tout le réseau 192.168.0")
        print("Cliquez sur Scan pour lancer le scan")
        print("Dans la rubrique topologie le resultat du scan est ensuite affiché sous forme de graphe")
        print("Cliquez sur le bouton 'control' puis 'View' pour modifier l'apparence du graphe (zoom et ring gap)")
        print("Cliquez sur le bouton 'Save Graphic' pour sauvegarder le graphe dans un fichier png")
        print("Voulez-vous afficher la légende du graphe ainsi que des explications suplémentaires ?")
        yn = input("Y/N ? ")
        if yn == "y" or yn == "Y":
            webbrowser.open("https://www.notion.so/352f0532469047ab9ed955df199d8e81")
        input("Appuyez sur entrée pour lancer Zenmap...")


    def start(self):
        print("\n--------------Démarrage de Zenmap--------------\n")
        self.commadeProcessor.execute("zenmap-kbx -n nmap -F --traceroute", True) # start zenmap
        print ("-------------------------------------------------")
        print ("si zenmap n'est pas lancé, il faut lancer en tapant la commande suivante : [sudo -E zenmap-kbx -n nmap -O --traceroute] dans un terminal")

    def addImage(self):
        yn = input("Voulez-vous ajouter l'image de la topologie au document ? Y/N ")
        if yn == "y" or yn == "Y":
            print("--------------Ajout de l'image dans le document--------------")
            self.document.headerTwo("Topologie du réseau")
            self.document.addImage("Topologie du réseau")