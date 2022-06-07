import sys
import re
from .structures import Age, Date, Document, Hemistich, Hukm, Isnad, Matn, NamedEntity, OpenTagAuto, OpenTagUser, PageNumber, Paragraph, Line, RouteDist, RouteFrom, RouteTowa, Verse, Milestone
from .structures import SectionHeader, Editorial, Appendix, Paratext, DictionaryUnit, BioOrEvent
from .structures import DoxographicalItem, MorphologicalPattern, TextPart
from .structures import AdministrativeRegion, RouteOrDistance, Riwayat
from . import tags as t

PAGE_PATTERN = rf"{t.PAGE}[^P]+P\d+[AB]?"
PAGE_PATTERN_GROUPED = rf"{t.PAGE}([^P]+)P(\d+[AB]?)"
PAGE_RE = re.compile(PAGE_PATTERN_GROUPED)
MILESTONE_PATTERN = r"Milestone300|ms[A-Z]?\d+"
HEADER_PATTERN = r"### \|+"
HEADER_PATTERN_GROUPED = r"### (\|+)"
OPEN_TAG_CUSTOM_PATTERN = r"@[^@]+?@[^_@]+?_[^_@]+?(?:_[^_@]+?)?@"
OPEN_TAG_CUSTOM_PATTERN_GROUPED = re.compile(
    r"@([^@]+?)@([^_@]+?)_([^_@]+?)(_([^_@]+?))?@"
)
OPEN_TAG_AUTO_PATTERN = r"@[A-Z]{3}@[A-Z]{3,}@[A-Za-z]+@(?:-@[0tf][ftalmr]@)?"
OPEN_TAG_AUTO_PATTERN_GROUPED = re.compile(
    r"@([A-Z]{3})@([A-Z]{3,})@([A-Za-z]+)@(-@([0tf][ftalmr])@)?"
)
YEAR_PATTERN = [rf"{t.YEAR_AGE}\d{{1,4}}", rf"{t.YEAR_DEATH}\d{{1,4}}", rf"{t.YEAR_BIRTH}\d{{1,4}}", rf"{t.YEAR_OTHER}\d{{1,4}}"]
TOP_PATTERN = [rf"{t.TOP_FULL}\d{{1,2}}", rf"{t.TOP}\d{{1,2}}"]
PER_PATTERN = [rf"{t.PER_FULL}\d{{1,2}}", rf"{t.PER}\d{{1,2}}"]
SOC_PATTERN = [rf"{t.SOC_FULL}\d{{1,2}}", rf"{t.SOC}\d{{1,2}}"]
NAMED_ENTITIES_PATTERN = [*YEAR_PATTERN, *TOP_PATTERN, *PER_PATTERN, rf"{t.SRC}\d{{1,2}}", *SOC_PATTERN]


def parse_tags(s: str):
    return s


def remove_phrase_lv_tags(s: str):
    text_only = s
    for tag in t.PHRASE_LV_TAGS:
        text_only = text_only.replace(tag, '')
    for tag in NAMED_ENTITIES_PATTERN:
        text_only = re.compile(tag).sub('', text_only)
    # Open tag
    text_only = OPEN_TAG_CUSTOM_PATTERN_GROUPED.sub('', text_only)
    text_only = OPEN_TAG_AUTO_PATTERN_GROUPED.sub('', text_only)
    text_only = PAGE_RE.sub('', text_only)
    return text_only


def parse_line(tagged_il: str, index: int, obj=Line, first_token=None):
    """ parse a line text into LineParts by splitting it by tags and patterns """
    # remove line tag
    il = tagged_il.replace(t.LINE, '')

    # get clean text
    text_only = il
    text_only = remove_phrase_lv_tags(text_only)

    if text_only == "":
        return None

    line = obj(il, text_only)

    # Split the line by tags. Make sure patterns do not include subgroups!
    tokens = re.split(rf"({PAGE_PATTERN}|{MILESTONE_PATTERN}|{OPEN_TAG_AUTO_PATTERN}|{OPEN_TAG_CUSTOM_PATTERN}|{'|'.join([re.escape(t) for t in t.PHRASE_LV_TAGS])}|{'|'.join([t for t in NAMED_ENTITIES_PATTERN])})", il)

    # Some structures inject a token at the beginning of a line, like a riwāyaŧ's isnād
    if first_token:
        line.add_part(first_token(""))

    # Named entities include in their `text` property a given number of words from the following text token
    # This variable is used to keep track. A "word" is just a space-separated token.
    include_words = 0

    for token in tokens:
        if token == '':
            continue

        opentag_match = None
        opentagauto_match = None

        if token.startswith('@'):
            opentag_match = OPEN_TAG_CUSTOM_PATTERN_GROUPED.match(token)
            opentagauto_match = OPEN_TAG_AUTO_PATTERN_GROUPED.match(token)

        if t.PAGE in token:
            m = PAGE_RE.search(token)
            try:
                line.add_part(PageNumber(token, m.group(1), m.group(2)))
            except Exception:
                raise Exception(
                    'Could not parse page number at line: ' + str(index+1)
                )
        elif re.compile(MILESTONE_PATTERN).match(token):
            line.add_part(Milestone(token))
        elif opentag_match:
            line.add_part(OpenTagUser(token, 
                opentag_match.group(1),  # user
                opentag_match.group(2),  # t_type
                opentag_match.group(3),  # t_subtype
                opentag_match.group(5))) # t_subsubtype
        elif opentagauto_match:
            line.add_part(OpenTagAuto(token, 
                opentagauto_match.group(1),  # resp
                opentagauto_match.group(2),  # t_type                
                opentagauto_match.group(3),  # category
                opentagauto_match.group(5))) # review
        elif t.HEMI in token:
            line.add_part(Hemistich(token))
        elif t.MATN in token:
            line.add_part(Matn(token))
        elif t.HUKM in token:
            line.add_part(Hukm(token))
        elif t.ROUTE_FROM in token:
            line.add_part(RouteFrom(token))
        elif t.ROUTE_TOWA in token:
            line.add_part(RouteTowa(token))
        elif t.ROUTE_DIST in token:
            line.add_part(RouteDist(token))
        elif t.YEAR_BIRTH in token:
            line.add_part(Date(token, token.replace(t.YEAR_BIRTH, ''), 'birth'))
        elif t.YEAR_DEATH in token:
            line.add_part(Date(token, token.replace(t.YEAR_DEATH, ''), 'death'))
        elif t.YEAR_OTHER in token:
            line.add_part(Date(token, token.replace(t.YEAR_OTHER, ''), 'other'))
        elif t.YEAR_AGE in token:
            line.add_part(Age(token, token.replace(t.YEAR_AGE, '')))
        elif t.SRC in token:
            val = token.replace(t.SRC, '')
            include_words = int(val[1])
            line.add_part(NamedEntity(token, int(val[0]), include_words, "", 'src'))
        elif t.SOC_FULL in token:
            val = token.replace(t.SOC_FULL, '')
            include_words = int(val[1])
            line.add_part(NamedEntity(token, int(val[0]), include_words, "", 'soc'))
        elif t.SOC in token in token:
            val = token.replace(t.SOC, '')
            include_words = int(val[1])
            line.add_part(NamedEntity(token, int(val[0]), include_words, "", 'soc'))
        elif t.TOP_FULL in token:
            val = token.replace(t.TOP_FULL, '')
            include_words = int(val[1])
            line.add_part(NamedEntity(token, int(val[0]), include_words, "", 'top'))
        elif t.TOP in token:
            val = token.replace(t.TOP, '')
            include_words = int(val[1])
            line.add_part(NamedEntity(token, int(val[0]), include_words, "", 'top'))
        elif t.PER_FULL in token:
            val = token.replace(t.PER_FULL, '')
            include_words = int(val[1])
            line.add_part(NamedEntity(token, int(val[0]), include_words, "", 'per'))
        elif t.PER in token:
            val = token.replace(t.PER, '')
            include_words = int(val[1])
            line.add_part(NamedEntity(token, int(val[0]), include_words, "", 'per'))
        else:
            if include_words > 0:
                rest = ""
                words = token.strip().split()
                for pos, word in enumerate(words):
                    if (pos < include_words):
                        line.parts[-1].text = line.parts[-1].text + word + " "
                    else:
                        rest = rest + word + " "
                if len(rest):
                    line.add_part(TextPart(rest))
                include_words = 0
            else:
                line.add_part(TextPart(token))
    return line


def parser(text: str, strict: bool = False):
    """Parses an OpenITI mARkdown file and returns a Document object"""
    document = Document(text)

    # Split input text into lines
    ilines = text.splitlines()

    # Magic value
    magic_value = ilines[0]
    
    if strict and magic_value.strip() != "######OpenITI#":
        raise Exception(
            "This does not appear to be an OpenITI mARkdown document (strict mode)")
        sys.exit(1)
    elif not magic_value.strip().startswith("######OpenITI#"):
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
            pv = PAGE_RE.search(il)
            try:
                document.add_content(PageNumber(il, pv.group(1), pv.group(2)))
            except Exception:
                raise Exception(
                    'Could not parse page number at line: ' + str(i+1)
                )

        # Riwāyāt units
        elif (il.startswith(t.RWY)):
            # Set first line, skipping para marker "# $RWY$"
            document.add_content(Riwayat())
            first_line = parse_line(il[7:], i, first_token=Isnad)
            if first_line:
                document.add_content(first_line)

        # Routes
        elif (il.startswith(t.ROUTE_FROM)):
            document.add_content(parse_line(il, i, RouteOrDistance))

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

        # Sections
        elif (il.startswith(t.EDITORIAL)):
            document.add_content(Editorial(il))
        elif (il.startswith(t.APPENDIX)):
            document.add_content(Appendix(il))
        elif (il.startswith(t.PARATEXT)):
            document.add_content(Paratext(il))

        # Section headers
        elif (il.startswith(t.HEADER)):
            value = il
            header_re = re.compile(HEADER_PATTERN_GROUPED)
            value = header_re.sub('', value)
            # remove other phrase level tags
            value = remove_phrase_lv_tags(value)
            level = len(header_re.match(il).group(1))

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

        else:
            continue

    return document
