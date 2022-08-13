from documentGenerator.markdowngenerator import MarkdownGenerator
import matplotlib
matplotlib.use('Agg')
from tkinter import Tk, filedialog
import os
import matplotlib as mpl

class DocumentMarkdown:
    def __init__(self, filename):
        self.filename = filename
        with MarkdownGenerator(
                # By setting enable_write as False, content of the file is written
                # into buffer at first, instead of writing directly into the file
                # This enables for example the generation of table of contents
                filename=filename+".md", enable_write=True
        ) as self.doc:
            pass
        self.headerOne(filename)

    def headerOne(self, text):
        self.doc.__enter__()
        self.doc.addHeader(1, text)
        self.doc.writeTextLine(f'{self.doc.addBoldedText("Scan DIS")}')

    def headerTwo(self, text):
        self.doc.__enter__()
        self.doc.addHeader(2, text)

    def headerThree(self, text):
        self.doc.__enter__()
        self.doc.addHeader(3, text)

    def addCode(self, title, code):
        self.doc.__enter__()
        self.doc.addHeader(2, title)
        self.doc.addCodeBlock(code)

    def addCodeBlock(self, code):
        self.doc.__enter__()
        self.doc.addCodeBlock(code)

    def writeSumary(self, text):
        self.doc.__enter__()
        self.doc.addHeader(3, "Résultat du scan")
        # add text block to explain the scan
        self.doc.writeTextLine(f'{self.doc.addBoldedText("Scan de la machine " + text)}')

    def writeTextLine(self, text):
        self.doc.__enter__()
        self.doc.writeTextLine(text)

    #image
    def addImage(self, altText):
        self.doc.__enter__()
        uri = self.dialogUri()
        self.doc.writeTextLine(self.doc.generateImageHrefNotation(uri, altText))


    def dialogUri(self):
        root = Tk()
        root.withdraw()
        uri = filedialog.askopenfilename(filetypes=[("Image Files", ".png .jfif, .jpg, .jpeg")])
        root.destroy()
        return uri

    def write(self):
        self.doc.__exit__()