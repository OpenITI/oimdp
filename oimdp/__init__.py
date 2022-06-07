from .parser import parser


def parse(text, strict = False):
    return parser(text, strict)


__all__ = [
   'parse'
]
__version__ = '1.1.1'
