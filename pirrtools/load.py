"""Load pirrtools preferences from a `.pirc` file in the home directory 
and set up the IPython environment."""

from . import __load_matplotlib_inline, __load_pirc_file


__load_matplotlib_inline()
__load_pirc_file()
