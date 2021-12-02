# oimdp: OpenITI mARkdown Parser

This Python library will parse an [OpenITI mARkdown](https://alraqmiyyat.github.io/mARkdown/) document and return a python class
representation of the document structures.

## Usage

```py
import oimdp

md_file = open("mARkdownfile", "r")
text = md_file.read()
md_file.close()
parsed = oimdp.parse(text)
```

## Parsed structure

Please see [the docs](https://openiti.github.io/oimdp/), but here are some highlights:

### Document API

`content`: a list of content structures

`get_clean_text()`: get the text stripped of markup

### Content structures

`Content` classes contain an original value from the document and some extracted content such as a text string or a specific value.

Most other structures are listed in sequence (e.g. a `Paragraph` is followed by a `Line`). 

`Line` objects and other line-level structures are divided in `PhrasePart` objects.

`PhrasePart` are phrase-level tags

## Develop

Set up a virtual environment with `venv`

```py
python3 -m venv .env
```

Activate the virtual environment

```py
source .env/bin/activate
```

Install

```py
python setup.py install
```

## Tests

With the environment activated:

```py
python tests/test.py
```