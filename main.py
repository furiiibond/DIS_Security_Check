# coding=utf-8
from ProcessCommande import ProcessCommande, passSudo
from documentGenerator.DocumentMarkdown import DocumentMarkdown
from networkMapper.NetworkMapper import NetworkMapper
from vulnerability import *
from wireshark.Wireshark import Wireshark


def sayHello():
    print("\033[1;32m Bienvenue dans l'application d'analyse de sécurité DIS \n")



def menu(commadeProcessor, document):
    print("-------------------------------------------------")
    print("\033[1;32m Menu principal \n")
    print("1. Analyse de trame avec Wireshark")
    print("2. Analyse de faille de sécurité")
    print("3. Cartographie du réseau avec Zenmap")
    print("4. Identification des équipements critiques")
    print("5. Quitter et sauvgarder le document")
    choix = input("Votre choix : ")
    if choix == "1":
        Wireshark(commadeProcessor, document)
        return True
    elif choix == "2":
        Vulnerability(commadeProcessor, document)
        return True
    elif choix == "3":
        NetworkMapper(commadeProcessor, document)
        return True
    elif choix == "4":
        CriticalEquipment(commadeProcessor, document)
        return True
    elif choix == "5":
        document.write()
        print("\033[1;32m Au revoir ! \n")
        return False



if __name__ == '__main__':
    sayHello()
    docname = input("Entrez le nom du document à générer: ")
    document = DocumentMarkdown(docname)
    commadeProcessor = ProcessCommande() # create an instance of the class ProcessCommande
    #passSudo(commadeProcessor) # sudo mode
    adresse = "192.168.0.70"#input("Saisisez l'adresse de la machine à scanner => ")
    #wifi_attaque(commadeProcessor)
    while menu(commadeProcessor, document) == True:
        pass




