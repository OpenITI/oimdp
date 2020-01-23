import sys
import re
from .structures import Document, PageNumber, Paragraph, Line, Verse

# Container structure type for structure stack.
PARA = "paragraph"

# mARkdown tag library
META = "#META#"
METAEND = "#META#Header#End#"
PAGE = "PageV"
HEMI = "%~%"
LINE = "~~"


def parse_tags(s: str):
    return s


def parse_line(tagged_il: str):
    text_only = tagged_il.replace("#", '').replace(HEMI, '').replace(LINE, '')

    # remove line tag
    il = tagged_il.replace(LINE, '')
    # Hemistichs
    # if (HEMI in il):
    #     for (hemi in il.split(HEMI)):
    #         # mark as hemi and process further by calling parse_tags()
    return Line(il, text_only, il)


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
    para_pattern = re.compile("^#($|[^#])")
    page_pattern = re.compile("PageV(\d+)P(\d+)")

    # Input lines loop
    for il in ilines:

        # Non-machine readable metadata
        if (il.startswith(META)):
            if (il.strip() == METAEND):
                continue
            value = il.split(META, 1)[1].strip()
            document.set_simple_metadata_field(il, value)

        # Page numbers
        elif (PAGE in il):
            pv = page_pattern.search(il)
            document.set_page_number(PageNumber(il, pv.group(1), pv.group(2)))

        # Paragraphs and lines of verse
        elif (para_pattern.search(il)):
            first_line = parse_line(il)
            if (HEMI in il):
                # this is a verse line
                document.set_verse(Verse(il, first_line))
            else:
                current_structure = Paragraph([first_line])
                document.set_paragraph(current_structure)

        # Paragraph lines
        elif (il.startswith(LINE)):
            if (isinstance(current_structure, Paragraph)):
                current_structure.add_line(parse_line(il))

    return document
