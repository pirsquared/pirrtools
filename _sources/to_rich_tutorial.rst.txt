=======================
to_rich Method Tutorial
=======================

The ``to_rich`` method is pirrtools' flagship feature for converting pandas DataFrames and Series into beautifully styled Rich tables. This tutorial covers all styling options and provides examples for each feature.

.. contents::
   :local:
   :depth: 2

Overview
========

The ``.pirr.to_rich()`` accessor method extends pandas DataFrames and Series with Rich table styling capabilities. It supports:

- Background and text color gradients
- Custom header and index styling  
- Alternating row colors
- Integration with existing pandas Styler objects
- Professional table theming

Quick Start
===========

Basic usage is simple:

.. code-block:: python

   import pandas as pd
   import pirrtools
   from rich.console import Console
   
   # Create sample data
   df = pd.DataFrame({
       'Sales': [150, 230, 180],
       'Profit': [25, 45, 32]
   })
   
   # Convert to Rich table
   console = Console()
   table = df.pirr.to_rich(title="Sales Report")
   console.print(table)

Interactive Tutorial
===================

For hands-on learning, run the interactive tutorial:

.. code-block:: bash

   cd examples/
   python tutor.py

This script provides step-by-step guidance through all ``to_rich`` features with live examples.

Basic Usage
===========

Converting DataFrames
---------------------

.. code-block:: python

   # Basic conversion
   table = df.pirr.to_rich()
   
   # With title
   table = df.pirr.to_rich(title="My Report")
   
   # Hide index
   table = df.pirr.to_rich(show_index=False)

Converting Series
-----------------

.. code-block:: python

   series = pd.Series([85, 92, 78], name='Scores')
   table = series.pirr.to_rich()

Background Gradients
===================

Apply color gradients to table backgrounds for enhanced data visualization.

Basic Gradients
---------------

.. code-block:: python

   # Default gradient
   table = df.pirr.to_rich(bg="gradient")
   
   # Specific colormap
   table = df.pirr.to_rich(bg="viridis")
   table = df.pirr.to_rich(bg="plasma")
   table = df.pirr.to_rich(bg="coolwarm")

Available colormaps include: ``viridis``, ``plasma``, ``inferno``, ``magma``, ``cividis``, ``coolwarm``, ``RdYlBu``, ``RdYlGn``, ``spectral``, and more.

Gradient Direction
------------------

Control gradient application direction:

.. code-block:: python

   # Column-wise gradient (default)
   table = df.pirr.to_rich(bg="viridis", bg_kwargs={"axis": 0})
   
   # Row-wise gradient  
   table = df.pirr.to_rich(bg="viridis", bg_kwargs={"axis": 1})
   
   # Both directions
   table = df.pirr.to_rich(bg="viridis", bg_kwargs={"axis": None})

Subset Styling
--------------

Apply gradients to specific columns:

.. code-block:: python

   table = df.pirr.to_rich(
       bg="plasma", 
       bg_kwargs={"subset": ["Sales", "Profit"]}
   )

Text Gradients
==============

Apply color gradients to text for enhanced readability.

.. code-block:: python

   # Default text gradient
   table = df.pirr.to_rich(tg="gradient")
   
   # Specific colormap
   table = df.pirr.to_rich(tg="inferno")
   
   # Combined with background
   table = df.pirr.to_rich(bg="viridis", tg="plasma")

Header and Index Styling
========================

Customize headers and index appearance.

Column Headers
--------------

.. code-block:: python

   table = df.pirr.to_rich(
       column_header_style="bold white on blue"
   )

Index Styling
-------------

.. code-block:: python

   table = df.pirr.to_rich(
       index_style="italic green",
       index_header_style="bold yellow on red"
   )

Index Background Gradients
--------------------------

.. code-block:: python

   table = df.pirr.to_rich(
       index_bg="coolwarm",
       index_bg_kwargs={"cmap": "plasma"}
   )

Alternating Rows
===============

Improve readability with alternating row colors.

.. code-block:: python

   # Default alternating colors
   table = df.pirr.to_rich(alternating_rows=True)
   
   # Custom colors
   table = df.pirr.to_rich(
       alternating_rows=True,
       alternating_row_colors=("", "on dark_blue")
   )
   
   # With gradients
   table = df.pirr.to_rich(
       bg="gradient",
       alternating_rows=True,
       alternating_row_colors=("", "on grey15")
   )

Advanced Styling
===============

Professional Report Style
-------------------------

.. code-block:: python

   table = df.pirr.to_rich(
       bg="viridis",
       column_header_style="bold white on dark_blue",
       index_header_style="bold yellow on dark_red", 
       index_style="italic cyan",
       alternating_rows=True,
       alternating_row_colors=("", "on grey11"),
       title="📊 Quarterly Sales Report",
       border_style="blue"
   )

High Contrast Theme
------------------

.. code-block:: python

   table = df.pirr.to_rich(
       bg="coolwarm",
       column_header_style="bold black on bright_white",
       index_header_style="bold white on bright_black",
       table_style="bold",
       title="⚡ High Contrast Report",
       border_style="bright_yellow"
   )

Pandas Styler Integration
========================

Use existing pandas Styler objects with ``to_rich`` enhancements.

Basic Integration
----------------

.. code-block:: python

   # Create pandas styler
   styled_df = df.style.highlight_max(axis=0, color='lightblue')
   
   # Use with to_rich
   table = df.pirr.to_rich(
       styler=styled_df,
       title="Pandas Styler + to_rich"
   )

Style Override
--------------

Built-in ``to_rich`` options override pandas styler:

.. code-block:: python

   styled_df = df.style.background_gradient(cmap='Reds')
   
   # Blues gradient overrides Reds from styler
   table = df.pirr.to_rich(
       styler=styled_df,
       bg="Blues",
       title="Style Override"
   )

Complete Parameter Reference
===========================

Core Parameters
--------------

* ``title`` (str): Table title
* ``show_index`` (bool): Show DataFrame index (default: True)
* ``styler`` (pandas.Styler): Existing pandas Styler object

Background Styling  
-----------------

* ``bg`` (str): Background gradient colormap
* ``bg_kwargs`` (dict): Background gradient options
* ``index_bg`` (str): Index background gradient colormap  
* ``index_bg_kwargs`` (dict): Index background gradient options

Text Styling
------------

* ``tg`` (str): Text gradient colormap
* ``tg_kwargs`` (dict): Text gradient options

Header and Index
---------------

* ``column_header_style`` (str): Column header Rich style
* ``index_header_style`` (str): Index header Rich style
* ``index_style`` (str): Index values Rich style
* ``index_justify`` (str): Index text justification

Row Styling
-----------

* ``alternating_rows`` (bool): Enable alternating row colors
* ``alternating_row_colors`` (tuple): Custom row colors

Table Appearance
---------------

* ``table_style`` (str): Overall table Rich style
* ``border_style`` (str): Border color/style
* ``title_style`` (str): Title Rich style
* ``minimize_gaps`` (bool): Reduce cell padding

Examples
========

All examples are available in the ``examples/`` directory:

* ``tutor.py`` - Interactive tutorial (recommended starting point)
* ``to_rich_examples.py`` - Comprehensive examples of all features
* ``example_to_rich_styling.py`` - Gradient styling examples
* ``gradient_example.py`` - Simple gradient demonstrations
* ``to_rich_demo.py`` - Basic demos with multiple gradients

Run any example file to see the ``to_rich`` method in action:

.. code-block:: bash

   cd examples/
   python tutor.py               # Interactive learning
   python to_rich_examples.py    # All features demo
   python example_to_rich_styling.py  # Gradient focus

Color Reference
===============

Rich Color Formats
------------------

``to_rich`` supports all Rich color formats:

* **Named colors**: ``"red"``, ``"blue"``, ``"green"``
* **Hex colors**: ``"#ff0000"``, ``"#00ff00"``  
* **RGB colors**: ``"rgb(255,0,0)"``
* **Background**: ``"white on red"``, ``"bold blue on yellow"``
* **Styles**: ``"bold"``, ``"italic"``, ``"dim"``

Gradient Colormaps
-----------------

Popular matplotlib colormaps supported:

* **Sequential**: ``viridis``, ``plasma``, ``inferno``, ``magma``, ``cividis``
* **Diverging**: ``coolwarm``, ``RdYlBu``, ``RdYlGn``, ``spectral``
* **Qualitative**: ``tab10``, ``tab20``, ``set1``, ``set2``

See Also
========

* :doc:`api_reference` - Complete API documentation
* :doc:`examples` - Additional usage examples  
* `Rich Documentation <https://rich.readthedocs.io/>`_ - Rich library reference
* `Pandas Styling <https://pandas.pydata.org/docs/user_guide/style.html>`_ - Pandas styling guide