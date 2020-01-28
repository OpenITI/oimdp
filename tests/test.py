import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import unittest
import oimdp
from oimdp.structures import PageNumber, Paragraph


class TestStringMethods(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestStringMethods, self).__init__(*args, **kwargs)
        root = os.path.dirname(__file__)
        filepath = os.path.join(
            root, "test.md"
        )
        test_file = open(filepath, "r")
        self.text = test_file.read()
        test_file.close()
        self.parsed = oimdp.parse(self.text)

    def test_magic(self):
        self.assertEqual(str(self.parsed.magic_value), "######OpenITI#")

    def test_meta(self):
        self.assertEqual(str(self.parsed.simple_metadata[0]),
                         "000.SortField	:: Shamela_0023833")
        self.assertEqual(str(self.parsed.simple_metadata[-1]),
                         "999.MiscINFO	:: NODATA")

    def test_page(self):
        for content in self.parsed.content:
            if (isinstance(content, PageNumber)):
                self.assertEqual(str(content), "Vol. 00, p. 000")
                break

    # def test_para(self):
    #     for content in self.parsed.content:
    #         if (isinstance(content, Paragraph)):
    #             print(content.lines[1])
    #             break

    # TODO: other tests.

    def test_clean_text(self):
        text = self.parsed.get_clean_text(True)
        # print(text)


if __name__ == "__main__":
    unittest.main()
