import sys
import re
from .structures import Document, PageNumber, Paragraph, Line, Verse, Milestone
from .structures import SectionHeader, Editorial, DictionaryUnit, BioOrEvent
from .structures import DoxographicalItem, MorphologicalPattern, TextPart
from .structures import AdministrativeRegion, RouteOrDistance, Riwayat
from . import tags as t

PAGE_PATTERN = re.compile(r"PageV(\d+)P(\d+)")
OPEN_TAG_CUSTOM_PATTERN = re.compile(
    r"@([^@]+?)@([^_@]+?)_([^_@]+?)(_([^_@]+?))?@"
)
OPEN_TAG_AUTO_PATTERN = re.compile(
    r"@([A-Z]{3})@([A-Z]{3,})@([A-Za-z])@(-@([0tf][ftalmr])@)?"
)


def parse_tags(s: str):
    return s


def remove_phrase_lv_tags(s: str):
    text_only = s
    for tag in t.PHRASE_LV_TAGS:
        text_only = text_only.replace(tag, '')
    # Open tag
    text_only = OPEN_TAG_CUSTOM_PATTERN.sub('', text_only)
    text_only = OPEN_TAG_AUTO_PATTERN.sub('', text_only)
    text_only = PAGE_PATTERN.sub('', text_only)
    return text_only


def parse_line(tagged_il: str):
    # remove line tag
    il = tagged_il.replace(t.LINE, '')

    # get clean text
    text_only = il
    text_only = remove_phrase_lv_tags(text_only)

    line = Line(il, text_only)

    # TODO: deal with line parts, which is needed to support conversion
    # to other tag systems.

    # Split the line by tags. Make sure patterns do not include subgroups!
    tokens = re.split(rf"(PageV\d+P\d+|{t.MILESTONE})", il)

    for token in tokens:
        if (t.PAGE in token):
            m = PAGE_PATTERN.search(token)
            line.add_part(PageNumber(token, m.group(1), m.group(2)))
        elif (t.MILESTONE in token):
            line.add_part(Milestone(token))
        else:
            line.add_part(TextPart(token))
    return line


def parser(text):
    """Parses an OpenITI mARkdown file and returns a Document object"""
    document = Document(text)

    # Split input text into lines
    ilines = text.splitlines()

    # Magic value
    magic_value = ilines[0]

    if magic_value.strip() != "######OpenITI#":
        raise Exception(
            "This does not appear to be an OpenITI mARkdown document")
        sys.exit(1)

    document.set_magic_value(magic_value)

    # Structure stack
    current_structure = document

    # RE patterns
    para_pattern = re.compile(r"^#($|[^#])")    
    bio_pattern = re.compile(rf"{t.BIO_MAN}[^\w]")
    morpho_pattern = re.compile(r"#~:([^:]+?):")
    region_pattern = re.compile(
        rf"({t.PROV}|{t.REG}\d) .*? {t.GEO_TYPE} .*? ({t.REG}\d|{t.STTL}) ([\w# ]+) $"
    )
    route_pattern = re.compile(
        rf"{t.DIST_FROM} .*? {t.DIST_TO} .*? {t.DIST} .*"
    )

    # Input lines loop
    for il in ilines:

        # N.B. if order matters! We're doing string matching
        # and tag elements are re-used.

        # Non-machine readable metadata
        if (il.startswith(t.META)):
            if (il.strip() == t.METAEND):
                continue
            value = il.split(t.META, 1)[1].strip()
            document.set_simple_metadata_field(il, value)

        # Content-level page numbers
        elif (il.startswith(t.PAGE)):
            pv = PAGE_PATTERN.search(il)
            document.add_content(PageNumber(il, pv.group(1), pv.group(2)))

        # Riwāyāt units
        elif (il.startswith(t.RWY)):
            # Set first line, skipping para marker "#""
            first_line = parse_line(il[1:])
            current_structure = Riwayat([first_line])

        # Paragraphs and lines of verse
        elif (para_pattern.search(il)):
            # Set first line, skipping para marker "#""
            first_line = parse_line(il[1:])
            if (t.HEMI in il):
                # this is a verse line
                document.add_content(Verse(il, first_line))
            else:
                current_structure = Paragraph([first_line])
                document.add_content(current_structure)

        # Paragraph or Riwāyāt unit lines
        elif (il.startswith(t.LINE)):
            if (isinstance(current_structure, Paragraph) or
               isinstance(current_structure, Riwayat)):
                current_structure.add_line(parse_line(il))

        # Editorial section
        # TODO: this section contains paragraphs. Keeping as milestone for now.
        elif (il.startswith(t.EDITORIAL)):
            document.add_content(Editorial(il))

        # Section headers
        elif (il.startswith(t.HEADER1)):
            value = il
            for tag in t.HEADERS:
                value = value.replace(tag, '')
            # remove other phrase level tags
            value = remove_phrase_lv_tags(value)
            # TODO: capture tags as PhraseParts
            level = 1
            if (t.HEADER2 in il):
                level = 2
            elif (t.HEADER3 in il):
                level = 3
            elif (t.HEADER4 in il):
                level = 4
            elif (t.HEADER5 in il):
                level = 5
            document.add_content(SectionHeader(il, value, level))

        # Dictionary entry
        elif (il.startswith(t.DIC)):
            value = il
            for tag in t.DICTIONARIES:
                value = value.replace(tag, '')
            # remove other phrase level tags
            value = remove_phrase_lv_tags(value)
            # TODO: capture tags as PhraseParts
            dic_type = "bib"
            if (t.DIC_LEX in il):
                dic_type = "lex"
            elif (t.DIC_NIS in il):
                dic_type = "nis"
            elif (t.DIC_TOP in il):
                dic_type = "top"
            document.add_content(DictionaryUnit(il, value, dic_type))

        # Biographies and Events
        elif (bio_pattern.search(il) or il.startswith(t.EVENT)):
            value = il
            for tag in t.BIOS_EVENTS:
                value = value.replace(tag, '')
            # remove other phrase level tags
            value = remove_phrase_lv_tags(value)
            # TODO: capture tags as PhraseParts
            be_type = "man"
            if (t.BIO_WOM in il):
                be_type = "wom"
            elif (t.BIO_REP in il):
                be_type = "rep"
            elif (t.LIST_NAMES in il):
                be_type = "names"
            elif (t.EVENT in il):
                be_type = "event"
            elif (t.LIST_EVENTS in il):
                be_type = "events"
            document.add_content(BioOrEvent(il, value, be_type))

        # Doxographical item
        elif (il.startswith(t.DOX)):
            value = il
            for tag in t.DOXOGRAPHICAL:
                value = value.replace(tag, '')
            # remove other phrase level tags
            value = remove_phrase_lv_tags(value)
            # TODO: capture tags as PhraseParts
            be_type = "pos"
            if (t.DOX_SEC in il):
                dox_type = "sec"
            document.add_content(DoxographicalItem(il, value, dox_type))

        # Morphological pattern
        elif (morpho_pattern.search(il)):
            m = morpho_pattern.search(il)
            document.add_content(MorphologicalPattern(il, m.group(1)))

        # Regions
        elif (region_pattern.search(il)):
            document.add_content(AdministrativeRegion(il))

        # Routes
        elif (route_pattern.search(il)):
            document.add_content(RouteOrDistance(il))

        else:
            # Return current structure to document.
            current_structure = document

    return document
