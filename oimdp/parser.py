import sys
from .structures import Document


def parser(text):
    """Parses an OpenITI mARkdown file and returns a Document object"""
    document = Document(text)

    lines = text.splitlines()

    magic_value = lines[0]

    if magic_value.strip() != "######OpenITI#":
        raise Exception(
            "This does not appear to be an OpenITI mARkdown document")
        sys.exit(1)

    document.set_MagicValue(magic_value)
    print(document.magic_value)
