from notion.client import NotionClient
from notion.block import PageBlock
from md2notion.upload import upload


class NotionUploader:
    def __init__(self, notion_token, notion_page_id):
        self.notion_token = notion_token
        self.notion_page_id = notion_page_id

    def upload(self, docUri, title):
        # Follow the instructions at https://github.com/jamalex/notion-py#quickstart to setup Notion.py
        client = NotionClient(
            token_v2=self.notion_token)
        page = client.get_block(self.notion_page_id)

        with open(docUri, "r", encoding="utf-8") as mdFile:
            newPage = page.children.add_new(PageBlock, title=title)
            upload(mdFile, newPage)  # Appends the converted contents of TestMarkdown.md to newPage
