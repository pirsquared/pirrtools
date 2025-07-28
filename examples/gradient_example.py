import numpy as np
import pandas as pd
from rich.console import Console

import pirrtools


def main():
    """Example of DataFrame with background gradient styling converted to Rich table."""

    # Create sample DataFrame with numerical data suitable for gradient styling
    np.random.seed(42)
    data = {
        "Product": ["Widget A", "Widget B", "Widget C", "Widget D", "Widget E"],
        "Q1_Sales": np.random.randint(50, 200, 5),
        "Q2_Sales": np.random.randint(40, 220, 5),
        "Q3_Sales": np.random.randint(60, 180, 5),
        "Q4_Sales": np.random.randint(45, 210, 5),
    }

    df = pd.DataFrame(data)
    df["Total_Sales"] = df[["Q1_Sales", "Q2_Sales", "Q3_Sales", "Q4_Sales"]].sum(axis=1)

    print("Original DataFrame:")
    print(df)
    print()

    # Apply background gradient styling
    styled_df = df.style.background_gradient(
        subset=["Q1_Sales", "Q2_Sales", "Q3_Sales", "Q4_Sales", "Total_Sales"],
        cmap="RdYlGn",  # Red-Yellow-Green colormap
        axis=0,  # Apply gradient across rows for each column
    )

    print("DataFrame with background gradient styling applied (pandas Styler):")
    print()

    # Convert to Rich table using to_rich with the styler
    console = Console()
    print("Rich table with background gradient colors:")
    rich_table = df.pirr.to_rich(styler=styled_df, title="Sales Data with Gradient")
    console.print(rich_table)
    print()

    # Example without gradient styling for comparison
    print("Rich table without styling:")
    basic_table = df.pirr.to_rich(title="Basic Sales Data")
    console.print(basic_table)


if __name__ == "__main__":
    main()
