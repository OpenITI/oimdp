from .parser import parser


def parse(text):
    return parser(text)


__all__ = [
   'parse'
]
__version__ = '0.0.1'
