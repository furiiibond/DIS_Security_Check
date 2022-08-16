import json
import webbrowser

from notion.client import NotionClient
from notion.block import PageBlock
from md2notion.upload import upload


class NotionUploader:
    def __init__(self):
        self.readParameters()

    def upload(self, docUri, title):
        # Follow the instructions at https://github.com/jamalex/notion-py#quickstart to setup Notion.py
        client = NotionClient(
            token_v2=self.notion_token)
        page = client.get_block(self.notion_page_id)

        with open(docUri, "r", encoding="utf-8") as mdFile:
            newPage = page.children.add_new(PageBlock, title=title)
            upload(mdFile, newPage)  # Appends the converted contents of TestMarkdown.md to newPage
        self.openNotionPage()

    def readParameters(self):
        with open("notionParameters.json", "r") as parametersFile:
            parameters = json.load(parametersFile)
            self.notion_token = parameters["notion_token"]
            self.notion_page_id = parameters["notion_page_id"]

    def openNotionPage(self):
        webbrowser.open("https://www.notion.so/{}".format(self.notion_page_id))
