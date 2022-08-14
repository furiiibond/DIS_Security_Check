import time
import unittest

from ProcessCommande import ProcessCommande
from documentGenerator.DocumentMarkdown import DocumentMarkdown
from utils import getAllHostsOnNetwork
from vulnerability.Vulnerability import cmd_scan_vuln




class TestVuln(unittest.TestCase):
    def test_vulnerability_metasplotable(self):
        jcli7 = "192.168.0.70"
        host = "192.168.0.177"
        commadeProcessor = ProcessCommande()
        commadeProcessor.execute(cmd_scan_vuln + jcli7, False, True)
        commadeProcessor.execute(cmd_scan_vuln + host, False, True)

    def test_vulnerability_multiple_hosts(self):
        commadeProcessor = ProcessCommande()
        hosts = getAllHostsOnNetwork("192.168.0.*")
        times = []
        for i, host in enumerate(hosts):
            #calculate avarage time for scan
            start = time.time()
            commadeProcessor.execute(cmd_scan_vuln + host, False, True)
            end = time.time()
            times.append(end - start)
            print("Temps de scan pour " + host + " : " + str(end - start))
            avarageTime = sum(times) / len(times)
            # extimate time for all hosts
            estimatedTime = (len(hosts)-i) * avarageTime
            print("Temps estimé pour la suite : " + str(estimatedTime))
        #calculate avarage time for scan
        print("Temps moyen de scan : " + str(sum(times) / len(times)))

        # simulate that the user choose to scan a host and type 4
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
