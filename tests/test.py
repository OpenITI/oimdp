import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import oimdp


if __name__ == '__main__':
    root = os.path.dirname(__file__)
    filepath = os.path.join(
        root, 'test.md'
    )
    with open(filepath, 'r') as f:
        text = f.read()
        parsed = oimdp.parse(text)
