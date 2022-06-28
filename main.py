from documentGenerator.DocumentMarkdown import DocumentMarkdown
from vulnerability import nmapVul


def sayHello():
    print("\033[1;32m Binvenue dans l'aplication d'analyse de sécurité DIS \n")

if __name__ == '__main__':
    sayHello()
    adresse = input("Saisisez l'adresse de la machine à scanner => ")
    document = DocumentMarkdown("testScanResult")
    scanResult = nmapVul(adresse)
    document.addCode("Scan de Vulnérabilité", scanResult)
