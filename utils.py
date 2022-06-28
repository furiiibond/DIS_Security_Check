import os

def executeCommande(commande):
    print('Execution de la commande "' + commande +'"')
    result = os.popen(commande).read()
    return result