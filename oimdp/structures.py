from typing import List, Literal


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


class LinePart:
    """A line-level tag"""
    def __init__(self, orig: str):
        self.orig = orig

    def __str__(self):
        return self.orig


class TextPart(LinePart):
    """Phrase-level text"""
    def __init__(self, orig: str):
        self.orig = orig
        self.text = orig

    def __str__(self):
        return self.text


class Date(LinePart):
    """A date in running text"""
    def __init__(self, orig: str, value: str, date_type: str):
        self.orig = orig
        self.value = value
        self.date_type: Literal["birth", "death", "age", "other"] = date_type

    def __str__(self):
        return self.orig

class Age(LinePart):
    """A number indicating age in running text"""
    def __init__(self, orig: str, value: str):
        self.orig = orig
        self.value = value

    def __str__(self):
        return self.orig

class NamedEntity(LinePart):
    """A named entity"""
    def __init__(self, orig: str, prefix: int, extent: int, text: str, ne_type: str):
        self.orig = orig
        self.text = text
        self.prefix = prefix
        self.extent = extent
        self.ne_type: Literal["top", "per", "soc", "src"] = ne_type

    def __str__(self):
        return self.text


class OpenTagUser(LinePart):
    """A custom tag added by a specific user"""
    def __init__(self, orig: str, user: str, t_type: str, t_subtype: str, t_subsubtype: str):
        self.orig = orig
        self.user = user
        self.t_type = t_type
        self.t_subtype = t_subtype
        self.t_subsubtype = t_subsubtype

    def __str__(self):
        return self.value


class OpenTagAuto(LinePart):
    """A custom tag added automatically"""
    def __init__(self, orig: str, resp: str, t_type: str, category: str, review: str):
        self.orig = orig
        self.resp = resp
        self.t_type = t_type
        self.category = category
        self.review = review

    def __str__(self):
        return self.value


class Milestone(LinePart):
    """Milestone typically used for splitting text in 300-word blocks"""
    def __str__(self):
        return ""


class Isnad(LinePart):
    """An isnād part of a riwāyaŧ unit"""


class Matn(LinePart):
    """A matn part of a riwāyaŧ unit"""


class Hukm(LinePart):
    """A ḥukm part of a riwāyaŧ unit"""


class Line:
    """A line of text that may contain parts"""
    def __init__(self, orig: str, text_only: str, parts: List[LinePart] = None):
        self.orig = orig
        self.text_only = text_only
        if (parts is None):
            self.parts = []
        else:
            self.parts = parts

    def add_part(self, part: LinePart):
        self.parts.append(part)

    def __str__(self):
        return "".join([str(p) for p in self.parts])


class PageNumber():
    """A page and volume number. Can be Content or LinePart object"""
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


class Verse(Line):
    """A line of poetry"""

class Hemistich(LinePart):
    """Tags the beginning of a hemistic in a verse"""


class Paragraph(Content):
    """Marks the beginning of a paragraph"""
    def __init__(self, orig = "#"):
        self.orig = orig

    def __str__(self):
        return ""

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
    def __init__(self, orig: str, dic_type: str):
        self.orig = orig
        self.dic_type: Literal["nit", "top", "lex", "bib"] = dic_type

    def __str__(self):
        return ""


class BioOrEvent(Content):
    """Marks a biography or an event"""
    def __init__(self, orig: str, be_type: str):
        self.orig = orig
        self.be_type: Literal["man", "wom", "ref", "names", "event", "events"] = be_type

    def __str__(self):
        return ""


class DoxographicalItem(Content):
    """Marks a doxographical section"""
    def __init__(self, orig: str, dox_type: str):
        self.orig = orig
        self.dox_type: Literal["pos", "sec"] = dox_type

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


class RouteOrDistance(Line):
    """A route or distance"""


class RouteFrom(LinePart):
    """Origin of a Route"""


class RouteTowa(LinePart):
    """Destination of a Route"""


class RouteDist(LinePart):
    """Distance of a Route"""


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
