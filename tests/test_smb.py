import unittest

from ProcessCommande import ProcessCommande
from smbSecurity.SmbSecurity import cmd_smb, cmd_smb_connected


class TestSmb(unittest.TestCase):
    def test_not_connected(self):
        commandeProcessor = ProcessCommande()
        commandeProcessor.execute(cmd_smb + "192.168.0.177")

    def test_connected(self):
        commandeProcessor = ProcessCommande()
        commandeProcessor.execute(cmd_smb_connected + "192.168.0.70 -u jcl -p password")


if __name__ == '__main__':
    unittest.main()
