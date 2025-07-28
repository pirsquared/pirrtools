"""Enhanced pathlib with attribute-based navigation and intelligent file viewing.

This module provides the AttrPath class, which extends pathlib.Path with
attribute-based navigation capabilities and intelligent file viewing based
on file extensions. Files and directories can be accessed as attributes,
and various file types are automatically displayed with appropriate formatting.

Key Features:
    - Attribute-based file and directory navigation
    - Automatic syntax highlighting for code files
    - Built-in viewers for common file formats (CSV, JSON, images, etc.)
    - Safe attribute names for files with special characters
    - Organized access to files by type and directory structure

Example:
    >>> path = AttrPath('/my/project')
    >>> path.src.main_py.view  # View main.py with syntax highlighting
    >>> path.data.results_csv.view  # View CSV as pandas DataFrame
    >>> path.D.subdirectory  # Access subdirectory
    >>> path.py.script  # Access script.py from .py extension group
"""

import json
import re
import subprocess  # noqa: F401
import webbrowser  # for test patching
from functools import cached_property
from pathlib import Path
from textwrap import dedent

import pandas as pd
from IPython import get_ipython
from IPython.display import HTML, SVG, Image, Markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound

from .attrdict import AttrDict

__all__ = ["AttrPath"]


def read_and_highlight(file_path: str, lexer) -> str:
    """Read file and return syntax-highlighted HTML.

    This function reads a file and applies syntax highlighting using
    Pygments, returning formatted HTML suitable for display in
    Jupyter notebooks or other HTML contexts.

    Args:
        file_path (Path): The path to the file to read and highlight.
        lexer (pygments.lexer.Lexer): The Pygments lexer to use for
            syntax highlighting.

    Returns:
        str: The file contents formatted as HTML with syntax highlighting,
            wrapped in a styled container with the file path as header.

    Note:
        The output includes CSS styles for proper display with borders,
        padding, and scrollable content for long files.
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
    """Create a syntax highlighting handler for a file based on its extension.

    This function analyzes a file's extension and creates an appropriate
    handler function that will read and syntax-highlight the file when called.

    Args:
        file_path (Path): The file path to create a handler for.

    Returns:
        callable or None: A handler function that when called will return
            syntax-highlighted content, or None if no appropriate lexer
            is found for the file extension.

    Note:
        The returned handler automatically detects IPython environment
        and returns HTML objects when appropriate, otherwise returns
        raw HTML strings.
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


_NON_ALPHANUMERIC = re.compile(r"(?=^\d)|\W")
_IS_DUNDER = re.compile("(^__(?!_).*(?<!_)__$)")


def attribute_safe_string(string):
    """Convert string to a safe Python attribute name.

    This function transforms file and directory names into valid Python
    attribute names by replacing non-alphanumeric characters and handling
    special cases like numbers at the start and dunder methods.

    Args:
        string (str): The original string to convert.

    Returns:
        str: A safe attribute name that can be used in Python code.

    Examples:
        >>> attribute_safe_string('my-file.txt')
        'my_file_txt'
        >>> attribute_safe_string('123data')
        'INT_123data'
        >>> attribute_safe_string('__init__.py')
        'DUNDER___init___py'
    """
    string = _NON_ALPHANUMERIC.sub("_", _IS_DUNDER.sub(r"DUNDER_\1", string))
    if string[0].isdigit():
        string = f"INT_{string}"
    if string[0] == "_":
        string = f"PRI{string}"
    return string


def html_handler(file_path: Path):
    """Load and display HTML file content.

    Args:
        file_path (Path): Path to the HTML file.

    Returns:
        IPython.display.HTML: HTML object for display in Jupyter notebooks.
    """
    with file_path.open("r", encoding="utf-8") as file:
        return HTML(file.read())


def svg_handler(file_path: Path):
    """Load and display SVG file content.

    Args:
        file_path (Path): Path to the SVG file.

    Returns:
        IPython.display.SVG: SVG object for display in Jupyter notebooks.
    """
    with file_path.open("r", encoding="utf-8") as file:
        return SVG(file.read())


def jpg_handler(file_path: Path):
    """Load and display JPEG image file.

    Args:
        file_path (Path): Path to the JPEG file.

    Returns:
        IPython.display.Image: Image object for display in Jupyter notebooks.
    """
    return Image(file_path.as_posix())


def png_handler(file_path: Path):
    """Load and display PNG image file.

    Args:
        file_path (Path): Path to the PNG file.

    Returns:
        IPython.display.Image: Image object for display in Jupyter notebooks.
    """
    return Image(file_path.as_posix())


def txt_handler(file_path: Path):
    """Load and return text file content.

    Args:
        file_path (Path): Path to the text file.

    Returns:
        str: The complete contents of the text file.
    """
    with file_path.open("r", encoding="utf-8") as file:
        return file.read()


def json_handler(file_path: Path):
    """Load and parse JSON file.

    Args:
        file_path (Path): Path to the JSON file.

    Returns:
        dict: The parsed JSON data as a Python dictionary.
    """
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def csv_handler(file_path: Path):
    """Load CSV file as pandas DataFrame.

    Args:
        file_path (Path): Path to the CSV file.

    Returns:
        pd.DataFrame: The CSV data loaded as a pandas DataFrame.
    """
    return pd.read_csv(file_path.as_posix())


def feather_handler(file_path: Path):
    """Load feather file as pandas DataFrame.

    Args:
        file_path (Path): Path to the feather file.

    Returns:
        pd.DataFrame: The feather data loaded as a pandas DataFrame.
    """
    return pd.read_feather(file_path.as_posix())


def sas7bdat_handler(file_path: Path):
    """Load SAS7BDAT file as pandas DataFrame.

    Args:
        file_path (Path): Path to the SAS7BDAT file.

    Returns:
        pd.DataFrame: The SAS data loaded as a pandas DataFrame.

    Note:
        Uses ISO-8859-1 encoding for compatibility with SAS files.
    """
    return pd.read_sas(file_path.as_posix(), encoding="iso-8859-1")


def markdown_handler(file_path: Path):
    """Load and display Markdown file content.

    Args:
        file_path (Path): Path to the Markdown file.

    Returns:
        IPython.display.Markdown: Markdown object for rendered display
            in Jupyter notebooks.
    """
    with file_path.open("r", encoding="utf-8") as file:
        return Markdown(file.read())


_Path = type(Path())


class AttrPath(_Path):
    @cached_property
    def _attr(self):
        """Builds a dictionary of attribute-accessible children: D, F, extension
        groups, and all safe names."""
        attr = {}
        pself = Path(self)
        try:
            is_dir = pself.is_dir()
        except Exception:
            is_dir = False
        if not is_dir:
            return attr
        dirs = {}
        files = {}
        ext_groups = {}
        try:
            children = list(pself.iterdir())
        except Exception:
            children = []
        for child in children:
            safe = attribute_safe_string(child.name)
            try:
                if child.is_dir():
                    dirs[safe] = child
                elif child.is_file():
                    files[safe] = child
                    ext = child.suffix[1:] if child.suffix else None
                    if ext:
                        if ext not in ext_groups:
                            ext_groups[ext] = {}
                        ext_groups[ext][safe] = child
            except Exception:
                continue
        attr["D"] = AttrDict({k: AttrPath(v) for k, v in dirs.items()})
        attr["F"] = AttrDict({k: AttrPath(v) for k, v in files.items()})
        for ext, group in ext_groups.items():
            attr[ext] = AttrDict({k: AttrPath(v) for k, v in group.items()})
        # Add all direct children by safe name
        for k, v in {**dirs, **files}.items():
            attr[k] = AttrPath(v)
        return attr

    """Enhanced pathlib.Path with attribute-based navigation and file viewing.

    AttrPath extends pathlib.Path to provide intuitive attribute-based
    navigation through file systems and intelligent viewing of different
    file types. Files and directories become accessible as attributes,
    with automatic safe naming and organized access patterns.

    Key Features:
        - Access files and directories as attributes
        - Automatic file viewing based on extension
        - Syntax highlighting for code files
        - Organized access by file type (.py, .csv, etc.)
        - Safe attribute names for special characters
        - Built-in handlers for common file formats

    Attributes:
        _view_handlers (dict): Mapping of file extensions to view handlers.

    Example:
        >>> path = AttrPath('/project')
        >>> path.src.main_py.view  # View with syntax highlighting
        >>> path.data.D.subdir    # Navigate to subdirectory
        >>> path.py.utils         # Access utils.py via extension group
        >>> path.csv.data         # Access data.csv via extension group

    Note:
        All paths are automatically expanded and resolved to absolute paths.
    """
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
        "py": generalized_handler,
    }

    def __new__(cls, *args, **kwargs):
        """Create new AttrPath instance with expanded user path (no resolve to
        avoid recursion)."""
        self = super().__new__(cls, *args, **kwargs).expanduser()
        return self

    def __init__(self, *args, **kwargs):
        """Initialize AttrPath instance."""
        super().__init__()

    @cached_property
    def _code_handler(self):
        """Get syntax highlighting handler for this file.

        Creates a handler function that will apply appropriate syntax
        highlighting when called, based on the file's extension.

        Returns:
            callable or None: Handler function that returns highlighted
                content when called, or None if no highlighting is available.

        Note:
            CSV files are treated as text files for syntax highlighting
            purposes to show raw content rather than parsed data.
        """
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
        """Get file extension without the leading dot.

        Returns:
            str: File extension with leading dot removed, or empty string
                if no extension.

        Example:
            >>> AttrPath('file.txt')._suffix
                _attr[safe_name] = path
            'txt'
            >>> AttrPath('script.py')._suffix
            'py'
        """
        return self.suffix[1:]

    def __dir__(self):
        """Return list of available attributes for this path, including safe
        names, D/F, extension groups, and .view/.code."""
        names = set(super().__dir__())
        try:
            attr = self._attr or {}
        except Exception:
            attr = {}
        # Add D, F, extension groups, and all safe names for files/dirs
        names.update(attr.keys())
        for group in attr.values():
            if isinstance(group, AttrDict):
                names.update(group.keys())
        # Add .view and .code for files
        try:
            if Path(self).is_file():
                if self._suffix in self._view_handlers:
                    names.add("view")
                if getattr(self, "_code_handler", None) is not None:
                    names.add("code")
        except Exception:
            pass
        return list(names)

    def __getattr__(self, name):
        """Attribute-based access to extension groups, D/F, safe names, and
        direct children. Never call is_file/is_dir here."""
        # Provide .view for supported files
        if name == "view":
            ext = self._suffix
            handler = self._view_handlers.get(ext)
            if handler:

                def _view(*args, **kwargs):
                    # If file does not exist, handle gracefully
                    if not Path(self).exists():
                        print(f"[AttrPath] File does not exist: {self}")
                        return None
                    # HTML: open in browser
                    if ext == "html":
                        webbrowser.open(str(self))
                        return
                    # Text, CSV, JSON, MD, PY: print with rich if available
                    elif ext in ("txt", "csv", "json", "md", "py"):
                        try:
                            from rich.console import Console

                            console = Console()
                            result = handler(self, *args, **kwargs)
                            console.print(result)
                        except Exception:
                            print(handler(self, *args, **kwargs))
                        return
                    # Images: display with IPython if available
                    elif ext in ("png", "jpg", "svg"):
                        try:
                            from IPython.display import display

                            display(handler(self, *args, **kwargs))
                        except Exception:
                            pass
                        return
                    # Fallback: just call handler
                    return handler(self, *args, **kwargs)

                return _view
        # Only handle custom attribute names for extension groups, D/F, safe
        # names, and direct children
        try:
            _attr = object.__getattribute__(self, "_attr")
        except Exception:
            _attr = None
        if _attr:
            # D, F, extension groups
            if name in _attr:
                val = _attr[name]
                if isinstance(val, Path) and not isinstance(val, AttrPath):
                    return AttrPath(val)
                if isinstance(val, AttrDict):
                    return AttrDict(
                        {
                            k: (
                                AttrPath(v)
                                if isinstance(v, Path) and not isinstance(v, AttrPath)
                                else v
                            )
                            for k, v in val.items()
                        }
                    )
                return val
            # Direct safe names for files/dirs in all groups
            for group in _attr.values():
                if isinstance(group, AttrDict) and name in group:
                    val = group[name]
                    if isinstance(val, Path) and not isinstance(val, AttrPath):
                        return AttrPath(val)
                    return val
        # Fallback: try normal attribute (Path, etc.)
        return super().__getattribute__(name)
