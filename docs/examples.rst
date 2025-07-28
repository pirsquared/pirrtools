=================
Examples Gallery
=================

This section showcases various ways to use pirrtools features through practical examples.

Interactive Tutorial
====================

The best way to learn pirrtools is through the interactive tutorial:

.. code-block:: bash

   cd examples/
   python tutor.py

This script provides hands-on, step-by-step guidance through all ``to_rich`` features.

Example Files
=============

All examples are located in the ``examples/`` directory:

Core Examples
-------------

**tutor.py**
   Interactive tutorial with guided lessons covering all ``to_rich`` features. Recommended starting point for new users.

**to_rich_examples.py**  
   Comprehensive demonstration of all styling options and combinations. Shows every parameter and feature available.

**example_to_rich_styling.py**
   Focused examples of background gradient styling with various colormaps and configurations.

**gradient_example.py**
   Simple, clean examples showing basic gradient applications for quick reference.

**to_rich_demo.py**
   Basic demonstrations with multiple gradient types and comparison views.

Research and Technical
----------------------

**pandas_rich_styling_research.py**
   Technical deep-dive into how pandas Styler integration works internally. Useful for understanding implementation details.

**test_full_width_backgrounds.py**
   Demonstrates full-width background color functionality and optimization for styled tables.

**test_padding.py**
   Shows enhanced background padding behavior with varied text lengths.

Quick Examples
==============

Basic Rich Table
----------------

.. code-block:: python

   import pandas as pd
   import pirrtools
   from rich.console import Console
   
   df = pd.DataFrame({
       'Product': ['Widget A', 'Widget B', 'Widget C'],
       'Sales': [150, 230, 180],
       'Profit': [25, 45, 32]
   })
   
   console = Console()
   table = df.pirr.to_rich(title="Sales Report")
   console.print(table)

Background Gradients
-------------------

.. code-block:: python

   # Viridis colormap gradient
   table = df.pirr.to_rich(bg="viridis", title="Gradient Table")
   console.print(table)
   
   # Row-wise gradient
   table = df.pirr.to_rich(
       bg="plasma", 
       bg_kwargs={"axis": 1},
       title="Row-wise Gradient"
   )
   console.print(table)

Professional Styling
--------------------

.. code-block:: python

   table = df.pirr.to_rich(
       bg="viridis",
       column_header_style="bold white on dark_blue",
       index_header_style="bold yellow on dark_red",
       alternating_rows=True,
       alternating_row_colors=("", "on grey11"),
       title="📊 Professional Report",
       border_style="blue"
   )
   console.print(table)

Pandas Caching
===============

Save and Load DataFrames
------------------------

.. code-block:: python

   import pandas as pd
   from pirrtools import cache_and_load
   
   # Create expensive-to-compute DataFrame
   df = pd.DataFrame({
       'data': range(1000000),
       'computed': [x**2 for x in range(1000000)]
   })
   
   # Cache and load (saves time on subsequent runs)
   cached_df = cache_and_load(df, 'my_cache_dir')

Using the .pirr Accessor
-----------------------

.. code-block:: python

   # Save cache using accessor
   df.pirr.save_cache('cache_directory')
   
   # Load cache
   from pirrtools import load_cache
   loaded_df = load_cache('cache_directory')

AttrPath Navigation
==================

File System Exploration
-----------------------

.. code-block:: python

   from pirrtools.structures import AttrPath
   
   # Navigate using dot notation
   root = AttrPath('.')
   
   # Access subdirectories
   examples = root.examples
   
   # View files by extension
   print(examples.F.py)  # All .py files
   print(examples.D)     # All directories
   
   # View file contents with syntax highlighting
   examples.tutor_py.view()

Intelligent File Viewing
------------------------

.. code-block:: python

   # AttrPath automatically handles different file types:
   
   path = AttrPath('/path/to/files')
   
   # Images display inline (in Jupyter)
   path.image_jpg.view()
   
   # CSV files show as formatted tables
   path.data_csv.view()
   
   # Code files get syntax highlighting
   path.script_py.view()
   
   # HTML files render in browser
   path.report_html.view()

AttrDict Usage
==============

Dictionary with Attribute Access
--------------------------------

.. code-block:: python

   from pirrtools.structures import AttrDict
   
   # Create AttrDict
   config = AttrDict({
       'database': {
           'host': 'localhost',
           'port': 5432
       },
       'debug': True
   })
   
   # Access using attributes or keys
   print(config.database.host)  # 'localhost'
   print(config['database']['port'])  # 5432
   
   # Nested access
   config.api.endpoints.users = '/api/v1/users'

Development Utilities
====================

Path Management
---------------

.. code-block:: python

   from pirrtools import addpath
   
   # Add development paths
   addpath('/path/to/my/modules', verbose=True)
   addpath('~/development/utils')

Module Reloading
----------------

.. code-block:: python

   from pirrtools import reload_entity
   import my_module
   
   # Reload module during development
   my_module = reload_entity(my_module)
   
   # Reload class
   MyClass = reload_entity(MyClass)

Running Examples
================

To run any example:

.. code-block:: bash

   # Interactive tutorial
   cd examples/
   python tutor.py
   
   # Comprehensive examples
   python to_rich_examples.py
   
   # Specific feature demos
   python example_to_rich_styling.py
   python gradient_example.py

Tips for Examples
=================

1. **Start with tutor.py** - It provides the best learning experience
2. **Experiment** - Modify examples to see how different parameters work
3. **Check source code** - Examples show implementation patterns
4. **Use Rich Console** - Always create a Console() instance for proper display
5. **Try your data** - Apply techniques to your own DataFrames for practical learning

Next Steps
==========

After exploring examples:

- Read the :doc:`to_rich_tutorial` for comprehensive parameter reference
- Check the :doc:`api_reference` for detailed function documentation  
- Contribute examples via GitHub issues or pull requests