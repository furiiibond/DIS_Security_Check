import unittest

from utils import getAllHostsOnNetwork, getOSOfHost


class TestUtils(unittest.TestCase):
    def test_hosts_on_network(self):
        hosts = getAllHostsOnNetwork("192.168.0.*")
        # affichage des ipV4 des machines sur le réseau
        for host in hosts:
            print(host)
        # test si il y as plus de 2 hosts
        self.assertGreater(len(hosts), 2)

    def test_getOSOfHost(self):
        print(getOSOfHost("192.168.0.70"))
        print(getOSOfHost("192.168.0.123"))
        print(getOSOfHost("192.168.0.99"))
        print(getOSOfHost("192.168.0.1"))
        print(getOSOfHost("192.168.0.121"))
        print(getOSOfHost("192.168.0.20"))


if __name__ == '__main__':
    unittest.main()
