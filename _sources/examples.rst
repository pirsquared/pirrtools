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

.. rich-table::
   :width: 600px

   import pandas as pd
   import pirrtools
   from rich.console import Console
   
   console = Console()
   
   # Create sample data
   df = pd.DataFrame({
       'Q1': [100, 150, 200],
       'Q2': [120, 180, 220], 
       'Q3': [140, 200, 180],
       'Q4': [160, 170, 240]
   }, index=['Product A', 'Product B', 'Product C'])
   
   # Viridis colormap gradient
   table = df.pirr.to_rich(bg="viridis", title="📊 Quarterly Performance")
   console.print(table)

Professional Styling
--------------------

.. rich-table::
   :width: 700px

   import pandas as pd
   import pirrtools
   from rich.console import Console
   
   console = Console()
   
   # Create financial data
   df = pd.DataFrame({
       'Q1': [100.5, 150.3, 200.8],
       'Q2': [120.2, 180.7, 220.1], 
       'Q3': [140.9, 200.4, 180.6],
       'Q4': [160.1, 170.8, 240.3]
   }, index=['Revenue', 'Profit', 'Growth'])
   
   # Professional styling with format
   table = df.pirr.to_rich(
       bg="viridis",
       format="${:.1f}K",
       column_header_style="bold white on dark_blue",
       index_header_style="bold yellow on dark_red",
       alternating_rows=True,
       alternating_row_colors=("", "on grey11"),
       title="📊 Professional Financial Report"
   )
   console.print(table)

Pandas Caching
===============

Save and Load DataFrames
------------------------

.. code-block:: python

   import pandas as pd
   from pirrtools.pandas import cache_and_load
   
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
   df.pirr.to_cache('cache_directory')
   
   # Load cache
   from pirrtools.pandas import load_cache
   loaded_df = load_cache('cache_directory')


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
