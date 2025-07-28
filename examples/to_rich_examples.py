#!/usr/bin/env python3
"""
Comprehensive examples showcasing all to_rich functionality variations.
This script demonstrates the enhanced to_rich method with built-in styling options.
"""

import numpy as np
import pandas as pd
from rich.console import Console

from pirrtools import *  # Import pirrtools to get the .pirr accessor


def create_sample_data():
    """Create sample DataFrame and Series for demonstrations."""
    np.random.seed(42)

    # Create a sample DataFrame
    df = pd.DataFrame(
        {
            "Sales": np.random.randint(100, 1000, 8),
            "Profit": np.random.randint(10, 100, 8),
            "Growth": np.random.uniform(-0.2, 0.3, 8),
            "Region": ["North", "South", "East", "West"] * 2,
        },
        index=[f"Q{i//2 + 1}-{2023 + i%2}" for i in range(8)],
    )

    # Create a sample Series
    series = pd.Series(
        np.random.randint(50, 500, 6),
        index=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        name="Revenue",
    )

    return df, series


def demo_basic_usage(df, series, console):
    """Demonstrate basic usage without styling."""
    console.print("\n[bold blue]═══ BASIC USAGE ═══[/bold blue]")

    console.print("\n[yellow]Basic DataFrame:[/yellow]")
    console.print(df.pirr.to_rich())

    console.print("\n[yellow]Basic Series:[/yellow]")
    console.print(series.pirr.to_rich())

    console.print("\n[yellow]Hide Index:[/yellow]")
    console.print(df.head(3).pirr.to_rich(show_index=False))


def demo_background_gradients(df, console):
    """Demonstrate background gradient options."""
    console.print("\n[bold blue]═══ BACKGROUND GRADIENTS ═══[/bold blue]")

    console.print("\n[yellow]Default Background Gradient:[/yellow]")
    console.print(df.head(4).pirr.to_rich(bg="gradient"))

    console.print("\n[yellow]Viridis Colormap (column-wise):[/yellow]")
    console.print(df.head(4).pirr.to_rich(bg="viridis", bg_kwargs={"axis": 0}))

    console.print("\n[yellow]Plasma Colormap (row-wise):[/yellow]")
    console.print(df.head(4).pirr.to_rich(bg="plasma", bg_kwargs={"axis": 1}))

    console.print("\n[yellow]Custom Colormap with Subset:[/yellow]")
    console.print(
        df.head(4).pirr.to_rich(
            bg="coolwarm", bg_kwargs={"subset": ["Sales", "Profit"]}
        )
    )


def demo_text_gradients(df, console):
    """Demonstrate text gradient options."""
    console.print("\n[bold blue]═══ TEXT GRADIENTS ═══[/bold blue]")

    console.print("\n[yellow]Default Text Gradient:[/yellow]")
    console.print(df.head(4).pirr.to_rich(tg="gradient"))

    console.print("\n[yellow]Inferno Text Gradient:[/yellow]")
    console.print(df.head(4).pirr.to_rich(tg="inferno"))

    console.print("\n[yellow]Combined Background + Text Gradients:[/yellow]")
    console.print(
        df.head(4).pirr.to_rich(
            bg="viridis", tg="plasma", bg_kwargs={"axis": 0}, tg_kwargs={"axis": 1}
        )
    )


def demo_header_styling(df, series, console):
    """Demonstrate column header styling options."""
    console.print("\n[bold blue]═══ HEADER STYLING ═══[/bold blue]")

    console.print("\n[yellow]Custom Column Headers:[/yellow]")
    console.print(df.head(4).pirr.to_rich(column_header_style="bold white on blue"))

    console.print("\n[yellow]Custom Index Headers:[/yellow]")
    console.print(
        df.head(4).pirr.to_rich(
            index_header_style="bold yellow on red", index_style="italic green"
        )
    )

    console.print("\n[yellow]Series with Custom Headers:[/yellow]")
    console.print(
        series.head(4).pirr.to_rich(
            column_header_style="bold magenta on white",
            index_header_style="bold cyan on black",
        )
    )


def demo_index_styling(df, console):
    """Demonstrate index-specific styling."""
    console.print("\n[bold blue]═══ INDEX STYLING ═══[/bold blue]")

    console.print("\n[yellow]Index Background Gradient:[/yellow]")
    console.print(
        df.head(4).pirr.to_rich(index_bg="gradient", index_bg_kwargs={"cmap": "plasma"})
    )

    console.print("\n[yellow]Combined Data + Index Gradients:[/yellow]")
    console.print(
        df.head(4).pirr.to_rich(
            bg="viridis", index_bg="coolwarm", bg_kwargs={"axis": 0}
        )
    )


def demo_alternating_rows(df, console):
    """Demonstrate alternating row styling."""
    console.print("\n[bold blue]═══ ALTERNATING ROWS ═══[/bold blue]")

    console.print("\n[yellow]Default Alternating Rows:[/yellow]")
    console.print(df.head(6).pirr.to_rich(alternating_rows=True))

    console.print("\n[yellow]Custom Alternating Colors:[/yellow]")
    console.print(
        df.head(6).pirr.to_rich(
            alternating_rows=True, alternating_row_colors=("", "on dark_blue")
        )
    )

    console.print("\n[yellow]Alternating + Background Gradient:[/yellow]")
    console.print(
        df.head(6).pirr.to_rich(
            alternating_rows=True,
            bg="gradient",
            alternating_row_colors=("", "on grey15"),
        )
    )


def demo_table_wide_styling(df, console):
    """Demonstrate table-wide styling options."""
    console.print("\n[bold blue]═══ TABLE-WIDE STYLING ═══[/bold blue]")

    console.print("\n[yellow]Table Style with Title:[/yellow]")
    console.print(
        df.head(4).pirr.to_rich(
            table_style="bold", title="📊 Sales Report", border_style="bright_blue"
        )
    )

    console.print("\n[yellow]Minimal Table with Custom Box:[/yellow]")
    console.print(
        df.head(4).pirr.to_rich(
            minimize_gaps=True, border_style="red", title_style="bold red"
        )
    )


def demo_complex_combinations(df, console):
    """Demonstrate complex styling combinations."""
    console.print("\n[bold blue]═══ COMPLEX COMBINATIONS ═══[/bold blue]")

    console.print("\n[yellow]Everything Combined (Subtle):[/yellow]")
    console.print(
        df.head(5).pirr.to_rich(
            bg="viridis",
            tg="plasma",
            column_header_style="bold white on dark_blue",
            index_header_style="bold yellow on dark_red",
            index_style="italic cyan",
            alternating_rows=True,
            alternating_row_colors=("", "on grey11"),
            table_style="dim",
            title="📈 Complete Styling Demo",
            border_style="blue",
            bg_kwargs={"axis": 0, "low": 0.3, "high": 0.9},
            tg_kwargs={"axis": 1},
        )
    )

    console.print("\n[yellow]High Contrast Theme:[/yellow]")
    console.print(
        df.head(4).pirr.to_rich(
            bg="coolwarm",
            column_header_style="bold black on bright_white",
            index_header_style="bold white on bright_black",
            table_style="bold",
            title="⚡ High Contrast Report",
            border_style="bright_yellow",
            minimize_gaps=False,
        )
    )


def demo_pandas_styler_integration(df, console):
    """Demonstrate integration with existing pandas styler objects."""
    console.print("\n[bold blue]═══ PANDAS STYLER INTEGRATION ═══[/bold blue]")

    console.print(
        "\n[yellow]Traditional Pandas Styler + to_rich enhancements:[/yellow]"
    )
    styled_df = df.head(4).style.highlight_max(axis=0, color="lightblue")
    console.print(
        df.head(4).pirr.to_rich(
            styler=styled_df, column_header_style="bold green", alternating_rows=True
        )
    )

    console.print("\n[yellow]Built-in styling overrides pandas styler:[/yellow]")
    styled_df2 = df.head(4).style.background_gradient(cmap="Reds")
    console.print(
        df.head(4).pirr.to_rich(
            styler=styled_df2,
            bg="Blues",  # This will override the Reds from styler
            title="🎨 Style Override Demo",
        )
    )


def main():
    """Run all demonstrations."""
    console = Console()
    df, series = create_sample_data()

    console.print(
        "[bold green]🎨 PIRRTOOLS TO_RICH COMPREHENSIVE EXAMPLES[/bold green]"
    )
    console.print("[dim]Showcasing all styling variations and combinations[/dim]")

    # Run all demonstrations
    demo_basic_usage(df, series, console)
    demo_background_gradients(df, console)
    demo_text_gradients(df, console)
    demo_header_styling(df, series, console)
    demo_index_styling(df, console)
    demo_alternating_rows(df, console)
    demo_table_wide_styling(df, console)
    demo_pandas_styler_integration(df, console)
    demo_complex_combinations(df, console)

    console.print("\n[bold green]✨ Demo Complete! ✨[/bold green]")
    console.print("[dim]All to_rich styling options demonstrated above.[/dim]")


if __name__ == "__main__":
    main()
