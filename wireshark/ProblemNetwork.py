from vulnerability import getNetbiosName


class ProblemNetwork:
    def __init__(self, ipAddress, commadeProcessor, commentaire=None):
        self.ipAddress = ipAddress
        self.commadeProcessor = commadeProcessor
        self.commentaire = commentaire
        self.getName()

    def getName(self):
        self.scanName = getNetbiosName(self.commadeProcessor, self.ipAddress)

    def toDocument(self, document):
        document.writeTextLine("L'équipement suivant est problématique. \n")
        document.addCode("nom de équipement problématique", self.scanName)
        if self.commentaire:
            document.writeTextLine("Commentaire supplementaire : " + self.commentaire)