#!/usr/bin/env python3
"""
Interactive Tutor for pirrtools to_rich Method
=============================================

This script provides a step-by-step guided tutorial for using the `.pirr.to_rich()`
method with pandas DataFrames and Series. It demonstrates all styling options
and provides interactive examples.

Run this script to learn how to use pirrtools' Rich table styling features.
"""

import time

import numpy as np
import pandas as pd
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.rule import Rule
from rich.text import Text

import pirrtools


class ToRichTutor:
    """Interactive tutorial for the to_rich method."""

    def __init__(self):
        self.console = Console()
        self.sample_df = None
        self.sample_series = None
        self.create_sample_data()

    def create_sample_data(self):
        """Create sample DataFrame and Series for demonstrations."""
        np.random.seed(42)

        # Sample DataFrame with mixed data types
        self.sample_df = pd.DataFrame(
            {
                "Sales": [150, 230, 180, 340, 290, 410],
                "Profit": [25, 45, 32, 68, 55, 82],
                "Growth": [0.12, 0.18, 0.09, 0.25, 0.21, 0.31],
                "Region": ["North", "South", "East", "West", "North", "South"],
            },
            index=["Q1-2023", "Q2-2023", "Q3-2023", "Q4-2023", "Q1-2024", "Q2-2024"],
        )

        # Sample Series
        self.sample_series = pd.Series(
            [85, 92, 78, 96, 88, 94],
            index=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            name="Customer_Satisfaction",
        )

    def wait_for_user(self, message="Press Enter to continue..."):
        """Wait for user input before proceeding."""
        self.console.print(f"\n[dim]{message}[/dim]")
        input()

    def show_header(self, title, description):
        """Display a section header."""
        self.console.print(Rule(f"[bold blue]{title}[/bold blue]", style="blue"))
        if description:
            self.console.print(f"\n[dim]{description}[/dim]\n")

    def show_code_example(self, code, description=None):
        """Display a code example."""
        if description:
            self.console.print(f"[yellow]Example:[/yellow] {description}")

        # Format code with syntax highlighting
        code_panel = Panel(
            Text(code, style="green"),
            title="Code",
            title_align="left",
            border_style="green",
        )
        self.console.print(code_panel)

    def lesson_1_basic_usage(self):
        """Lesson 1: Basic to_rich usage."""
        self.show_header(
            "Lesson 1: Basic Usage",
            "Learn the fundamentals of converting pandas objects to Rich tables.",
        )

        # Show original data
        self.console.print("[bold]Sample DataFrame:[/bold]")
        self.console.print(self.sample_df)
        self.wait_for_user()

        # Basic conversion
        self.show_code_example(
            "df.pirr.to_rich()", "Convert DataFrame to Rich table with default styling"
        )

        basic_table = self.sample_df.pirr.to_rich()
        self.console.print(basic_table)
        self.wait_for_user()

        # With title
        self.show_code_example(
            'df.pirr.to_rich(title="Sales Report")', "Add a title to your table"
        )

        titled_table = self.sample_df.pirr.to_rich(title="Sales Report")
        self.console.print(titled_table)
        self.wait_for_user()

        # Hide index
        self.show_code_example(
            "df.pirr.to_rich(show_index=False)", "Hide the DataFrame index"
        )

        no_index_table = self.sample_df.pirr.to_rich(show_index=False)
        self.console.print(no_index_table)
        self.wait_for_user()

        # Series example
        self.console.print("\n[bold]Sample Series:[/bold]")
        self.console.print(self.sample_series)
        self.wait_for_user()

        self.show_code_example("series.pirr.to_rich()", "Convert Series to Rich table")

        series_table = self.sample_series.pirr.to_rich()
        self.console.print(series_table)
        self.wait_for_user()

    def lesson_2_background_gradients(self):
        """Lesson 2: Background gradient styling."""
        self.show_header(
            "Lesson 2: Background Gradients",
            "Add color gradients to table backgrounds for better data visualization.",
        )

        # Default gradient
        self.show_code_example(
            'df.pirr.to_rich(bg="gradient")', "Apply default background gradient"
        )

        gradient_table = self.sample_df.pirr.to_rich(bg="gradient")
        self.console.print(gradient_table)
        self.wait_for_user()

        # Different colormaps
        colormaps = ["viridis", "plasma", "coolwarm", "RdYlBu"]

        for cmap in colormaps:
            self.show_code_example(
                f'df.pirr.to_rich(bg="{cmap}")', f"Using {cmap} colormap"
            )

            cmap_table = self.sample_df.pirr.to_rich(bg=cmap)
            self.console.print(cmap_table)
            self.wait_for_user()

        # Gradient axis options
        self.show_code_example(
            'df.pirr.to_rich(bg="viridis", bg_kwargs={"axis": 0})',
            "Column-wise gradient (axis=0)",
        )

        col_gradient = self.sample_df.pirr.to_rich(bg="viridis", bg_kwargs={"axis": 0})
        self.console.print(col_gradient)
        self.wait_for_user()

        self.show_code_example(
            'df.pirr.to_rich(bg="viridis", bg_kwargs={"axis": 1})',
            "Row-wise gradient (axis=1)",
        )

        row_gradient = self.sample_df.pirr.to_rich(bg="viridis", bg_kwargs={"axis": 1})
        self.console.print(row_gradient)
        self.wait_for_user()

        # Subset styling
        self.show_code_example(
            'df.pirr.to_rich(bg="plasma", bg_kwargs={"subset": ["Sales", "Profit"]})',
            "Apply gradient to specific columns only",
        )

        subset_gradient = self.sample_df.pirr.to_rich(
            bg="plasma", bg_kwargs={"subset": ["Sales", "Profit"]}
        )
        self.console.print(subset_gradient)
        self.wait_for_user()

    def lesson_3_text_gradients(self):
        """Lesson 3: Text gradient styling."""
        self.show_header(
            "Lesson 3: Text Gradients",
            "Apply color gradients to text for enhanced readability and style.",
        )

        # Basic text gradient
        self.show_code_example(
            'df.pirr.to_rich(tg="gradient")', "Apply default text gradient"
        )

        text_gradient = self.sample_df.pirr.to_rich(tg="gradient")
        self.console.print(text_gradient)
        self.wait_for_user()

        # Different text gradients
        text_cmaps = ["inferno", "magma", "cividis"]

        for cmap in text_cmaps:
            self.show_code_example(
                f'df.pirr.to_rich(tg="{cmap}")', f"Text gradient with {cmap} colormap"
            )

            tg_table = self.sample_df.pirr.to_rich(tg=cmap)
            self.console.print(tg_table)
            self.wait_for_user()

        # Combined background and text gradients
        self.show_code_example(
            'df.pirr.to_rich(bg="viridis", tg="plasma")',
            "Combine background and text gradients",
        )

        combined_table = self.sample_df.pirr.to_rich(bg="viridis", tg="plasma")
        self.console.print(combined_table)
        self.wait_for_user()

    def lesson_4_header_styling(self):
        """Lesson 4: Header and index styling."""
        self.show_header(
            "Lesson 4: Header and Index Styling",
            "Customize the appearance of column headers and index labels.",
        )

        # Column header styling
        self.show_code_example(
            'df.pirr.to_rich(column_header_style="bold white on blue")',
            "Style column headers",
        )

        header_table = self.sample_df.pirr.to_rich(
            column_header_style="bold white on blue"
        )
        self.console.print(header_table)
        self.wait_for_user()

        # Index styling
        self.show_code_example(
            'df.pirr.to_rich(index_style="italic green", index_header_style="bold yellow on red")',
            "Style index values and header",
        )

        index_table = self.sample_df.pirr.to_rich(
            index_style="italic green", index_header_style="bold yellow on red"
        )
        self.console.print(index_table)
        self.wait_for_user()

        # Index background gradients
        self.show_code_example(
            'df.pirr.to_rich(index_bg="coolwarm")', "Apply background gradient to index"
        )

        index_bg_table = self.sample_df.pirr.to_rich(index_bg="coolwarm")
        self.console.print(index_bg_table)
        self.wait_for_user()

    def lesson_5_alternating_rows(self):
        """Lesson 5: Alternating row styling."""
        self.show_header(
            "Lesson 5: Alternating Rows",
            "Add alternating row colors for better readability.",
        )

        # Basic alternating rows
        self.show_code_example(
            "df.pirr.to_rich(alternating_rows=True)",
            "Enable default alternating row colors",
        )

        alt_table = self.sample_df.pirr.to_rich(alternating_rows=True)
        self.console.print(alt_table)
        self.wait_for_user()

        # Custom alternating colors
        self.show_code_example(
            'df.pirr.to_rich(alternating_rows=True, alternating_row_colors=("", "on dark_blue"))',
            "Custom alternating row colors",
        )

        custom_alt_table = self.sample_df.pirr.to_rich(
            alternating_rows=True, alternating_row_colors=("", "on dark_blue")
        )
        self.console.print(custom_alt_table)
        self.wait_for_user()

        # Alternating rows with gradient
        self.show_code_example(
            'df.pirr.to_rich(bg="gradient", alternating_rows=True, alternating_row_colors=("", "on grey15"))',
            "Combine gradients with alternating rows",
        )

        gradient_alt_table = self.sample_df.pirr.to_rich(
            bg="gradient",
            alternating_rows=True,
            alternating_row_colors=("", "on grey15"),
        )
        self.console.print(gradient_alt_table)
        self.wait_for_user()

    def lesson_6_advanced_combinations(self):
        """Lesson 6: Advanced styling combinations."""
        self.show_header(
            "Lesson 6: Advanced Combinations",
            "Combine multiple styling options for professional-looking tables.",
        )

        # Professional report style
        self.show_code_example(
            """df.pirr.to_rich(
    bg="viridis",
    column_header_style="bold white on dark_blue",
    index_header_style="bold yellow on dark_red",
    index_style="italic cyan",
    alternating_rows=True,
    alternating_row_colors=("", "on grey11"),
    title="📊 Quarterly Sales Report",
    border_style="blue"
)""",
            "Professional report styling",
        )

        professional_table = self.sample_df.pirr.to_rich(
            bg="viridis",
            column_header_style="bold white on dark_blue",
            index_header_style="bold yellow on dark_red",
            index_style="italic cyan",
            alternating_rows=True,
            alternating_row_colors=("", "on grey11"),
            title="📊 Quarterly Sales Report",
            border_style="blue",
        )
        self.console.print(professional_table)
        self.wait_for_user()

        # High contrast theme
        self.show_code_example(
            """df.pirr.to_rich(
    bg="coolwarm",
    column_header_style="bold black on bright_white",
    index_header_style="bold white on bright_black",
    table_style="bold",
    title="⚡ High Contrast Report",
    border_style="bright_yellow"
)""",
            "High contrast theme",
        )

        contrast_table = self.sample_df.pirr.to_rich(
            bg="coolwarm",
            column_header_style="bold black on bright_white",
            index_header_style="bold white on bright_black",
            table_style="bold",
            title="⚡ High Contrast Report",
            border_style="bright_yellow",
        )
        self.console.print(contrast_table)
        self.wait_for_user()

    def lesson_7_pandas_styler_integration(self):
        """Lesson 7: Integration with pandas Styler."""
        self.show_header(
            "Lesson 7: Pandas Styler Integration",
            "Use existing pandas Styler objects with to_rich enhancements.",
        )

        # Traditional pandas styler
        styled_df = self.sample_df.style.highlight_max(axis=0, color="lightblue")

        self.show_code_example(
            """styled_df = df.style.highlight_max(axis=0, color='lightblue')
df.pirr.to_rich(styler=styled_df, title="Pandas Styler + to_rich")""",
            "Using existing pandas Styler",
        )

        styler_table = self.sample_df.pirr.to_rich(
            styler=styled_df, title="Pandas Styler + to_rich"
        )
        self.console.print(styler_table)
        self.wait_for_user()

        # Override styler with built-in options
        styled_df2 = self.sample_df.style.background_gradient(cmap="Reds")

        self.show_code_example(
            """styled_df = df.style.background_gradient(cmap='Reds')
df.pirr.to_rich(styler=styled_df, bg="Blues", title="Style Override")""",
            "Built-in styling overrides pandas styler",
        )

        override_table = self.sample_df.pirr.to_rich(
            styler=styled_df2, bg="Blues", title="🎨 Style Override Demo"
        )
        self.console.print(override_table)
        self.wait_for_user()

    def show_summary(self):
        """Show tutorial summary and next steps."""
        self.show_header(
            "Tutorial Complete! 🎉",
            "You've learned all the key features of the to_rich method.",
        )

        summary_md = """
## What You've Learned

✅ **Basic Usage**: Converting DataFrames and Series to Rich tables  
✅ **Background Gradients**: Adding color gradients to table backgrounds  
✅ **Text Gradients**: Styling text with color gradients  
✅ **Header Styling**: Customizing column headers and index appearance  
✅ **Alternating Rows**: Improving readability with row alternation  
✅ **Advanced Combinations**: Creating professional-looking tables  
✅ **Pandas Integration**: Working with existing pandas Styler objects  

## Next Steps

1. **Practice**: Try these techniques with your own data
2. **Experiment**: Mix and match different styling options
3. **Explore**: Check out the example files in the `examples/` directory
4. **Reference**: Use the documentation for parameter details

## Quick Reference

```python
# Basic usage
df.pirr.to_rich()

# Background gradients
df.pirr.to_rich(bg="viridis")

# Text gradients  
df.pirr.to_rich(tg="plasma")

# Header styling
df.pirr.to_rich(column_header_style="bold blue")

# Alternating rows
df.pirr.to_rich(alternating_rows=True)

# Everything combined
df.pirr.to_rich(
    bg="viridis",
    tg="plasma", 
    column_header_style="bold white on blue",
    alternating_rows=True,
    title="My Report"
)
```

Happy styling! 🎨
        """

        self.console.print(Markdown(summary_md))

    def run_tutorial(self):
        """Run the complete interactive tutorial."""
        # Welcome message
        welcome_panel = Panel(
            Text.from_markup(
                "[bold blue]Welcome to the pirrtools to_rich Tutorial![/bold blue]\n\n"
                "This interactive guide will teach you how to create beautiful,\n"
                "styled tables from pandas DataFrames and Series using Rich.\n\n"
                "[dim]Press Enter to begin each lesson.[/dim]"
            ),
            title="🎓 Interactive Tutorial",
            border_style="blue",
        )
        self.console.print(welcome_panel)
        self.wait_for_user()

        # Run lessons
        lessons = [
            self.lesson_1_basic_usage,
            self.lesson_2_background_gradients,
            self.lesson_3_text_gradients,
            self.lesson_4_header_styling,
            self.lesson_5_alternating_rows,
            self.lesson_6_advanced_combinations,
            self.lesson_7_pandas_styler_integration,
        ]

        for i, lesson in enumerate(lessons, 1):
            try:
                lesson()

                # Ask if user wants to continue
                if i < len(lessons):
                    continue_lesson = Confirm.ask(
                        f"\nReady for Lesson {i + 1}?", default=True
                    )
                    if not continue_lesson:
                        self.console.print(
                            "\n[yellow]Tutorial paused. Run again to continue![/yellow]"
                        )
                        return

                    self.console.clear()

            except KeyboardInterrupt:
                self.console.print(
                    "\n\n[yellow]Tutorial interrupted. Run again to continue![/yellow]"
                )
                return

        # Show summary
        self.show_summary()


def main():
    """Run the interactive tutorial."""
    tutor = ToRichTutor()
    tutor.run_tutorial()


if __name__ == "__main__":
    main()
