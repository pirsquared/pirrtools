from pathlib import Path
from functools import cached_property
from textwrap import dedent
import json
import re
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound
from pygments.formatters import HtmlFormatter
from IPython import get_ipython
from IPython.display import HTML, SVG, Image, Markdown
import pandas as pd
from .attrdict import AttrDict


__all__ = ["AttrPath"]


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
                border: solid 1px var(--jp-inverse-border-color);
                padding: 1rem;
                max-height: 500px;
                overflow-y: auto;
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


def generalized_handler(file_path: Path):
    """Returns a handler that reads a file and returns its contents highlighted as HTML
    with syntax highlighting dictated by the file extension.
    """
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


_NON_ALPHANUMERIC = re.compile("(?=^\d)|\W")
_IS_DUNDER = re.compile("(^__(?!_).*(?<!_)__$)")


def attribute_safe_string(string):
    """Returns a path with a name that is safe for use as an attribute."""
    string = _NON_ALPHANUMERIC.sub("_", _IS_DUNDER.sub(r"DUNDER_\1", string))
    if string[0].isdigit():
        string = f"INT_{string}"
    if string[0] == "_":
        string = f"PRI{string}"
    return string


def html_handler(file_path: Path):
    """Returns the contents of an HTML file as an HTML object."""
    with file_path.open("r", encoding="utf-8") as file:
        return HTML(file.read())


def svg_handler(file_path: Path):
    """Returns the contents of an SVG file as an SVG object."""
    with file_path.open("r", encoding="utf-8") as file:
        return SVG(file.read())


def jpg_handler(file_path: Path):
    """Returns the contents of a JPG file as an Image object."""
    return Image(file_path.as_posix())


def png_handler(file_path: Path):
    """Returns the contents of a PNG file as an Image object."""
    return Image(file_path.as_posix())


def txt_handler(file_path: Path):
    """Returns the contents of a text file as a string."""
    with file_path.open("r", encoding="utf-8") as file:
        return file.read()


def json_handler(file_path: Path):
    """Returns the contents of a JSON file as a dictionary."""
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def csv_handler(file_path: Path):
    """Returns the contents of a CSV file as a pandas DataFrame."""
    return pd.read_csv(file_path.as_posix())


def feather_handler(file_path: Path):
    """Returns the contents of a feather file as a pandas DataFrame."""
    return pd.read_feather(file_path.as_posix())


def sas7bdat_handler(file_path: Path):
    """Returns the contents of a SAS7BDAT file as a pandas DataFrame."""
    return pd.read_sas(file_path.as_posix(), encoding="iso-8859-1")


def markdown_handler(file_path: Path):
    """Returns the contents of a markdown file as a Markdown object."""
    with file_path.open("r", encoding="utf-8") as file:
        return Markdown(file.read())


_Path = type(Path())


class AttrPath(_Path):
    _view_handlers = {
        "html": html_handler,
        "svg": svg_handler,
        "jpg": jpg_handler,
        "png": png_handler,
        "txt": txt_handler,
        "json": json_handler,
        "csv": csv_handler,
        "feather": feather_handler,
        "f": feather_handler,
        "sas7bdat": sas7bdat_handler,
        "md": markdown_handler,
    }

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls, *args, **kwargs).expanduser().resolve()
        return self

    def __init__(self, *args, **kwargs):
        super().__init__()

    @cached_property
    def _attr(self):
        if self.is_dir():
            _attr = AttrDict()
            for path in self.iterdir():
                safe_name = attribute_safe_string(path.name)
                safe_stem = attribute_safe_string(path.stem)
                new = AttrPath(path)
                suffix = new._suffix
                if path.is_dir():
                    _attr.setdefault("D", AttrDict())[safe_name] = new
                elif path.is_file():
                    _attr.setdefault("F", AttrDict())[safe_name] = new
                    if dir(new):
                        _attr.setdefault(suffix, AttrDict())[safe_stem] = new
            if _attr:
                return _attr

    @cached_property
    def _code_handler(self):
        if self._suffix == "csv":
            proxy = self.with_suffix(".txt")
        else:
            proxy = self
        handler = generalized_handler(proxy)
        if handler is not None:

            def _handler():
                return handler(self)

            return _handler

    @property
    def _suffix(self):
        return self.suffix[1:]

    def __dir__(self):
        pop_ups = []
        if self.is_file():
            if self._suffix in self._view_handlers:
                pop_ups.append("view")
            if self._code_handler is not None:
                pop_ups.append("code")
        elif self.is_dir():
            pop_ups.extend(self._attr.keys())
        return pop_ups

    def __getattr__(self, name):

        if name != "_str":
            if name in dir(self):
                if self.is_dir() and name in self._attr:
                    return getattr(self._attr, name)
                elif self.is_file():
                    if name == "view" and self._suffix in self._view_handlers:
                        return type(self)._view_handlers[self._suffix](self)
                    if name == "code" and self._code_handler is not None:
                        return self._code_handler()
        return getattr(super(), name)
