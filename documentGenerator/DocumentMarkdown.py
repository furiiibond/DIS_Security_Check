from documentGenerator.markdowngenerator import MarkdownGenerator

class DocumentMarkdown:
    def __int__(self, documentName):
        with MarkdownGenerator(
                # By setting enable_write as False, content of the file is written
                # into buffer at first, instead of writing directly into the file
                # This enables for example the generation of table of contents
                filename=documentName+".md", enable_write=False
        ) as self.doc:
            self.doc.addHeader(1, documentName)

    def addCode(self, title, code):
        self.doc.addHeader(2, title)
        self.doc.addCodeBlock(code)