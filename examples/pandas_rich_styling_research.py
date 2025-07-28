#!/usr/bin/env python3
"""
Research demonstration for pandas Styler to Rich Table conversion.

This script demonstrates:
1. How pandas Styler works internally - particularly CSS style extraction
2. Rich Table styling capabilities for individual cells and columns
3. CSS color format conversion to Rich color formats
4. Methods to extract generated CSS from pandas Styler and map to Rich styling

Key findings from research:
- pandas Styler uses internal context dictionary (self.ctx) to map cell positions to CSS
- Rich supports hex colors directly (#RRGGBB) and RGB format rgb(r,g,b)
- Rich Table allows per-column styling and individual cell formatting
- Extraction possible through Styler._compute() and self.ctx access
"""

import re
from collections import defaultdict
from typing import Any, Dict, Optional, Tuple

import pandas as pd
from rich import box
from rich.console import Console
from rich.table import Table


def demonstrate_pandas_styler_internals():
    """Demonstrate how pandas Styler works internally with CSS generation."""

    # Create sample data
    df = pd.DataFrame(
        {"A": [1, 2, 3, 4], "B": [10, 20, 30, 40], "C": [0.1, 0.2, 0.3, 0.4]}
    )

    print("=== Pandas Styler Internal Mechanics ===")
    print("Original DataFrame:")
    print(df)
    print()

    # Create styled dataframe with background gradient
    styled = df.style.background_gradient(cmap="viridis", axis=None)

    print("Styler object before compute:")
    print(f"_todo list length: {len(styled._todo)}")
    print(f"ctx (context) keys before compute: {list(styled.ctx.keys())}")
    print()

    # Force computation of styles (this is normally done during rendering)
    styled._compute()

    print("After _compute() execution:")
    print(f"ctx keys: {list(styled.ctx.keys())}")
    print("Sample ctx entries:")
    for i, (key, value) in enumerate(styled.ctx.items()):
        if i < 3:  # Show first 3 entries
            print(f"  Position {key}: {value}")
    print()

    return styled, df


def demonstrate_css_extraction(styled_df):
    """Extract CSS styles from pandas Styler."""

    print("=== CSS Style Extraction ===")

    # Method 1: Access internal context directly
    print("Method 1: Direct ctx access")
    css_styles = {}
    for (row, col), styles in styled_df.ctx.items():
        css_styles[(row, col)] = styles
        if len(css_styles) <= 3:  # Show first few
            print(f"  Cell ({row},{col}): {styles}")

    print()

    # Method 2: Parse HTML output
    print("Method 2: Parse HTML output")
    html = styled_df.to_html()

    # Extract inline styles with regex
    style_pattern = r'style="([^"]*)"'
    styles = re.findall(style_pattern, html)
    print(f"Found {len(styles)} inline styles in HTML")
    if styles:
        print(f"Sample style: {styles[0]}")

    print()
    return css_styles


def parse_css_properties(css_string: str) -> Dict[str, str]:
    """Parse CSS property string into dictionary."""
    if not css_string:
        return {}

    properties = {}
    # Split by semicolon and parse each property
    for prop in css_string.split(";"):
        if ":" in prop:
            key, value = prop.split(":", 1)
            properties[key.strip()] = value.strip()

    return properties


def css_color_to_rich(css_color: str) -> str:
    """Convert CSS color to Rich color format."""
    # Rich supports CSS hex colors directly
    if css_color.startswith("#"):
        return css_color

    # Parse RGB format: rgb(r, g, b)
    rgb_pattern = r"rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)"
    match = re.match(rgb_pattern, css_color)
    if match:
        r, g, b = match.groups()
        return f"rgb({r},{g},{b})"

    # Return as-is for named colors
    return css_color


def create_rich_table_from_pandas(df: pd.DataFrame, styled_df) -> Table:
    """Create Rich Table from pandas DataFrame with extracted styles."""

    console = Console()

    # Create Rich table
    table = Table(title="Styled DataFrame in Rich", box=box.ROUNDED)

    # Add columns with styling
    for col in df.columns:
        table.add_column(str(col), justify="right", style="cyan")

    # Add rows with potential cell-specific styling
    for idx, row in df.iterrows():
        row_values = []
        for col_idx, (col, value) in enumerate(row.items()):
            # Look up styling for this cell
            cell_styles = styled_df.ctx.get((idx, col_idx), [])

            # Parse CSS and apply to Rich
            formatted_value = str(value)
            if cell_styles:
                # cell_styles is a list of tuples: [('background-color', '#46085c'), ('color', '#f1f1f1')]
                css_props = dict(cell_styles)
                if "background-color" in css_props:
                    bg_color = css_color_to_rich(css_props["background-color"])
                    # Rich syntax: text with background
                    formatted_value = (
                        f"[on {bg_color.replace('#', '')}]{formatted_value}[/]"
                    )

            row_values.append(formatted_value)

        table.add_row(*row_values)

    return table


def demonstrate_rich_styling_capabilities():
    """Demonstrate Rich Table styling capabilities."""

    print("=== Rich Table Styling Capabilities ===")

    console = Console()

    # Create a sample table with various styling options
    table = Table(title="Rich Styling Demo", box=box.DOUBLE_EDGE)

    # Column-level styling
    table.add_column("Name", justify="left", style="bold magenta", no_wrap=True)
    table.add_column("Score", justify="right", style="green")
    table.add_column("Status", justify="center", style="yellow")
    table.add_column("Notes", style="dim")

    # Rows with cell-specific styling
    table.add_row("Alice", "95", "[green]PASS[/]", "[italic]Excellent work[/]")
    table.add_row("Bob", "78", "[yellow]REVIEW[/]", "[dim]Needs improvement[/]")
    table.add_row("Charlie", "92", "[green]PASS[/]", "[bold]Outstanding[/]")

    # Row with background colors
    table.add_row(
        "[on blue]Diana[/]",
        "[on green]98[/]",
        "[on cyan]PASS[/]",
        "[on yellow black]Perfect score![/]",
    )

    console.print(table)
    print()

    # Demonstrate color formats
    print("Rich Color Format Examples:")
    console.print("Hex color: ", style="#ff6b6b", end="")
    console.print("Red text")
    console.print("RGB color: ", style="rgb(107,203,119)", end="")
    console.print("Green text")
    console.print("Named color: ", style="blue", end="")
    console.print("Blue text")
    console.print("Background: ", style="white on red", end="")
    console.print("White on red")
    print()


def demonstrate_integration():
    """Demonstrate full integration of pandas Styler to Rich Table."""

    print("=== Integration Example: Pandas to Rich ===")

    # Create and style pandas dataframe
    styled_df, df = demonstrate_pandas_styler_internals()

    # Extract CSS styles
    css_styles = demonstrate_css_extraction(styled_df)

    # Create Rich table
    console = Console()
    rich_table = create_rich_table_from_pandas(df, styled_df)

    print("Rich Table with extracted pandas styling:")
    console.print(rich_table)
    print()


def main():
    """Main research demonstration."""

    print("PANDAS STYLER TO RICH TABLE STYLING RESEARCH")
    print("=" * 60)
    print()

    # Demonstrate pandas styler internals
    demonstrate_pandas_styler_internals()
    print()

    # Demonstrate Rich styling capabilities
    demonstrate_rich_styling_capabilities()
    print()

    # Show full integration
    demonstrate_integration()

    print("\nKey Research Findings:")
    print("=" * 40)
    print("1. pandas Styler uses self.ctx dictionary mapping (row,col) to CSS styles")
    print("2. Access via styled_df._compute() then styled_df.ctx")
    print("3. Rich supports CSS hex colors directly: #RRGGBB")
    print("4. Rich table styling: per-column styles, cell-specific markup")
    print("5. CSS background-color becomes Rich 'on color' syntax")
    print("6. Full integration possible through CSS parsing and mapping")


if __name__ == "__main__":
    main()
