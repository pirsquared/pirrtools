import numpy as np
import pandas as pd
from rich.console import Console

import pirrtools


def test_background_padding():
    """Test the enhanced background padding with varied text lengths."""

    # Create DataFrame with intentionally varied text lengths
    data = {
        "A": ["X", "YYYY", "ZZ"],
        "B": [1, 22, 333],
        "C": ["Short", "Very Long Text", "Med"],
    }

    df = pd.DataFrame(data)

    console = Console()

    print("Testing background padding with gradient styling:")
    print("=" * 60)

    # Apply gradient styling
    styled_df = df.style.background_gradient(cmap="Blues", axis=0)

    # Convert to Rich table - should now have proper padding
    rich_table = df.pirr.to_rich(styler=styled_df, title="With Enhanced Padding")
    console.print(rich_table)

    print("\nCompare with table without styling (no padding):")
    print("=" * 60)

    basic_table = df.pirr.to_rich(title="Without Styling")
    console.print(basic_table)


if __name__ == "__main__":
    test_background_padding()
