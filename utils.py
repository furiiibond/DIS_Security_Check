import signal

import nmap
import readchar

def getAllHostsOnNetwork(network):
    """
    Get all hosts on a network
    """
    nm = nmap.PortScanner()
    nm.scan(network, arguments='-sP')
    hosts = []
    for host in nm.all_hosts():
        hosts.append(host)
    print("Il y as " + str(len(hosts)) + " machines sur le réseau " + network)
    return hosts

def getOSOfHost(ip):
    """
    Get OS of all hosts on a ip
    """
    nm = nmap.PortScanner()
    print("Detection de l'OS de " + ip)
    scan = nm.scan(ip, arguments="-O --osscan-guess --fuzzy -Pn -F --max-retries 1")
    if len(scan['scan'][ip]['osmatch']) > 0:
        return scan['scan'][ip]['osmatch'][0]['name'], scan['scan'][ip]['osmatch'][0]['accuracy']

def getSMBHostsOnNetwork(network):
    """
    Get all hosts on a network
    """
    nm = nmap.PortScanner()
    nm.scan(network, arguments='-p445 --open -Pn')
    hosts = nm.all_hosts()
    print("Il y as " + str(len(hosts)) + " machines avec partage de fichier samba sur le réseau " + network)
    return hosts

def isNetwork(network):
    """
    Check if the ipv4 adress is a network or a host
    :param network:
    :return:
    """
    return "*" in network or "-" in network

def getNetbiosName(commadeProcessor, ipv4):
    commande = 'sudo nmap -sU --script nbstat.nse -p137 ' + ipv4
    return commadeProcessor.execute(commande)

def sigintHandler(commandeProcessor, document, signum, frame):
    killed = commandeProcessor.sigint()
    if not killed: # no process was killed
        msg = "On a appuyé sur Ctrl-c. Voulez-vous vraiment quitter DIS-Security? y/n "
        print(msg, end="", flush=True)
        res = readchar.readchar()
        if res == 'y':
            print("")
            print("Sauvegarde du document")
            document.write()
            exit(1)
        else:
            print("", end="\r", flush=True)
            print(" " * len(msg), end="", flush=True) # clear the printed line
            print("    ", end="\r", flush=True)