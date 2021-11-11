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


def parse_line(tagged_il: str, index: int, obj=Line):
    # remove line tag
    il = tagged_il.replace(t.LINE, '')

    # get clean text
    text_only = il
    text_only = remove_phrase_lv_tags(text_only)

    if text_only == "":
        return None

    line = obj(il, text_only)

    # TODO: deal with line parts, which is needed to support conversion
    # to other tag systems.

    # Split the line by tags. Make sure patterns do not include subgroups!
    tokens = re.split(rf"(PageV\d+P\d+|{t.MILESTONE})", il)

    for token in tokens:
        if (t.PAGE in token):
            m = PAGE_PATTERN.search(token)
            try:
                line.add_part(PageNumber(token, m.group(1), m.group(2)))
            except Exception:
                raise Exception(
                    'Could not parse page number at line: ' + str(index+1)
                )
        elif (t.MILESTONE in token):
            line.add_part(Milestone(token))
        else:
            line.add_part(TextPart(token))
    return line


def parser(text: str):
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

    # RE patterns
    para_pattern = re.compile(r"^#($|[^#])")    
    bio_pattern = re.compile(rf"{re.escape(t.BIO_MAN)}[^#]")
    morpho_pattern = re.compile(r"#~:([^:]+?):")
    region_pattern = re.compile(
        rf"({t.PROV}|{t.REG}\d) .*? {t.GEO_TYPE} .*? ({t.REG}\d|{t.STTL}) ([\w# ]+) $"
    )
    route_pattern = re.compile(
        rf"{t.DIST_FROM} .*? {t.DIST_TO} .*? {t.DIST} .*"
    )

    # Input lines loop
    for i, il in enumerate(ilines):
        
        # N.B. the order of if statements matters!
        # We're doing string matching and tag elements are re-used.

        # Non-machine readable metadata
        if (il.startswith(t.META)):
            if (il.strip() == t.METAEND):
                continue
            value = il.split(t.META, 1)[1].strip()
            document.set_simple_metadata_field(il, value)

        # Content-level page numbers
        elif (il.startswith(t.PAGE)):
            pv = PAGE_PATTERN.search(il)
            try:
                document.add_content(PageNumber(il, pv.group(1), pv.group(2)))
            except Exception:
                raise Exception(
                    'Could not parse page number at line: ' + str(i+1)
                )

        # Riwāyāt units
        elif (il.startswith(t.RWY)):
            # Set first line, skipping para marker "#"
            document.add_content(Riwayat())
            first_line = parse_line(il[1:], i)
            if first_line:
                document.add_content(first_line)

        # Morphological pattern
        elif (morpho_pattern.search(il)):
            m = morpho_pattern.search(il)
            document.add_content(MorphologicalPattern(il, m.group(1)))

        # Paragraphs and lines of verse
        elif (para_pattern.search(il)):
            if (t.HEMI in il):
                # this is a verse line, skip para marker "#"
                document.add_content(parse_line(il[1:], i, Verse))
            else:
                document.add_content(Paragraph())
                first_line = parse_line(il[1:], i)
                if first_line:
                    document.add_content(first_line)

        # Lines
        elif (il.startswith(t.LINE)):
            document.add_content(parse_line(il, i))

        # Editorial section
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
            no_tag = il
            for tag in t.DICTIONARIES:
                no_tag = no_tag.replace(tag, '')
            first_line = parse_line(no_tag, i)
            dic_type = "bib"
            if (t.DIC_LEX in il):
                dic_type = "lex"
            elif (t.DIC_NIS in il):
                dic_type = "nis"
            elif (t.DIC_TOP in il):
                dic_type = "top"
            document.add_content(DictionaryUnit(il, dic_type))
            if first_line:
                document.add_content(first_line)

        # Doxographical item
        elif (il.startswith(t.DOX)):
            no_tag = il
            for tag in t.DOXOGRAPHICAL:
                no_tag = no_tag.replace(tag, '')
            first_line = parse_line(no_tag, i)
            dox_type = "pos"
            if (t.DOX_SEC in il):
                dox_type = "sec"
            document.add_content(DoxographicalItem(il, dox_type))
            if first_line:
                document.add_content(first_line)

        # Biographies and Events
        elif (bio_pattern.search(il) or il.startswith(t.BIO) or il.startswith(t.EVENT)):
            no_tag = il
            for tag in t.BIOS_EVENTS:
                no_tag = no_tag.replace(tag, '')
            first_line = parse_line(no_tag, i)
            be_type = "man"
            # Ordered from longer to shorter string to aid matching. I.e. ### $$$ before ### $$
            if (t.LIST_NAMES_FULL in il or t.LIST_NAMES in il):
                be_type = "names"
            elif (t.BIO_REF_FULL in il or t.BIO_REF in il):
                be_type = "ref"
            elif (t.BIO_WOM_FULL in il or t.BIO_WOM in il):
                be_type = "wom"
            elif (t.LIST_EVENTS in il):
                be_type = "events"
            elif (t.EVENT in il):
                be_type = "event"
            document.add_content(BioOrEvent(il, be_type))
            if first_line:
                document.add_content(first_line)

        # Regions
        elif (region_pattern.search(il)):
            document.add_content(AdministrativeRegion(il))

        # Routes
        elif (route_pattern.search(il)):
            document.add_content(RouteOrDistance(il))

        else:
            continue

    return document
