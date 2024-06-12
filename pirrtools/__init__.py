import sys as __sys
import pathlib as __pathlib
import importlib as __importlib
import importlib.util as __importlib_util
import types as __types
from .pandas import load_cache

__HOME = __pathlib.Path.home().absolute()


def addpath(path, position=0, verbose=False):
    path = __pathlib.Path(path).expanduser().absolute()
    if path not in __sys.path:
        __sys.path.insert(position, str(path))
        if verbose:
            print(f'added "{str(path)}" into system path at position {position}')

def reload_entity(entity):
    """
    Reloads the given module or class. If a class is provided, its module is reloaded,
    and then the class is re-imported from this module.

    Args:
        entity: The module or class to reload.

    Returns:
        The reloaded module or class.
    """

    if isinstance(entity, __types.ModuleType):
        # It's a module, reload directly
        return __importlib.reload(entity)
    else:
        # It's assumed to be a class, get its module
        module_name = entity.__module__
        module = __importlib.import_module(module_name)
        # Reload the module
        reloaded_module = __importlib.reload(module)
        # Re-import and return the class from the reloaded module
        return getattr(reloaded_module, entity.__name__)
    
# Look for `.pirc` file in the home directory
def __get_pirc_file():
    pirc_file = __HOME / '.pirc.py'
    if pirc_file.exists():
        return pirc_file

def __load_pirc_file():
    pirc_file = __get_pirc_file()
    if pirc_file:
        spec = __importlib_util.spec_from_file_location("pirc", pirc_file)
        pirc = __importlib_util.module_from_spec(spec)
        spec.loader.exec_module(pirc)
        print(f'Loaded {pirc_file.stem} module from {pirc_file}')
        if hasattr(pirc, 'mypaths'):
            for path in pirc.mypaths:
                addpath(path, verbose=True)

def __load_matplotlib_inline():
    try:
        from IPython import get_ipython
        ipython = get_ipython()
        if ipython:
            ipython.run_line_magic('matplotlib', 'inline')
            print("Loaded '%matplotlib inline'")
    except ImportError:
        pass

__load_matplotlib_inline()
__load_pirc_file()
