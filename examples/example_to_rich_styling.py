#!/usr/bin/env python3
"""
Example demonstrating the to_rich method with pandas styling.

This example shows how to use the `.pirr.to_rich()` accessor method
with a background gradient styled DataFrame.
"""

import numpy as np
import pandas as pd
from rich.console import Console

import pirrtools

# Create sample data
np.random.seed(42)
data = {
    "Sales": [100, 150, 200, 175, 225, 190],
    "Profit": [20, 35, 50, 40, 60, 45],
    "Growth": [0.05, 0.12, 0.18, 0.15, 0.22, 0.19],
    "Rating": [3.2, 4.1, 4.8, 4.3, 4.9, 4.5],
}

df = pd.DataFrame(data, index=["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"])
print("Original DataFrame:")
print(df)
print()

# Create a styled version with background gradient
styled_df = df.style.background_gradient(cmap="viridis", axis=0)

# Initialize Rich console
console = Console()

print("DataFrame with background gradient styling using to_rich():")
print()

# Convert to Rich table with styling preserved
rich_table = df.pirr.to_rich(
    styler=styled_df, title="Sales Data with Background Gradient"
)

# Display the table
console.print(rich_table)

print("\n" + "=" * 60 + "\n")

# Example with different gradient and subset
print("Subset with different gradient (RdYlBu colormap):")
subset_styled = df[["Sales", "Profit"]].style.background_gradient(cmap="RdYlBu", axis=1)
rich_subset = df[["Sales", "Profit"]].pirr.to_rich(
    styler=subset_styled, title="Sales vs Profit Comparison", border_style="blue"
)
console.print(rich_subset)

print("\n" + "=" * 60 + "\n")

# Example with Series styling (create DataFrame with single column first)
print("Series with background gradient:")
growth_df = df[["Growth"]]
series_styled = growth_df.style.background_gradient(cmap="plasma")
rich_series = df["Growth"].pirr.to_rich(styler=None, title="Growth Rate (No Styling)")
console.print(rich_series)

print("\n" + "=" * 60 + "\n")

# Example showing the optimization for backgrounds
print("Comparison - Normal table vs Optimized for backgrounds:")
print("\nNormal table (no styling):")
normal_table = df.pirr.to_rich(title="Normal Table")
console.print(normal_table)

print("\nOptimized table (with background styling):")
optimized_table = df.pirr.to_rich(styler=styled_df, title="Background Optimized")
console.print(optimized_table)

print("\n" + "=" * 60 + "\n")

# Example with custom options
print("Custom styling options:")
custom_table = df.pirr.to_rich(
    styler=styled_df,
    title="Custom Styled Table",
    show_index=True,
    index_style="bold cyan",
    index_header_style="bold magenta",
    index_justify="center",
    border_style="green",
)
console.print(custom_table)
