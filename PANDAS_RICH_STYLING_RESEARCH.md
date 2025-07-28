# Pandas Styler to Rich Table Styling Research

## Executive Summary

This research document provides a comprehensive analysis of how pandas Styler works internally, Rich Table styling capabilities, and methods for extracting CSS styles from pandas to map them to Rich formatting. The findings enable full integration between pandas styled DataFrames and Rich terminal tables.

## 1. Pandas Styler Internal Architecture

### How pandas Styler Works

The pandas `Styler` class uses a lazy evaluation system for styling:

1. **Queueing Phase**: When users apply styles via `.apply()`, `.map()`, `background_gradient()`, etc., pandas doesn't immediately calculate anything. Instead, it appends functions and arguments to a list called `self._todo`.

2. **Computation Phase**: When rendering is requested (typically via `.render()` or `.to_html()`), pandas walks through `self._todo` and executes each function via `self._compute()`.

3. **Context Building**: Style functions update an internal `defaultdict(list)` called `self.ctx` which maps DataFrame row/column positions to CSS attribute-value pairs.

4. **Translation Phase**: The `_translate()` method takes `self.ctx` and builds a dictionary ready for Jinja template rendering.

### Key Internal Methods and Attributes

- **`self._todo`**: List of queued styling functions and their arguments
- **`self.ctx`**: Dictionary mapping `(row, col)` positions to CSS property tuples
- **`_compute()`**: Executes queued style functions and populates `self.ctx`
- **`_translate()`**: Converts context to template-ready format
- **`to_html()`**: Final rendering using Jinja2 templates

### Context Dictionary Structure

The `self.ctx` dictionary maps cell positions to CSS properties:

```python
# Example structure
{
    (0, 0): [('background-color', '#46085c'), ('color', '#f1f1f1')],
    (0, 1): [('background-color', '#471365'), ('color', '#f1f1f1')],
    (1, 0): [('background-color', '#481b6d'), ('color', '#f1f1f1')]
}
```

## 2. CSS Style Extraction Methods

### Method 1: Direct Context Access (Recommended)

```python
# Apply styling to trigger context population
styled_df = df.style.background_gradient(cmap='viridis')

# Force computation of styles
styled_df._compute()

# Extract styles directly from context
for (row, col), css_tuples in styled_df.ctx.items():
    css_properties = dict(css_tuples)  # Convert to dict
    print(f"Cell ({row},{col}): {css_properties}")
```

### Method 2: HTML Parsing

```python
# Render to HTML and parse inline styles
html = styled_df.to_html()
import re

style_pattern = r'style="([^"]*)"'
styles = re.findall(style_pattern, html)
```

**Note**: Method 1 is preferred as it provides direct access to computed styles without HTML parsing overhead.

## 3. Pandas Styling Methods Research

### Background Gradient

- **Method**: `df.style.background_gradient()`
- **Parameters**: 
  - `cmap`: Colormap (default 'PuBu')
  - `axis`: Apply per column (0), row (1), or entire DataFrame (None)
  - `subset`: Select specific columns/rows
  - `vmin/vmax`: Value range for normalization
  - `text_color_threshold`: Auto text color adjustment
- **CSS Output**: `background-color` and `color` properties

### Text Gradient

- **Method**: `df.style.text_gradient()`
- **Parameters**: Similar to `background_gradient`
- **CSS Output**: `color` property with gradient values

### Other Key Methods

- **`background_gradient()`**: Color backgrounds based on data values
- **`text_gradient()`**: Color text based on data values  
- **`highlight_max()`**: Highlight maximum values
- **`highlight_min()`**: highlight minimum values
- **`bar()`**: Add data bars to cells
- **`set_properties()`**: Apply CSS properties directly

## 4. Rich Table Styling Capabilities

### Column-Level Styling

Rich tables support comprehensive column styling:

```python
from rich.table import Table

table = Table(title="Styled Table")
table.add_column("Name", justify="left", style="bold magenta", no_wrap=True)
table.add_column("Score", justify="right", style="green") 
table.add_column("Status", justify="center", style="yellow")
```

**Column Style Options**:
- `style`: Text color and formatting
- `justify`: Text alignment ("left", "center", "right", "full")
- `vertical`: Vertical alignment ("top", "middle", "bottom")
- `no_wrap`: Prevent text wrapping
- `min_width`: Minimum column width
- `max_width`: Maximum column width

### Cell-Level Styling

Individual cells can have markup-based styling:

```python
# Cell with background color
table.add_row("[on blue]Diana[/]", "[on green]98[/]", "[on cyan]PASS[/]")

# Cell with text formatting
table.add_row("[bold]Alice[/]", "[italic]95[/]", "[dim]Notes[/]")
```

### Border and Table Styling

```python
from rich import box

# Various border styles
table = Table(box=box.ROUNDED)        # Rounded corners
table = Table(box=box.DOUBLE_EDGE)    # Double line border
table = Table(box=box.MINIMAL)        # Minimal border
table = Table(box=None)               # No border

# Show lines between rows
table = Table(show_lines=True)
```

## 5. Color Format Conversion

### Rich Color Support

Rich natively supports multiple color formats:

1. **Hex Colors**: `#RRGGBB` (e.g., `#ff6b6b`)
2. **RGB Colors**: `rgb(r,g,b)` (e.g., `rgb(255,107,107)`)
3. **Named Colors**: `red`, `blue`, `green`, etc.
4. **Background Colors**: `on color` syntax (e.g., `on red`, `on #ff6b6b`)

### Direct CSS to Rich Conversion

**No conversion needed!** Rich directly supports CSS hex and RGB formats:

```python
# These work directly in Rich
console.print("Text", style="#ff6b6b")         # CSS hex
console.print("Text", style="rgb(255,107,107)") # CSS RGB
console.print("Text", style="red on white")     # Background
```

### Programmatic Conversion (if needed)

```python
def css_color_to_rich(css_color: str) -> str:
    """Convert CSS color to Rich format."""
    if css_color.startswith('#'):
        return css_color  # Hex colors work directly
    
    # Parse RGB format
    import re
    rgb_match = re.match(r'rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', css_color)
    if rgb_match:
        r, g, b = rgb_match.groups()
        return f"rgb({r},{g},{b})"
    
    return css_color  # Named colors work directly
```

## 6. Integration Implementation

### Complete pandas to Rich Converter

```python
def pandas_to_rich_table(df: pd.DataFrame, styled_df=None) -> Table:
    """Convert pandas DataFrame with styling to Rich Table."""
    
    table = Table(title="Styled DataFrame")
    
    # Add columns
    for col in df.columns:
        table.add_column(str(col), justify="right")
    
    # If styled DataFrame provided, extract styles
    if styled_df:
        styled_df._compute()  # Force style computation
        
        # Add rows with styling
        for row_idx, row in df.iterrows():
            rich_row = []
            for col_idx, (col, value) in enumerate(row.items()):
                cell_styles = styled_df.ctx.get((row_idx, col_idx), [])
                formatted_value = str(value)
                
                if cell_styles:
                    css_props = dict(cell_styles)
                    if 'background-color' in css_props:
                        bg_color = css_props['background-color']
                        formatted_value = f"[on {bg_color[1:]}]{formatted_value}[/]"
                
                rich_row.append(formatted_value)
            
            table.add_row(*rich_row)
    else:
        # Add rows without styling
        for _, row in df.iterrows():
            table.add_row(*[str(val) for val in row])
    
    return table
```

## 7. Key Research Findings

1. **pandas Styler Architecture**: Uses lazy evaluation with `_todo` queue and `ctx` context dictionary mapping cell positions to CSS properties.

2. **CSS Extraction**: Direct access via `styled_df._compute()` then `styled_df.ctx` is the most efficient method.

3. **Rich Color Compatibility**: Rich natively supports CSS hex colors (`#RRGGBB`) and RGB format (`rgb(r,g,b)`), eliminating need for complex color conversion.

4. **Rich Styling Capabilities**: 
   - Column-level styling with comprehensive options
   - Cell-level markup-based formatting
   - Background colors via `on color` syntax
   - Multiple border and table styles

5. **Integration Feasibility**: Full integration is possible through:
   - Extracting pandas CSS styles from `ctx` dictionary
   - Converting CSS `background-color` to Rich `on color` syntax
   - Mapping cell positions between pandas and Rich table structures

6. **Performance Considerations**: Direct context access is more efficient than HTML parsing for style extraction.

## 8. Recommended Implementation Approach

1. **Style Extraction**: Use `styled_df._compute()` + `styled_df.ctx` for direct access
2. **Color Handling**: Use CSS hex colors directly in Rich (no conversion needed)
3. **Cell Mapping**: Map pandas `(row, col)` positions to Rich table cells
4. **Background Colors**: Convert CSS `background-color: #rrggbb` to Rich `[on rrggbb]text[/]`
5. **Text Colors**: Convert CSS `color: #rrggbb` to Rich `[#rrggbb]text[/]`

This research provides the foundation for implementing a robust pandas Styler to Rich Table conversion system with full styling preservation.