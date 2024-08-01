from pathlib import Path
from functools import cached_property
from collections.abc import Mapping
from textwrap import dedent
import json
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound
from pygments.formatters import HtmlFormatter
from IPython import get_ipython
from IPython.display import HTML, SVG, Image, Markdown
import pandas as pd
from .attrdict import AttrDict


def read_and_highlight(file_path: str, lexer) -> str:
    """
    Reads a file and returns its contents highlighted as HTML with syntax highlighting
    dictated by the passed lexer.

    Parameters
    ----------
    file_path : Path
        The path to the file to read.

    lexer : pygments.lexer.Lexer
        The lexer to use for syntax highlighting.

    Returns
    -------
    str
        The file contents highlighted as HTML.

    """
    with file_path.open("r", encoding="utf-8") as file:
        code = file.read()

    # Highlight the code
    formatter = HtmlFormatter()
    highlighted_code = highlight(code, lexer, formatter)

    # Wrap in <pre> tag
    tagged_code = dedent(
        f"""\
        <style>
            pre.formatted-code {{
                border: solid 1px white;
                padding: 1rem;
            }}
            .formatted-code-container strong {{
                display: block;
                margin-bottom: 1rem;
            }}
        </style>
        <div class="formatted-code-container">
            <strong>{file_path.as_posix()}</strong>
            <pre class="formatted-code">{highlighted_code}</pre>
        </div>
    """
    )

    return tagged_code


def hightlight_handler(lexer):

    def handler(file_path: Path):
        return read_and_highlight(file_path, lexer)

    return handler


def generalized_handler(file_path: Path):
    try:
        lexer = get_lexer_for_filename(file_path.name)
    except ClassNotFound:
        lexer = None

    if lexer is not None:

        def handler(file_path: Path):

            html = read_and_highlight(file_path, lexer)

            ipython = get_ipython()
            if ipython:
                return HTML(html)

            return html

        return handler


def dict_pack(d: dict, k_: tuple = ()):
    """Generator that yields tuples of nested keys and values from a dictionary.

    Parameters
    ----------
    d : dict
        The dictionary to pack.

    k_ : tuple, optional
        The keys of the parent dictionaries. Default is an empty tuple.
        Purpose is to allow for recursive unpacking.  It is not recommended
        to pass this argument directly.

    Yields
    ------
    tuple
        A tuple of the nested keys and the value.

    Examples
    --------

    .. testcode::

        d = {'a': {'b': 1, 'c': 2}}
        list(dict_pack(d))

    .. testoutput::

        [(('a', 'b'), 1), (('a', 'c'), 2)]

    """

    for k, v in d.items():
        kt = (*k_, k)
        if isinstance(v, Mapping):
            yield from dict_pack(v, kt)
        else:
            yield kt, v


def dict_pack_as_dict(d: dict):
    """Packs a dictionary with nested dictionaries into a flat dictionary with tuples as
    keys.

    Parameters
    ----------
    d : dict
        The dictionary to pack.

    Returns
    -------
    dict
        A flat dictionary with tuples as keys.

    Examples
    --------

    .. testcode::

        d = {'a': {'b': 1, 'c': 2}}
        dict_pack_as_dict(d)

    .. testoutput::

        {('a', 'b'): 1, ('a', 'c'): 2}

    """
    return dict(dict_pack(d))


class ExtendedAttrDict(AttrDict):
    """A dictionary that allows access to its keys as attributes.

    This class extends the `AttrDict` class to allow for nested dictionaries to be
    accessed as attributes.  The difference between this class and the `AttrDict` class
    is that this class allows for nested dictionaries to be show up in the `dir` method.
    """

    @cached_property
    def _pact(self):

        return {".".join(k): v for k, v in dict_pack(self)}

    def __dir__(self):

        return list(self._pact)


_Path = type(Path())


class HandledPath(_Path):

    _handlers = AttrDict()

    def __dir__(self):
        return list(self._handlers.keys())

    def __getattr__(self, name):
        if name in self._handlers:
            return self._handlers[name](self)
        return getattr(super(), name)


def subclass_handledpath(name, handlers):

    class SubclassPath(HandledPath):

        _handlers = handlers

    SubclassPath.__name__ = name
    return SubclassPath


def html_handler(file_path: Path):
    with file_path.open("r", encoding="utf-8") as file:
        return HTML(file.read())


def svg_handler(file_path: Path):
    with file_path.open("r", encoding="utf-8") as file:
        return SVG(file.read())


def jpg_handler(file_path: Path):
    return Image(file_path.as_posix())


def png_handler(file_path: Path):
    return Image(file_path.as_posix())


def txt_handler(file_path: Path):
    with file_path.open("r", encoding="utf-8") as file:
        return file.read()


def json_handler(file_path: Path):
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def csv_handler(file_path: Path):
    return pd.read_csv(file_path.as_posix())


def feather_handler(file_path: Path):
    return pd.read_feather(file_path.as_posix())


def sas7bdat_handler(file_path: Path):
    return pd.read_sas(file_path.as_posix(), encoding="iso-8859-1")


def markdown_handler(file_path: Path):
    with file_path.open("r", encoding="utf-8") as file:
        return Markdown(file.read())


class AttrPath(_Path):

    _flavour = _Path._flavour
    _handlers = {
        "html": html_handler,
        "svg": svg_handler,
        "jpg": jpg_handler,
        "png": png_handler,
        "txt": txt_handler,
        "json": json_handler,
        "csv": csv_handler,
        "feather": feather_handler,
        "sas7bdat": sas7bdat_handler,
        "md": markdown_handler,
    }

    @property
    def categorize_paths(self):

        handlers = set(type(self)._handlers.keys())
        root = self.expanduser().resolve()

        if root.is_file():
            return root

        maptype = ExtendedAttrDict
        result = maptype()

        if root.is_dir():
            for path in root.iterdir():
                *keys, last = path.name.split(".")
                if path.is_file():
                    subresult = result.setdefault("F", maptype())
                    for key in keys:
                        subresult = subresult.setdefault(key or "_", maptype())
                    subresult[last] = path

                    suffix = path.suffix[1:]
                    code_handler = generalized_handler(path)
                    handler = maptype()
                    if suffix in handlers:
                        handler["view"] = self._handlers[suffix]
                    if code_handler:
                        handler["code"] = code_handler

                    if handler:
                        subresult = result.setdefault(suffix, maptype())
                        for key in keys:
                            subresult = subresult.setdefault(key or "_", maptype())

                        subclass_name = f"{suffix.title()}Path"
                        subclass = subclass_handledpath(subclass_name, handler)
                        subresult[last] = subclass(path)

                if path.is_dir():
                    subresult = result.setdefault("D", maptype())
                    for key in keys:
                        subresult = subresult.setdefault(key or "_", maptype())
                    subresult[last] = path

        return result

    @cached_property
    def get(self):

        if self.is_file() and (suffix := self.suffix[1:]) in self._handlers:
            return self._handlers[suffix](self)

    @cached_property
    def _attr(self):

        return self.categorize_paths

    def __dir__(self):

        return list(self._attr.keys())

    def __getattr__(self, name):

        if name != "_str" and name in self._attr:
            return getattr(self._attr, name)
        return getattr(super(), name)


def subclass_attrpath(name, handlers):

    class SubclassPath(AttrPath):

        _handlers = handlers

    SubclassPath.__name__ = name
    return SubclassPath
