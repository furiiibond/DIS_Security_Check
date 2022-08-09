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