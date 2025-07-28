============
Installation
============

This guide covers different ways to install and set up pirrtools for various use cases.

Quick Installation
==================

Install from PyPI (recommended):

.. code-block:: bash

   pip install pirrtools

This installs pirrtools and all required dependencies.

Requirements
============

**Python Version**
   Python 3.8 or higher is required.

**Core Dependencies**
   - pandas - DataFrame and Series manipulation
   - numpy - Numerical computing
   - rich - Terminal styling and Rich tables
   - feather-format - Fast DataFrame serialization
   - ipython - Interactive Python shell
   - pygments - Code syntax highlighting
   - jinja2 - Templating engine
   - matplotlib - Plotting (for IPython integration)

Development Installation
========================

For development work or to get the latest features:

.. code-block:: bash

   git clone https://github.com/pirsquared/pirrtools.git
   cd pirrtools
   pip install -e .[dev]

This installs pirrtools in editable mode with development dependencies:

- pytest - Testing framework
- pytest-cov - Coverage reporting
- build - Package building
- twine - PyPI publishing
- black - Code formatting
- pre-commit - Git hooks
- pylint - Code linting

Docker Development Environment
==============================

Use the provided Docker setup for consistent development:

**Docker Compose**

.. code-block:: bash

   # Start development container
   docker-compose up -d
   
   # Access container shell
   docker-compose exec pirrtools-dev bash
   
   # Run commands in container
   docker-compose run --rm pirrtools-dev pytest
   docker-compose run --rm pirrtools-dev black pirrtools tests

**VS Code Dev Container**

1. Open the project in VS Code
2. Install the "Dev Containers" extension
3. Use Command Palette > "Dev Containers: Reopen in Container"
4. VS Code will automatically build and open the development environment

The container includes:
- Python 3.11
- All dependencies pre-installed
- VS Code extensions for Python development
- Pre-commit hooks configured

Virtual Environment Setup
=========================

Create an isolated environment:

**Using venv:**

.. code-block:: bash

   python -m venv pirrtools-env
   source pirrtools-env/bin/activate  # On Windows: pirrtools-env\\Scripts\\activate
   pip install pirrtools

**Using conda:**

.. code-block:: bash

   conda create -n pirrtools python=3.9
   conda activate pirrtools
   pip install pirrtools

Verification
============

Test your installation:

.. code-block:: python

   import pirrtools
   import pandas as pd
   from rich.console import Console
   
   # Create test DataFrame
   df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
   
   # Test Rich table conversion
   console = Console()
   table = df.pirr.to_rich(title="Test Table")
   console.print(table)
   
   print("✅ pirrtools installed successfully!")

Run the interactive tutorial:

.. code-block:: bash

   python -c "
   import subprocess
   import sys
   from pathlib import Path
   
   # Find examples directory
   import pirrtools
   pkg_path = Path(pirrtools.__file__).parent.parent
   examples_path = pkg_path / 'examples'
   
   if examples_path.exists():
       subprocess.run([sys.executable, str(examples_path / 'tutor.py')])
   else:
       print('Examples not found. Clone the repository for full examples.')
   "

Configuration
=============

**IPython Integration**

pirrtools automatically configures matplotlib inline mode in IPython/Jupyter environments.

**Custom Configuration**

Create a ``.pirc.py`` file in your home directory to customize paths:

.. code-block:: python

   # ~/.pirc.py
   mypaths = [
       '/path/to/my/modules',
       '/another/development/path'
   ]

These paths will be automatically added to sys.path when pirrtools is imported.

Troubleshooting
===============

**Import Errors**

If you encounter import errors, ensure all dependencies are installed:

.. code-block:: bash

   pip install --upgrade pirrtools

**Permission Issues**

On some systems, you may need to use ``--user`` flag:

.. code-block:: bash

   pip install --user pirrtools

**Development Dependencies**

If development dependencies fail to install:

.. code-block:: bash

   pip install --upgrade pip setuptools wheel
   pip install -e .[dev]

**Docker Issues**

If Docker commands fail:

1. Ensure Docker is running
2. Check Docker Compose version (v2+ recommended)
3. Try rebuilding: ``docker-compose build --no-cache``

**Rich Display Issues**

If Rich tables don't display correctly:

1. Ensure terminal supports color
2. Update terminal if using old version
3. Try in Jupyter notebook for best experience

Getting Help
============

If you encounter issues:

1. Check the GitHub Issues: https://github.com/pirsquared/pirrtools/issues
2. Review the documentation: :doc:`api_reference`
3. Try the examples: :doc:`examples`
4. Create a new issue with error details

Upgrading
=========

To upgrade to the latest version:

.. code-block:: bash

   pip install --upgrade pirrtools

Check your version:

.. code-block:: python

   import pirrtools
   print(pirrtools.__version__)

Uninstalling
============

To remove pirrtools:

.. code-block:: bash

   pip uninstall pirrtools

This removes pirrtools but leaves dependencies installed. To remove dependencies, you may need to uninstall them manually or recreate your virtual environment.