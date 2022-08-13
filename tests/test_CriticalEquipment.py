import unittest

from ProcessCommande import ProcessCommande
from criticalEquipment.CriticalEquipment import CriticalEquipment
from documentGenerator.DocumentMarkdown import DocumentMarkdown


class TesCriticalEquipent(unittest.TestCase):
    def testOldWindows(self):
        commadeProcessor = ProcessCommande()
        document = DocumentMarkdown("testOldWindows.md")
        criticalEquipment = CriticalEquipment(commadeProcessor, document, True)
        criticalEquipment.detectOsProblem("192.168.0.1")
        criticalEquipment.detectOsProblem("192.168.0.70")
        criticalEquipment.detectOsProblem("192.168.0.20")



if __name__ == '__main__':
    unittest.main()
