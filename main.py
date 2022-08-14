# coding=utf-8
from ProcessCommande import ProcessCommande, passSudo
from criticalEquipment.CriticalEquipment import CriticalEquipment
from documentGenerator.DocumentMarkdown import DocumentMarkdown
from networkMapper.NetworkMapper import NetworkMapper
from smbSecurity.SmbSecurity import SmbSecurity
from vulnerability.Vulnerability import *
from wireshark.Wireshark import Wireshark
import pyfiglet


def sayHello():
    print("\033[1;32m Bienvenue dans l'application d'analyse de sécurité DIS \n")

def banner():
    print(pyfiglet.figlet_format("D I S - Security"))

def menu(commadeProcessor, document):
    print("\n")
    banner()
    print("\033[1;32m-------------------------Menu principal------------------------\n")
    print("1. Analyse de trame avec Wireshark\n")
    print("2. Analyse de faille de sécurité\n")
    print("3. Cartographie du réseau avec Zenmap\n")
    print("4. Identification des équipements critiques\n")
    print("5. Sécurisation des partages SMB\n")
    print("6. Quitter et sauvgarder le document\n")
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
        SmbSecurity(commadeProcessor, document)
        return True
    elif choix == "6":
        document.write()
        print("\033[1;32m Au revoir ! \n")
        return False
    else:
        print("\033[1;31m Choix invalide \n")
        return True



if __name__ == '__main__':
    sayHello()
    #docname = input("Entrez le nom du document à générer: ")
    docname = "test"
    document = DocumentMarkdown(docname)
    #sudoPassword = input("Entrez le mot de passe sudo: ")
    sudoPassword = "kali"
    commadeProcessor = ProcessCommande(sudoPassword=sudoPassword) # create an instance of the class ProcessCommande
    adresse = "192.168.0.70"#input("Saisisez l'adresse de la machine à scanner => ")
    #wifi_attaque(commadeProcessor)
    while menu(commadeProcessor, document) == True:
        pass




