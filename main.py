# coding=utf-8
import signal

from ProcessCommande import ProcessCommande, passSudo
from activeDirectory.ActiveDirectory import ActiveDirectory
from criticalEquipment.CriticalEquipment import CriticalEquipment
from documentGenerator.DocumentMarkdown import DocumentMarkdown
from networkMapper.NetworkMapper import NetworkMapper
from smbSecurity.SmbSecurity import SmbSecurity
from utils import sigintHandler
from vulnerability.Vulnerability import *
from wireshark.Wireshark import Wireshark
from functools import partial
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
    print("6. Active Directory : Politique des mots de passes et GPO\n")
    print("7. Quitter et sauvgarder le document\n")
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
        ActiveDirectory(commadeProcessor, document)
        return True
    elif choix == "7":
        document.write()
        print("\033[1;32m Au revoir ! \n")
        return False
    else:
        print("\033[1;31m Choix invalide \n")
        return True



if __name__ == '__main__':
    sayHello()
    docname = input("Entrez le nom du document à générer: ")
    document = DocumentMarkdown(docname)
    sudoPassword = "kali"
    commandeProcessor = ProcessCommande(sudoPassword=sudoPassword) # create an instance of the class ProcessCommande
    signal.signal(signal.SIGINT, partial(sigintHandler, commandeProcessor, document)) # On gère le CTRL+C
    adresse = "192.168.0.70"#input("Saisisez l'adresse de la machine à scanner => ")
    #wifi_attaque(commadeProcessor)
    while menu(commandeProcessor, document) == True:
        pass




