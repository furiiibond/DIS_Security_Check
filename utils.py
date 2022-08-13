import nmap
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
    nm.scan(network, arguments='-p445 -sS')
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
