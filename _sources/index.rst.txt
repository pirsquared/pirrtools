.. pirrtools documentation master file

=================================
pirrtools Documentation
=================================

A powerful collection of tools for data analysis, featuring enhanced pandas functionality, Rich table styling, and intelligent file system navigation.

.. image:: https://img.shields.io/pypi/v/pirrtools.svg
   :target: https://pypi.python.org/pypi/pirrtools
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/pirrtools.svg
   :target: https://pypi.python.org/pypi/pirrtools
   :alt: Python Versions

Quick Start
===========

Install pirrtools via pip:

.. code-block:: bash

   pip install pirrtools

Basic usage:

.. code-block:: python

   import pandas as pd
   import pirrtools
   from rich.console import Console
   
   # Create a DataFrame
   df = pd.DataFrame({
       'Sales': [150, 230, 180, 340],
       'Profit': [25, 45, 32, 68]
   })
   
   # Convert to styled Rich table
   console = Console()
   table = df.pirr.to_rich(bg="viridis", title="Sales Report")
   console.print(table)

Key Features
============

🎨 **Rich Table Styling**
   Convert pandas DataFrames and Series to beautifully styled Rich tables with gradients, custom headers, and professional theming.

💾 **Pandas Caching**
   Efficient caching system for pandas objects using feather format, perfect for large datasets and complex preprocessing.

📁 **AttrPath Navigation**
   Navigate file systems using dot notation with intelligent file viewing and organized directory structures.

🔧 **Development Utilities**
   Module reloading, path management, and development workflow enhancements.

Documentation Contents
======================

.. toctree::
   :maxdepth: 2
   :caption: User Guide
   
   to_rich_tutorial
   jupyter_example
   examples
   installation
   
.. toctree::
   :maxdepth: 2
   :caption: API Reference
   
   api_reference
   modules

.. toctree::
   :maxdepth: 1
   :caption: Development
   
   contributing
   changelog

Interactive Tutorial
===================

Get started quickly with the interactive tutorial:

.. code-block:: bash

   cd examples/
   python tutor.py

This hands-on tutorial walks through all ``to_rich`` features with live examples and step-by-step guidance.

Examples Directory
==================

The ``examples/`` directory contains comprehensive demonstrations:

* ``tutor.py`` - Interactive tutorial (recommended starting point)
* ``to_rich_examples.py`` - All styling features demonstrated
* ``example_to_rich_styling.py`` - Focus on gradient styling
* ``gradient_example.py`` - Simple gradient examples
* ``pandas_rich_styling_research.py`` - Technical implementation details

Core Modules
============

**pirrtools.pandas**
   Enhanced pandas functionality with caching and Rich table conversion via the ``.pirr`` accessor.

**pirrtools.structures.attrpath**
   File system navigation using attribute access with intelligent file viewing.

**pirrtools.structures.attrdict**
   Dictionary with attribute access capabilities.

**pirrtools utilities**
   Path management, module reloading, and development helpers.

Installation
============

Requirements
------------

* Python 3.8+
* pandas
* numpy  
* rich
* feather-format
* ipython
* pygments
* jinja2
* matplotlib

Development Installation
------------------------

For development work:

.. code-block:: bash

   git clone https://github.com/pirsquared/pirrtools.git
   cd pirrtools
   pip install -e .[dev]

This installs development dependencies including pytest, black, pylint, and documentation tools.

Docker Development
------------------

Use the provided Docker environment:

.. code-block:: bash

   docker-compose up -d
   docker-compose exec pirrtools-dev bash

Or with VS Code Dev Containers - open the project and select "Reopen in Container".

Contributing
============

Contributions are welcome! Please see the contributing guidelines for development setup, testing procedures, and code style requirements.

License
=======

This project is licensed under the MIT License. See the LICENSE file for details.

Support
=======

* GitHub Issues: https://github.com/pirsquared/pirrtools/issues
* PyPI Package: https://pypi.org/project/pirrtools/
* Documentation: https://pirrtools.readthedocs.io/ (coming soon)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`