# pirrtools

*I find them useful*

## Description

`pirrtools` is a set of bespoke tools I wanted preserved in a library. It provides various utilities, with a key feature being a pandas accessor that enables caching of usually non-conforming datasets.

## Features

- **Pandas Accessor**: Easily cache and load pandas DataFrames and Series, even those with non-conforming datasets.

## Requirements

- Python 3.6 or greater
- pandas
- feather-format

## Installation

Install `pirrtools` using pip:

```bash
pip install pirrtools
```

## Usage

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

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Authors
- Sean Smith