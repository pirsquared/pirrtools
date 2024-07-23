"""This module provides utility functions for the pirrtools package.

Functions:
- addpath(path, position=0, verbose=False): Adds a path to the system path at the
  specified position.
- reload_entity(entity): Reloads a module or class. If a class is provided, its module
  is reloaded, and then the class is re-imported from this module.
- __get_pirc_file(): Looks for a `.pirc` file in the home directory.
- __load_pirc_file(): Loads the `.pirc` module from the `.pirc.py` file in the home
  directory and adds the specified paths to the system path.
- __load_matplotlib_inline(): Loads the '%matplotlib inline' magic command in IPython if
  available.

Classes:
- AttrDict: A dictionary-like object that allows attribute access to its items.9

Usage:
- To add a path to the system path, use the addpath() function.
- To reload a module or class, use the reload_entity() function.
- The __get_pirc_file() function looks for a `.pirc` file in the home directory.
- The __load_pirc_file() function loads the `.pirc` module from the `.pirc.py` file in
  the home directory and adds the specified paths to the system path.
- The __load_matplotlib_inline() function loads the '%matplotlib inline' magic command
  in IPython if available.

Note: This module is part of the pirrtools package.
"""

import sys as __sys
import pathlib as __pathlib
import importlib as __importlib
import importlib.util as __importlib_util
import types as __types
from IPython import get_ipython
from .pandas import load_cache
from .structures import AttrDict


__HOME = __pathlib.Path.home().absolute()


def addpath(path, position=0, verbose=False):
    """Adds a path to the system path at the specified position.

    Args:
        path (str): The path to add.
        position (int, optional): The position in the system path where the path should
          be added. Defaults to 0.
        verbose (bool, optional): Whether to print a message when the path is added.
          Defaults to False.
    """
    path = __pathlib.Path(path).expanduser().absolute()
    if path not in __sys.path:
        __sys.path.insert(position, str(path))
        if verbose:
            print(f'added "{str(path)}" into system path at position {position}')


def reload_entity(entity):
    """Reloads a module or class. If a class is provided, its module is reloaded, and
    then the class is re-imported from this module.

    Args:
        entity (module or class): The module or class to reload.

    Returns:
        The reloaded module or class.
    """
    if isinstance(entity, __types.ModuleType):
        # It's a module, reload directly
        return __importlib.reload(entity)
    # It's assumed to be a class, get its module
    module_name = entity.__module__
    module = __importlib.import_module(module_name)
    # Reload the module
    reloaded_module = __importlib.reload(module)
    # Re-import and return the class from the reloaded module
    return getattr(reloaded_module, entity.__name__)


def __get_pirc_file():
    """Looks for a `.pirc` file in the home directory.

    Returns:
        The path to the `.pirc` file if it exists, None otherwise.
    """
    pirc_file = __HOME / ".pirc.py"
    if pirc_file.exists():
        return pirc_file
    return None


def __load_pirc_file():
    """Loads the `.pirc` module from the `.pirc.py` file in the home directory and adds
    the specified paths to the system path."""
    pirc_file = __get_pirc_file()
    if pirc_file:
        spec = __importlib_util.spec_from_file_location("pirc", pirc_file)
        pirc = __importlib_util.module_from_spec(spec)
        spec.loader.exec_module(pirc)
        print(f"Loaded {pirc_file.stem} module from {pirc_file}")
        if hasattr(pirc, "mypaths"):
            for path in pirc.mypaths:
                addpath(path, verbose=True)


def __load_matplotlib_inline():
    """Loads the '%matplotlib inline' magic command in IPython if available."""
    try:
        ipython = get_ipython()
        if ipython:
            ipython.run_line_magic("matplotlib", "inline")
            print("Loaded '%matplotlib inline'")
    except ImportError:
        pass


################################################################################
# Bespoke functions ############################################################
################################################################################


def get_base_package(module):
    """Get the base package of a module.

    Args:
        module (module): The module to get the base package of.

    Returns:
        str: The base package of the module.
    """
    return module.__name__.split(".", maxsplit=1)[0]


def find_instances(cls, module, tracker_type=AttrDict, filter_func=None):
    """Find all instances of a class in a module or submodules."""
    if filter_func is None:

        def filter_func(*_):
            return True

    base_package = get_base_package(module)
    tracker = tracker_type()
    ModuleType = __types.ModuleType
    for name, obj in vars(module).items():
        if filter_func(name, obj):
            if isinstance(obj, cls):
                tracker[name] = obj
            elif isinstance(obj, ModuleType) and get_base_package(obj) == base_package:
                subtracker = find_instances(cls, obj, tracker_type, filter_func)
                if subtracker:
                    tracker[name] = subtracker
    return tracker
