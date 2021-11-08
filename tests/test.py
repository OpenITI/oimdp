import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import unittest 
import oimdp
from oimdp.structures import BioOrEvent, DictionaryUnit, PageNumber, Paragraph


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

    def generic_check(self, datatype, location: int, type: str, lines_at_least: int = 0, val: str = "", property: str = ""):
            content = self.parsed.content[location]
            self.assertTrue(isinstance(content, datatype))
            if (len(property) > 0):
                self.assertEqual(getattr(content, property), type)
            self.assertGreaterEqual(len(content.lines), lines_at_least)
            if len(val) > 0:
                self.assertEqual(content.value, val)

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
        def check(location: int, type: str, lines_at_least: int, val: str = ""):
            self.generic_check(BioOrEvent, location, type, lines_at_least, val, "be_type")

        check(1, "man", 2, " أبو عمرو ابن العلاء واسمه")
        check(2, "man", 2, " أبو عمرو ابن العلاء واسمه")
        check(3, "wom", 2, " 1729 - صمعة بنت أحمد بن محمد بن عبيد الله الرئيس النيسابورية من ولد عثمان بن")
        check(4, "wom", 2, " 1729 - صمعة بنت أحمد بن محمد بن عبيد الله الرئيس النيسابورية من ولد عثمان بن")
        check(5, "ref", 2, " [a cross-reference, for both men and women]")
        check(6, "ref", 2, " [a cross-reference, for both men and women]")
        check(7, "names", 2, " -وفيها ولد: (@)(@@) المحدث عفيف ")
        check(8, "names", 2, " -وفيها ولد: (@)(@@) المحدث عفيف ")
        check(9, "events", 2)
        check(10, "event", 2)

    def test_dictionary_unit(self):
        def check(location: int, type: str, lines_at_least: int, val: str = ""):
            self.generic_check(DictionaryUnit, location, type, lines_at_least, val, "dic_type")
        
        check(11, "nis", 2)
        check(12, "top", 2)
        check(13, "lex", 2)
        check(14, "bib", 2)

    # TODO: other tests.

    # def test_clean_text(self):
    #     text = self.parsed.get_clean_text(True)
    #     # print(text)


if __name__ == "__main__":
    unittest.main()
