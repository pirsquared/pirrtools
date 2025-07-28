"""Module for loading utilities in pirrtools.

Provides functions for loading modules, classes, and other entities with
optional IPython integration.
"""

from IPython import get_ipython  # noqa: F401

from . import load_matplotlib_inline, load_pirc_file

load_matplotlib_inline()
load_pirc_file()
