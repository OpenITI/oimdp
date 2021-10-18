import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import unittest 
import oimdp
from oimdp.structures import BioOrEvent, PageNumber, Paragraph


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
        self.assertEqual(str(self.parsed.simple_metadata[1]),
                         "000.SortField	:: Shamela_0023833")
        self.assertEqual(str(self.parsed.simple_metadata[-1]),
                         "999.MiscINFO	:: NODATA")

    def test_page(self):
        self.assertTrue(isinstance(self.parsed.content[0].lines[0].parts[1], 
                        PageNumber))
        self.assertEqual(str(self.parsed.content[0].lines[0].parts[1]),
                         "Vol. 00, p. 000")

    def test_bio_or_event(self):
        bioman_full = self.parsed.content[1]
        self.assertTrue(isinstance(bioman_full, 
                        BioOrEvent))
        self.assertEqual(bioman_full.value, " أبو عمرو ابن العلاء واسمه")
        self.assertEqual(bioman_full.be_type, "man")

        bioman = self.parsed.content[2]
        self.assertTrue(isinstance(bioman, 
                        BioOrEvent))
        self.assertEqual(bioman.value, " أبو عمرو ابن العلاء واسمه")
        self.assertEqual(bioman.be_type, "man")

    # TODO: other tests.

    # def test_clean_text(self):
    #     text = self.parsed.get_clean_text(True)
    #     # print(text)


if __name__ == "__main__":
    unittest.main()
