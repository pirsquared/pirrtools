#!/usr/bin/env python3
"""
Simple demo of to_rich method with background gradient styling.
"""

import numpy as np
import pandas as pd
from rich.console import Console

import pirrtools

# Create a simple DataFrame with numeric data
np.random.seed(42)
df = pd.DataFrame(
    {"A": [1, 5, 10, 15, 20], "B": [2, 8, 12, 18, 25], "C": [3, 6, 9, 14, 22]},
    index=["Row1", "Row2", "Row3", "Row4", "Row5"],
)

print("Original DataFrame:")
print(df)
print()

# Create console
console = Console()

print("1. Basic Rich table (no styling):")
basic_table = df.pirr.to_rich(title="Basic Table")
console.print(basic_table)
print()

print("2. DataFrame with background gradient - viridis colormap:")
# Apply background gradient styling
styled_viridis = df.style.background_gradient(cmap="viridis", axis=0)
rich_viridis = df.pirr.to_rich(
    styler=styled_viridis, title="Viridis Background Gradient"
)
console.print(rich_viridis)
print()

print("3. DataFrame with background gradient - plasma colormap:")
styled_plasma = df.style.background_gradient(cmap="plasma", axis=0)
rich_plasma = df.pirr.to_rich(styler=styled_plasma, title="Plasma Background Gradient")
console.print(rich_plasma)
print()

print("4. Subset columns with different gradient:")
subset = df[["A", "B"]]
styled_subset = subset.style.background_gradient(cmap="coolwarm", axis=1)
rich_subset = subset.pirr.to_rich(
    styler=styled_subset, title="A vs B Comparison (CoolWarm)", border_style="cyan"
)
console.print(rich_subset)
print()

print("5. Custom styling options with gradient:")
custom_styled = df.style.background_gradient(cmap="RdYlBu", axis=0)
custom_table = df.pirr.to_rich(
    styler=custom_styled,
    title="Custom Styled Table",
    index_style="bold blue",
    index_header_style="bold magenta",
    border_style="green",
)
console.print(custom_table)
