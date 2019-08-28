class MagicValue:
    """Magic Value of OpenITI mARkdown file"""
    def __init__(self, value):
        self.orig_value = value
        self.value = "######OpenITI#"

    def __str__(self):
        return self.value


class Document:
    """The OpenITI mARkdown document"""
    def __init__(self, text):
        self.orig_text = text

    def set_MagicValue(self, value):
        self.magic_value = MagicValue(value)

    def __str__(self):
        return self.orig_text
