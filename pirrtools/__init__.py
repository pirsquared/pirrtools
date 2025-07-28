"""Main entry point for the pirrtools package.

This module provides core utility functions for path management, module reloading,
and environment setup. It automatically loads configuration from `.pirc` files
and sets up matplotlib inline mode for IPython environments.

The module exposes key functionality from submodules and provides utilities for:
- System path manipulation
- Module and class reloading
- Configuration file loading
- IPython environment setup

Example:
    >>> from pirrtools import addpath, reload_entity
    >>> addpath('/my/custom/path')
    >>> reloaded_module = reload_entity(my_module)
"""

import importlib as __importlib
import importlib.util as __importlib_util
import pathlib as __pathlib
import sys as __sys
import types as __types

from IPython import get_ipython

from .pandas import load_cache  # noqa: F401
from .structures import AttrDict, AttrPath  # noqa: F401

__HOME = __pathlib.Path.home().absolute()


def addpath(path, position=0, verbose=False):
    """Add a path to the system path at the specified position.

    Args:
        path (str): The path to add to sys.path.
        position (int, optional): The position in sys.path where the path should
            be inserted. Defaults to 0 (beginning of path).
        verbose (bool, optional): Whether to print a confirmation message when
            the path is added. Defaults to False.

    Note:
        The path is expanded and converted to absolute form before adding.
        Duplicate paths are not added.
    """
    path = __pathlib.Path(path).expanduser().absolute()
    path_str = str(path)
    # Remove all existing occurrences of the path
    __sys.path = [p for p in __sys.path if p != path_str]
    __sys.path.insert(position, path_str)
    if verbose:
        print(f'added "{path_str}" into system path at position {position}')


def reload_entity(entity):
    """Reload a module or class.

    If a class is provided, its module is reloaded and the class is
    re-imported from the reloaded module.

    Args:
        entity (module or class): The module or class to reload.

    Returns:
        module or class: The reloaded module or class.

    Example:
        >>> import my_module
        >>> reloaded_module = reload_entity(my_module)
        >>> reloaded_class = reload_entity(MyClass)
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
    """Look for a `.pirc.py` file in the home directory.

    Returns:
        pathlib.Path or None: The path to the `.pirc.py` file if it exists,
            None otherwise.
    """
    pirc_file = __HOME / ".pirc.py"
    if pirc_file.exists():
        return pirc_file
    return None


def load_pirc_file(verbose=False):
    """Load the `.pirc` module from the home directory and add specified paths.

    This function loads the `.pirc.py` file from the home directory and
    automatically adds any paths specified in the `mypaths` variable to
    the system path.

    Args:
        verbose (bool, optional): Whether to print status messages.
            Defaults to False.
    """
    pirc_file = __get_pirc_file()
    if pirc_file:
        spec = __importlib_util.spec_from_file_location("pirc", pirc_file)
        pirc = __importlib_util.module_from_spec(spec)
        spec.loader.exec_module(pirc)
        if verbose:
            print(f"Loaded {pirc_file.stem} module from {pirc_file}")
        if hasattr(pirc, "mypaths"):
            for path in pirc.mypaths:
                addpath(path, verbose=verbose)


def load_matplotlib_inline(verbose=False):
    """Load the '%matplotlib inline' magic command in IPython if available.

    Args:
        verbose (bool, optional): Whether to print status messages.
            Defaults to False.
    """
    try:
        ipython = get_ipython()
        if ipython:
            ipython.run_line_magic("matplotlib", "inline")
            if verbose:
                print("Loaded '%matplotlib inline'")
    except ImportError:
        pass


################################################################################
# Bespoke functions ############################################################
################################################################################


def get_base_package(module):
    """Get the base package name of a module.

    Args:
        module (module): The module to get the base package of.

    Returns:
        str: The name of the base package (first component of module.__name__).

    Example:
        >>> import numpy.linalg
        >>> get_base_package(numpy.linalg)
        'numpy'
    """
    return module.__name__.split(".", maxsplit=1)[0]


def find_instances(cls, module, tracker_type=AttrDict, filter_func=None):
    """Find all instances of a class in a module and its submodules.

    Args:
        cls (type): The class type to search for instances of.
        module (module): The module to search in.
        tracker_type (type, optional): The container type to use for results.
            Defaults to AttrDict.
        filter_func (callable, optional): A function to filter results.
            Should accept (name, obj) and return bool. If None, no filtering
            is applied.

    Returns:
        tracker_type: A nested structure containing found instances,
            organized by module hierarchy.

    Example:
        >>> instances = find_instances(MyClass, my_module)
        >>> print(instances.submodule.instance_name)
    """
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
