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


class PhrasePart:
    """A phrase-level tag"""
    def __init__(self, orig: str):
        self.orig = orig

    def __str__(self):
        return self.orig


class TextPart(PhrasePart):
    """Phrase-level text"""


class NamedEntity(PhrasePart):
    """A named entity"""
    def __init__(self, orig: str, value: str, ne_type: str):
        self.orig = orig
        self.value = value
        self.ne_type = ne_type

    def __str__(self):
        return self.value


class OpenTagUser(PhrasePart):
    """A custom tag added by a specific user"""
    def __init__(self, orig: str, value: str, user: str, t_type: str):
        self.orig = orig
        self.value = value
        self.user = user
        self.t_type = t_type

    def __str__(self):
        return self.value


class OpenTagAuto(PhrasePart):
    """A custom tag added automatically"""
    def __init__(self, orig: str, value: str, resp: str,
                 t_type: str, category: str, review: str):
        self.orig = orig
        self.value = value
        self.resp = resp
        self.t_type = t_type
        self.category = category
        self.review = review

    def __str__(self):
        return self.value


class Milestone(PhrasePart):
    """Milestone typically used for splitting text in 300-word blocks"""
    def __str__(self):
        return ""


class RiwayatPart(PhrasePart):
    """Part of a riwāyaŧ unit"""
    def __init__(self, orig: str, value: str):
        self.orig = orig
        self.value = value

    def __str__(self):
        return self.value


class Isnad(RiwayatPart):
    """An isnād part of a riwāyaŧ unit"""


class Matn(RiwayatPart):
    """A matn part of a riwāyaŧ unit"""


class Hukm(RiwayatPart):
    """A ḥukm part of a riwāyaŧ unit"""


class Line:
    """A line of text, typically within a Content object"""
    def __init__(self, orig: str, text_only: str, parts: List[PhrasePart] = None):
        self.orig = orig
        self.text_only = text_only
        if (parts is None):
            self.parts = []
        else:
            self.parts = parts

    def add_part(self, part: PhrasePart):
        self.parts.append(part)

    def __str__(self):
        return "".join([str(p) for p in self.parts])


class PageNumber():
    """A page and volume number. Can be Content or PhraseLevel object"""
    def __init__(self, orig: str, vol: str, page: str):
        self.orig = orig
        self.page = page
        self.volume = vol

    def __str__(self):
        return f"Vol. {self.volume}, p. {self.page}"


class Content:
    """A content structure"""
    def __init__(self, orig: str):
        self.orig = orig

    def __str__(self):
        return self.orig


class Verse(Content):
    """A line of poetry"""
    def __init__(self, orig: str, line: Line):
        self.orig = orig
        self.line = line

    def __str__(self):
        """returns the whole line without tags"""
        return self.line


class Paragraph(Content):
    """A paragraph contaning a list of lines"""
    def __init__(self, lines: List[Line]):
        self.lines = lines

    def add_line(self, line: Line):
        self.lines.append(line)

    def __str__(self):
        return "\n".join([str(l) for l in self.lines])


class SectionHeader(Content):
    """A section header"""
    def __init__(self, orig: str, value: str, level: int):
        self.orig = orig
        self.value = value
        self.level = level

    def __str__(self):
        return self.value


class Editorial(Content):
    """Marks the beginning of an editorial section"""
    def __init__(self, orig: str):
        self.orig = orig

    def __str__(self):
        return ""


class DictionaryUnit(Content):
    """Marks a dictionary unit"""
    def __init__(self, orig: str, value: str, dic_type: str):
        self.orig = orig
        self.value = value
        self.dic_type = dic_type

    def __str__(self):
        return self.value


class BioOrEvent(Content):
    """Marks a biography or an event"""
    def __init__(self, orig: str, value: str, be_type: str):
        self.orig = orig
        self.value = value
        self.be_type = be_type

    def __str__(self):
        return self.value


class DoxographicalItem(Content):
    """Marks a doxographical section"""
    def __init__(self, orig: str, value: str, dox_type: str):
        self.orig = orig
        self.value = value
        self.dox_type = dox_type

    def __str__(self):
        return self.value


class MorphologicalPattern(Content):
    """A milestone to tag passages that can be categorized thematically."""
    def __init__(self, orig: str, category: str):
        self.orig = orig
        self.category = category

    def __str__(self):
        return ""


class AdministrativeRegion(Content):
    """An administrative region"""
    # TODO

    def __str__(self):
        return ""


class RouteOrDistance(Content):
    """A route or distance"""
    # TODO

    def __str__(self):
        return ""


class Riwayat(Paragraph):
    """Riwāyāt unit"""


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

    def add_content(self, content: Content):
        self.content.append(content)

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
