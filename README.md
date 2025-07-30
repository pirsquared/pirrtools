# pirrtools

*I find them useful*

## Description

`pirrtools` is a set of bespoke tools I wanted preserved in a library. It provides various utilities, with key features including a pandas accessor for caching non-conforming datasets and beautiful Rich table formatting.

## Documentation

📚 **[Full Documentation](https://pirsquared.github.io/pirrtools/)** - Complete guides, examples, and API reference

## Features

- **Rich Table Formatting**: Transform pandas DataFrames into beautiful, styled terminal tables with gradients, colors, and professional formatting
- **Pandas Caching**: Easily cache and load pandas DataFrames and Series, even those with non-conforming datasets using feather format
- **Interactive Tutorial**: Launch an interactive tutorial with `pirrtools-tutorial` command
- **Development Utilities**: Path management, module reloading, and instance finding tools

## Requirements

- Python 3.9 or greater
- pandas
- rich
- feather-format

## Installation

Install `pirrtools` using pip:

```bash
pip install pirrtools
```

## Quick Start

### Beautiful Rich Tables

```python
import pandas as pd
import pirrtools
from rich.console import Console

# Create sample data
df = pd.DataFrame({
    'Product': ['Widget A', 'Widget B', 'Widget C'],
    'Q1': [100, 150, 200],
    'Q2': [120, 180, 220], 
    'Q3': [140, 200, 180],
    'Q4': [160, 170, 240]
})

# Create beautiful table with gradient background
console = Console()
table = df.pirr.to_rich(
    bg="viridis",  # Gradient colormap
    title="📊 Quarterly Sales Report",
    format="${:.0f}K"  # Format numbers
)
console.print(table)
```

### Pandas Caching

```python
import pirrtools as pirr
import pandas as pd

# Create a DataFrame
df = pd.DataFrame(1, range(10), ['a', 'b', 'c']).rename_axis('N')

# Cache the DataFrame
df.pirr.to_cache('name_of_cache_path')

# Load the cached DataFrame
loaded_df = pirr.load_cache('name_of_cache_path')
```

### Interactive Tutorial

```bash
# Launch interactive tutorial
pirrtools-tutorial
```

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Authors
- Sean Smith