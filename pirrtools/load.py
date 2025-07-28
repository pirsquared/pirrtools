"""Initialize pirrtools environment and load user preferences.

This module handles the automatic loading of user preferences from
a `.pirc.py` file in the home directory and sets up the IPython
environment with matplotlib inline plotting enabled.

The module is typically imported automatically when pirrtools is used
and performs the following setup tasks:
    - Enables matplotlib inline mode for IPython/Jupyter
    - Loads and executes user's `.pirc.py` configuration file
    - Adds custom paths specified in the configuration

Note:
    This module has side effects and executes setup code on import.
"""

from . import __load_matplotlib_inline, __load_pirc_file


__load_matplotlib_inline()
__load_pirc_file()
