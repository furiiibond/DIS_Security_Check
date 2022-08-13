import unittest

from documentGenerator.NotionUploader import NotionUploader


class MyTestCase(unittest.TestCase):
    def test_upload(self):
        notionUploader = NotionUploader("2261eb1e02d1433d4130991505384d7a6c29d9d83ca6abf09355b5c7616c9a6c5f65ec406676b13eae22ea60a4037063a6ab3c99ddc00aa0570ba11f3bd1bb5852153d3c46d7b05c0f68bd9d3a89","34ae2723e5b043ed929a6e8466ef9288")
        notionUploader.upload("/home/kali/PycharmProjects/DIS_Security_Check/test.md", "test Upload")



if __name__ == '__main__':
    unittest.main()
