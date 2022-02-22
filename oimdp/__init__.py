from .parser import parser


def parse(text):
    return parser(text)


__all__ = [
   'parse'
]
__version__ = '1.1.1'
