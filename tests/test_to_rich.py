"""
Comprehensive tests for the to_rich method and supporting Rich table functionality.

This module tests the enhanced to_rich method with all styling options,
utility functions, and edge cases.
"""

import numpy as np
import pandas as pd
import pytest
from rich.console import Console
from rich.table import Table

from pirrtools.pandas import (
    _create_index_gradient_styles,
    _css_to_rich_text,
    _format_index_value,
    _format_multiindex_value,
    _get_index_header_name,
    _measure_column_widths,
    _parse_css_color,
)


class TestToRichBasic:
    """Test basic to_rich functionality."""

    def test_simple_dataframe_to_rich(self):
        """Test basic DataFrame conversion to Rich table."""
        df = pd.DataFrame({"A": [1, 2, 3], "B": ["x", "y", "z"]})

        table = df.pirr.to_rich()

        assert isinstance(table, Table)
        assert table.title is None
        # Verify it doesn't raise an exception

    def test_simple_series_to_rich(self):
        """Test basic Series conversion to Rich table."""
        series = pd.Series([1, 2, 3], name="TestSeries")

        table = series.pirr.to_rich()

        assert isinstance(table, Table)
        assert table.title is None

    def test_dataframe_with_title(self):
        """Test DataFrame with custom title."""
        df = pd.DataFrame({"A": [1, 2]})

        table = df.pirr.to_rich(title="Test Table")

        assert table.title == "Test Table"

    def test_hide_index(self):
        """Test hiding the index column."""
        df = pd.DataFrame({"A": [1, 2]}, index=["row1", "row2"])

        table = df.pirr.to_rich(show_index=False)

        # Should have 1 column (just 'A'), not 2 (Index + A)
        assert len(table.columns) == 1

    def test_multiindex_dataframe(self):
        """Test DataFrame with MultiIndex."""
        arrays = [["A", "A", "B", "B"], ["one", "two", "one", "two"]]
        index = pd.MultiIndex.from_arrays(arrays, names=["first", "second"])
        df = pd.DataFrame({"values": [1, 2, 3, 4]}, index=index)

        table = df.pirr.to_rich()

        assert isinstance(table, Table)
        # Should not raise an exception with MultiIndex

    def test_multiindex_series(self):
        """Test Series with MultiIndex."""
        arrays = [["A", "A", "B", "B"], ["one", "two", "one", "two"]]
        index = pd.MultiIndex.from_arrays(arrays, names=["first", "second"])
        series = pd.Series([1, 2, 3, 4], index=index, name="values")

        table = series.pirr.to_rich()

        assert isinstance(table, Table)


class TestToRichStyling:
    """Test to_rich styling parameters."""

    def test_background_gradient_basic(self):
        """Test basic background gradient."""
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

        table = df.pirr.to_rich(bg="viridis")

        assert isinstance(table, Table)

    def test_background_gradient_with_kwargs(self):
        """Test background gradient with additional arguments."""
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

        table = df.pirr.to_rich(bg="plasma", bg_kwargs={"axis": 0, "subset": ["A"]})

        assert isinstance(table, Table)

    def test_text_gradient(self):
        """Test text gradient styling."""
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

        table = df.pirr.to_rich(tg="inferno")

        assert isinstance(table, Table)

    def test_combined_gradients(self):
        """Test combining background and text gradients."""
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

        table = df.pirr.to_rich(bg="viridis", tg="plasma")

        assert isinstance(table, Table)

    def test_index_background_gradient(self):
        """Test index background gradient."""
        df = pd.DataFrame(
            {"A": [1, 2, 3], "B": [4, 5, 6]}, index=["row1", "row2", "row3"]
        )

        table = df.pirr.to_rich(index_bg="coolwarm")

        assert isinstance(table, Table)

    def test_index_background_gradient_series(self):
        """Test index background gradient with Series."""
        series = pd.Series([1, 2, 3], index=["a", "b", "c"], name="values")

        table = series.pirr.to_rich(index_bg="plasma")

        assert isinstance(table, Table)

    def test_alternating_rows(self):
        """Test alternating row colors."""
        df = pd.DataFrame({"A": [1, 2, 3, 4], "B": [4, 5, 6, 7]})

        table = df.pirr.to_rich(alternating_rows=True)

        assert isinstance(table, Table)

    def test_alternating_rows_custom_colors(self):
        """Test alternating rows with custom colors."""
        df = pd.DataFrame({"A": [1, 2, 3, 4], "B": [4, 5, 6, 7]})

        table = df.pirr.to_rich(
            alternating_rows=True, alternating_row_colors=("", "on blue")
        )

        assert isinstance(table, Table)

    def test_header_styling(self):
        """Test column and index header styling."""
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})

        table = df.pirr.to_rich(
            column_header_style="bold blue",
            index_header_style="bold red",
            index_style="italic green",
        )

        assert isinstance(table, Table)

    def test_table_styling_options(self):
        """Test table-wide styling options."""
        df = pd.DataFrame({"A": [1, 2]})

        table = df.pirr.to_rich(
            table_style="bold", border_style="red", minimize_gaps=True
        )

        assert isinstance(table, Table)


class TestToRichWithPandasStyler:
    """Test to_rich integration with pandas Styler objects."""

    def test_existing_styler_integration(self):
        """Test using existing pandas Styler object."""
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

        # Create pandas styler
        styled = df.style.highlight_max()

        table = df.pirr.to_rich(styler=styled)

        assert isinstance(table, Table)

    def test_styler_with_built_in_options(self):
        """Test pandas styler combined with built-in styling."""
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

        styled = df.style.highlight_max()

        table = df.pirr.to_rich(styler=styled, alternating_rows=True, index_bg="plasma")

        assert isinstance(table, Table)

    def test_series_with_styler(self):
        """Test Series with pandas styler."""
        series = pd.Series([1, 2, 3], name="values")

        # Series styler (converted to DataFrame internally)
        table = series.pirr.to_rich(bg="viridis")

        assert isinstance(table, Table)


class TestToRichEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_dataframe(self):
        """Test with empty DataFrame."""
        df = pd.DataFrame()

        table = df.pirr.to_rich()

        assert isinstance(table, Table)

    def test_single_row_dataframe(self):
        """Test with single-row DataFrame."""
        df = pd.DataFrame({"A": [1], "B": [2]})

        table = df.pirr.to_rich(bg="viridis", index_bg="plasma")

        assert isinstance(table, Table)

    def test_single_column_dataframe(self):
        """Test with single-column DataFrame."""
        df = pd.DataFrame({"A": [1, 2, 3]})

        table = df.pirr.to_rich(bg="viridis")

        assert isinstance(table, Table)

    def test_dataframe_with_nan_values(self):
        """Test DataFrame with NaN values."""
        df = pd.DataFrame({"A": [1, np.nan, 3], "B": [np.nan, 2, 3]})

        table = df.pirr.to_rich(bg="viridis")

        assert isinstance(table, Table)

    def test_dataframe_mixed_dtypes(self):
        """Test DataFrame with mixed data types."""
        df = pd.DataFrame(
            {
                "ints": [1, 2, 3],
                "floats": [1.1, 2.2, 3.3],
                "strings": ["a", "b", "c"],
                "bools": [True, False, True],
                "dates": pd.date_range("2021-01-01", periods=3),
            }
        )

        table = df.pirr.to_rich(bg="viridis")

        assert isinstance(table, Table)

    def test_invalid_colormap_graceful_fallback(self):
        """Test graceful fallback with invalid colormap."""
        df = pd.DataFrame({"A": [1, 2, 3]})

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            table = df.pirr.to_rich(bg="nonexistent_colormap")
        assert isinstance(table, Table)

    def test_large_dataframe_performance(self):
        """Test with larger DataFrame for performance."""
        # Create a moderately large DataFrame
        df = pd.DataFrame({f"col_{i}": np.random.randn(100) for i in range(5)})

        table = df.pirr.to_rich(bg="viridis")

        assert isinstance(table, Table)


class TestUtilityFunctions:
    """Test supporting utility functions."""

    def test_parse_css_color(self):
        """Test CSS color parsing function."""
        # Test hex colors
        assert _parse_css_color("#ff0000") == "#ff0000"

        # Test RGB colors
        assert _parse_css_color("rgb(255, 0, 0)") == "rgb(255, 0, 0)"

        # Test named colors
        assert _parse_css_color("red") == "red"

    def test_format_index_value(self):
        """Test index value formatting."""
        # Test basic values
        assert _format_index_value("test") == "test"
        assert _format_index_value(123) == "123"

        # Test datetime
        dt = pd.Timestamp("2021-01-01")
        formatted = _format_index_value(dt)
        assert isinstance(formatted, str)

    def test_format_multiindex_value(self):
        """Test MultiIndex value formatting."""
        # Test tuple formatting
        result = _format_multiindex_value(("A", "one"))
        assert isinstance(result, str)
        assert "A" in result and "one" in result

    def test_get_index_header_name(self):
        """Test index header name generation."""
        # Test simple index
        index = pd.Index([1, 2, 3], name="TestIndex")
        assert _get_index_header_name(index) == "TestIndex"

        # Test unnamed index
        index = pd.Index([1, 2, 3])
        assert _get_index_header_name(index) == "Index"

        # Test MultiIndex
        arrays = [["A", "B"], ["one", "two"]]
        multi_index = pd.MultiIndex.from_arrays(arrays, names=["first", "second"])
        result = _get_index_header_name(multi_index)
        assert isinstance(result, str)

    def test_create_index_gradient_styles(self):
        """Test index gradient style creation."""
        index_values = ["A", "B", "C"]

        styles = _create_index_gradient_styles(index_values, "viridis")

        assert len(styles) == 3
        assert all(style.startswith("on #") for style in styles)

    def test_create_index_gradient_styles_empty(self):
        """Test index gradient styles with empty input."""
        styles = _create_index_gradient_styles([], "viridis")

        assert styles == []

    def test_create_index_gradient_styles_single_value(self):
        """Test index gradient styles with single value."""
        styles = _create_index_gradient_styles(["A"], "viridis")

        assert len(styles) == 1
        assert styles[0].startswith("on #")

    def test_create_index_gradient_styles_invalid_colormap(self):
        """Test index gradient styles with invalid colormap."""
        index_values = ["A", "B", "C"]

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            styles = _create_index_gradient_styles(index_values, "invalid_colormap")
        assert len(styles) == 3
        assert all(style == "" for style in styles)

    def test_measure_column_widths(self):
        """Test column width measurement."""
        df = pd.DataFrame({"Short": [1, 2], "VeryLongColumnName": [1, 2]})

        widths = _measure_column_widths(df)

        assert isinstance(widths, dict)
        assert "Short" in widths
        assert "VeryLongColumnName" in widths

    def test_css_to_rich_text_basic(self):
        """Test basic CSS to Rich text conversion."""
        css_styles = [("color", "red")]

        result = _css_to_rich_text(css_styles, "test", None)

        # Should return styled text
        assert result is not None

    def test_css_to_rich_text_with_background(self):
        """Test CSS to Rich text conversion with background."""
        css_styles = [("background-color", "#ff0000"), ("color", "white")]

        result = _css_to_rich_text(css_styles, "test", 10)

        assert result is not None


class TestIntegrationScenarios:
    """Test real-world integration scenarios."""

    def test_financial_data_styling(self):
        """Test styling financial data with all features."""
        # Create realistic financial data
        df = pd.DataFrame(
            {
                "Stock": ["AAPL", "GOOGL", "MSFT", "AMZN"],
                "Price": [150.25, 2800.50, 300.75, 3200.00],
                "Change": [2.5, -50.25, 5.0, 15.75],
                "Volume": [1000000, 500000, 750000, 600000],
            }
        )

        table = df.pirr.to_rich(
            bg="RdYlGn",
            bg_kwargs={"subset": ["Change"]},
            index_bg="plasma",
            alternating_rows=True,
            column_header_style="bold white on blue",
            title="📈 Stock Market Data",
        )

        assert isinstance(table, Table)
        assert table.title == "📈 Stock Market Data"

    def test_scientific_data_styling(self):
        """Test styling scientific data."""
        # Create scientific measurement data
        df = pd.DataFrame(
            {
                "Experiment": ["A", "B", "C", "D"],
                "Temperature": [25.5, 30.2, 22.8, 28.1],
                "Pressure": [1.013, 1.025, 0.998, 1.042],
                "Result": ["Pass", "Fail", "Pass", "Pass"],
            }
        )

        table = df.pirr.to_rich(
            bg="viridis",
            bg_kwargs={"subset": ["Temperature", "Pressure"]},
            tg="plasma",
            tg_kwargs={"subset": ["Result"]},
            title="🔬 Experiment Results",
        )

        assert isinstance(table, Table)

    def test_time_series_styling(self):
        """Test styling time series data."""
        dates = pd.date_range("2023-01-01", periods=5, freq="D")
        series = pd.Series([100, 105, 98, 110, 115], index=dates, name="Value")

        table = series.pirr.to_rich(
            index_bg="coolwarm",
            column_header_style="bold green",
            title="📊 Time Series Data",
        )

        assert isinstance(table, Table)


class TestConsoleIntegration:
    """Test integration with Rich Console."""

    def test_console_parameter(self):
        """Test providing custom Console object."""
        df = pd.DataFrame({"A": [1, 2, 3]})
        console = Console()

        table = df.pirr.to_rich(console=console)

        assert isinstance(table, Table)

    def test_console_rendering(self):
        """Test that table can be rendered by Console."""
        df = pd.DataFrame({"A": [1, 2, 3]})
        console = Console()

        table = df.pirr.to_rich(bg="viridis")

        # Should not raise an exception when rendering
        try:
            console.print(table)
        except Exception as e:
            pytest.fail(f"Console rendering failed: {e}")


@pytest.mark.parametrize(
    "colormap",
    [
        "viridis",
        "plasma",
        "inferno",
        "magma",
        "cividis",
        "coolwarm",
        "RdYlBu",
        "RdYlGn",
        "spectral",
    ],
)
def test_colormap_compatibility(colormap):
    """Test compatibility with various colormaps."""
    import warnings

    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        table = df.pirr.to_rich(bg=colormap, index_bg=colormap)
    assert isinstance(table, Table)


@pytest.mark.parametrize(
    "data_type",
    [
        [1, 2, 3],  # integers
        [1.1, 2.2, 3.3],  # floats
        ["a", "b", "c"],  # strings
        [True, False, True],  # booleans
    ],
)
def test_data_type_compatibility(data_type):
    """Test compatibility with various data types."""
    df = pd.DataFrame({"A": data_type})

    table = df.pirr.to_rich(bg="viridis")

    assert isinstance(table, Table)
