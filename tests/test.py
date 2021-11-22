import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import unittest 
import oimdp
from oimdp.structures import BioOrEvent, DictionaryUnit, DoxographicalItem, Editorial, Hukm, Isnad, Line, Matn, MorphologicalPattern, PageNumber, Paragraph, Riwayat, TextPart


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

    def generic_check(self, datatype, location: int, type: str, property: str = ""):
            content = self.parsed.content[location]
            self.assertTrue(isinstance(content, datatype))
            if (len(property) > 0):
                self.assertEqual(getattr(content, property), type)

    def test_magic(self):
        self.assertEqual(str(self.parsed.magic_value), "######OpenITI#")

    def test_meta(self):
        self.assertEqual(str(self.parsed.simple_metadata[1]),
                         "000.SortField	:: Shamela_0023833")
        self.assertEqual(str(self.parsed.simple_metadata[-1]),
                         "999.MiscINFO	:: NODATA")

    def test_page(self):
        self.assertTrue(isinstance(self.parsed.content[1].parts[1], 
                        PageNumber))
        self.assertEqual(str(self.parsed.content[1].parts[1]),
                         "Vol. 00, p. 000")

    def test_bio_or_event(self):
        def check(location: int, type: str):
            self.generic_check(BioOrEvent, location, type, "be_type")

        check(2, "man")
        self.assertEqual(str(self.parsed.content[3].parts[0]),
            " أبو عمرو ابن العلاء واسمه")
        check(8, "man")
        self.assertEqual(str(self.parsed.content[9].parts[0]),
            " أبو عمرو ابن العلاء واسمه")
        check(14, "wom")
        self.assertEqual(str(self.parsed.content[15].parts[0]),
            " 1729 - صمعة بنت أحمد بن محمد بن عبيد الله الرئيس النيسابورية من ولد عثمان بن")
        check(17, "wom")
        self.assertEqual(str(self.parsed.content[18].parts[0]),
            " 1729 - صمعة بنت أحمد بن محمد بن عبيد الله الرئيس النيسابورية من ولد عثمان بن")
        check(20, "ref")
        self.assertEqual(str(self.parsed.content[21].parts[0]),
            " [a cross-reference, for both men and women]")
        check(23, "ref")
        self.assertEqual(str(self.parsed.content[24].parts[0]),
            " [a cross-reference, for both men and women]")
        check(26, "names")
        self.assertEqual(str(self.parsed.content[27].parts[0]),
            " -وفيها ولد: (@)(@@) المحدث عفيف ")
        check(29, "names")
        self.assertEqual(str(self.parsed.content[30].parts[0]),
            " -وفيها ولد: (@)(@@) المحدث عفيف ")
        check(32, "events")
        check(34, "event")
        check(49, "man")

    def test_dictionary_unit(self):
        def check(location: int, type: str):
            self.generic_check(DictionaryUnit, location, type, "dic_type")
        
        check(36, "nis")
        check(38, "top")
        check(40, "lex")
        check(42, "bib")

    def test_doxographical(self):
        def check(location: int, type: str):
            self.generic_check(DoxographicalItem, location, type, "dox_type")

        check(44, "pos")
        check(46, "sec")

    def test_editorial(self):
        self.assertTrue(isinstance(self.parsed.content[48], Editorial))

    def test_morphological(self):
        self.assertTrue(isinstance(self.parsed.content[50], MorphologicalPattern))
        self.assertTrue(self.parsed.content[50].category, "onomastic")
    
    def test_paragraph(self):
        self.assertTrue(isinstance(self.parsed.content[51], Paragraph))

    def test_line(self):
        self.assertTrue(isinstance(self.parsed.content[52], Line))
        self.assertTrue(isinstance(self.parsed.content[53], Line))
        ## Check line parts on 53

    def test_riwayat(self):
        self.assertTrue(isinstance(self.parsed.content[54], Riwayat))
        self.assertTrue(isinstance(self.parsed.content[55], Line))
        self.assertTrue(isinstance(self.parsed.content[55].parts[0], Isnad))
        self.assertTrue(isinstance(self.parsed.content[55].parts[1], TextPart))
        self.assertEqual(self.parsed.content[55].parts[1].orig, " this section contains isnād ")
        
        self.assertTrue(isinstance(self.parsed.content[55].parts[2], Matn))
        self.assertTrue(isinstance(self.parsed.content[55].parts[3], TextPart))
        self.assertEqual(self.parsed.content[55].parts[3].orig, " this section")

        self.assertTrue(isinstance(self.parsed.content[56], Line))
        self.assertTrue(isinstance(self.parsed.content[56].parts[0], TextPart))
        self.assertEqual(self.parsed.content[56].parts[0].orig, " contains matn ")

        self.assertTrue(isinstance(self.parsed.content[56].parts[1], Hukm))
        self.assertTrue(isinstance(self.parsed.content[56].parts[2], TextPart))
        self.assertEqual(self.parsed.content[56].parts[2].orig, " this section contains ḥukm .")
        


    # TODO: other tests.

    # def test_clean_text(self):
    #     text = self.parsed.get_clean_text(True)
    #     # print(text)


if __name__ == "__main__":
    unittest.main()
