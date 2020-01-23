from typing import List


class MagicValue:
    """Magic Value of OpenITI mARkdown file"""
    def __init__(self, orig: str):
        self.orig = orig
        self.value = "######OpenITI#"

    def __str__(self):
        return self.value


class SimpleMetadataField:
    """A non-machine readable metadata field"""
    def __init__(self, orig: str, value: str):
        self.orig = orig
        self.value = value

    def __str__(self):
        return self.value


class Line:
    """A line of text"""
    def __init__(self, orig: str, text_only: str, parts):
        self.orig = orig
        self.text_only = text_only
        self.parts = parts

    def __str__(self):
        """returns the whole line without tags"""
        return self.text_only


class Verse:
    """A line of poetry"""
    def __init__(self, orig: str, line: Line):
        self.orig = orig
        self.line = line

    def __str__(self):
        """returns the whole line without tags"""
        return self.line


class Paragraph:
    """A paragraph contaning a list of lines"""
    def __init__(self, lines: List[Line]):
        self.lines = lines

    def add_line(self, line: Line):
        self.lines.append(line)

    def __str__(self):        
        return "\n".join([str(l) for l in self.lines])


class PageNumber:
    """A page and volume number"""
    def __init__(self, orig: str, vol: str, page: str):
        self.orig = orig
        self.page = page
        self.volume = vol

    def __str__(self):
        return f"Vol. {self.volume}, p. {self.page}"


class Document:
    """The OpenITI mARkdown document"""
    def __init__(self, text):
        self.orig_text = text
        self.simple_metadata = []
        self.content = []

    def set_magic_value(self, orig: str):
        self.magic_value = MagicValue(orig)

    def set_simple_metadata_field(self, orig: str, value: str):
        self.simple_metadata.append(SimpleMetadataField(orig, value))

    def set_page_number(self, page: PageNumber):
        self.content.append(page)

    def set_paragraph(self, para: Paragraph):
        self.content.append(para)

    def set_verse_line(self, verse: Verse):
        self.content.append(verse)

    def get_clean_text(self, includeMetadata: bool = False):
        text = ""
        if (includeMetadata):
            text += "Metadata:\n"
            text += "\n".join([str(md) for md in self.simple_metadata])
            text += "\n\n"

        text += "\n".join([str(c) for c in self.content])

        return text

    def __str__(self):
        return self.orig_text
