#!/usr/bin/env python3
"""
Test demonstrating full-width background colors with to_rich method.
"""

import numpy as np
import pandas as pd
from rich.console import Console

import pirrtools

# Create a DataFrame with different value ranges for better gradient demonstration
df = pd.DataFrame(
    {
        "Small": [1, 2, 3, 4, 5],
        "Medium": [10, 20, 30, 40, 50],
        "Large": [100, 200, 300, 400, 500],
    },
    index=["A", "B", "C", "D", "E"],
)

console = Console()

print("Testing full-width background colors:")
print("=" * 50)
print()

# Test 1: Strong gradient with high contrast
print("1. High contrast gradient (RdYlBu colormap):")
styled_high_contrast = df.style.background_gradient(cmap="RdYlBu", axis=0)
table_high_contrast = df.pirr.to_rich(
    styler=styled_high_contrast, title="High Contrast Background Gradient"
)
console.print(table_high_contrast)
print()

# Test 2: Different axis for gradient
print("2. Row-wise gradient (axis=1):")
styled_row_wise = df.style.background_gradient(cmap="viridis", axis=1)
table_row_wise = df.pirr.to_rich(
    styler=styled_row_wise, title="Row-wise Gradient (Each row gets its own gradient)"
)
console.print(table_row_wise)
print()

# Test 3: Subset with specific styling
print("3. Two-column subset with Spectral colormap:")
subset = df[["Small", "Large"]]
styled_subset = subset.style.background_gradient(cmap="Spectral", axis=0)
table_subset = subset.pirr.to_rich(
    styler=styled_subset,
    title="Small vs Large Comparison",
    index_style="bold white",
    border_style="bright_blue",
)
console.print(table_subset)
print()

# Test 4: Show the difference with and without styling
print("4. Comparison - Same data with and without background styling:")
print("\nWithout styling (normal table):")
normal_table = df.pirr.to_rich(title="Normal Table")
console.print(normal_table)

print("\nWith background styling (expanded table):")
styled_table = df.pirr.to_rich(
    styler=df.style.background_gradient(cmap="plasma"), title="Background Styled Table"
)
console.print(styled_table)
