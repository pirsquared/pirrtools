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
    }

    def __new__(cls, *args, **kwargs):
        """Create new AttrPath instance with expanded and resolved path.
        
        Args:
            *args: Arguments passed to pathlib.Path constructor.
            **kwargs: Keyword arguments passed to pathlib.Path constructor.
            
        Returns:
            AttrPath: New instance with expanded user path and resolved absolute path.
        """
        self = super().__new__(cls, *args, **kwargs).expanduser().resolve()
        return self

    def __init__(self, *args, **kwargs):
        """Initialize AttrPath instance.
        
        Args:
            *args: Arguments passed to parent Path constructor.
            **kwargs: Keyword arguments passed to parent Path constructor.
        """
        super().__init__()

    @cached_property
    def _attr(self):
        """Compute and cache attribute-based navigation structure.
        
        This property analyzes the directory contents and creates an
        organized structure for attribute-based access. Directories
        are grouped under 'D', files under 'F', and by extension.
        
        Returns:
            AttrDict or None: Organized structure of available attributes,
                or None if directory is empty or path is not a directory.
        
        Note:
            Results are cached for performance. The structure includes:
            - D: Subdirectories accessible by safe names
            - F: Files accessible by safe names  
            - Extension groups (py, csv, etc.): Files by safe stem names
        """
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
            'txt'
            >>> AttrPath('script.py')._suffix  
            'py'
        """
        return self.suffix[1:]

    def __dir__(self):
        """Return list of available attributes for this path.
        
        For files, returns available actions like 'view' and 'code'.
        For directories, returns available navigation attributes.
        
        Returns:
            list: Available attribute names for tab completion and inspection.
        """
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
        """Provide attribute-based access to files, directories, and actions.
        
        This method enables the core functionality of AttrPath by allowing
        navigation and file viewing through attribute access.
        
        Args:
            name (str): The attribute name being accessed.
            
        Returns:
            Various types depending on the attribute:
            - AttrPath: For directory navigation
            - AttrDict: For grouped file access
            - File content: For file viewing ('view' attribute)
            - HTML/formatted content: For code viewing ('code' attribute)
            - Parent class attributes: For standard Path functionality
            
        Note:
            Special attributes:
            - 'view': Display file with appropriate handler
            - 'code': Display file with syntax highlighting
            - Directory/file names: Navigate to that location
        """
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
