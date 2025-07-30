"""
Sphinx directive for executing code and embedding Rich table examples in documentation.
"""

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives import flag, unchanged
from sphinx.util.docutils import SphinxDirective
from pathlib import Path
import os
import io
import traceback
import sys


class RichTableDirective(SphinxDirective):
    """
    Directive to execute a code block and embed Rich table HTML output in documentation.
    
    Usage:
        .. rich-table::
           :width: 800px
           :height: 400px
           :class: my-class

           import pandas as pd
           import pirrtools
           from rich.console import Console
           
           # Create sample data
           df = pd.DataFrame({
               'Sales': [150, 230, 180],
               'Profit': [25, 45, 32]
           })
           
           # Convert to Rich table
           console = Console()
           table = df.pirr.to_rich(title="Sales Report")
           console.print(table)
    """
    
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        'width': unchanged,
        'height': unchanged,
        'class': unchanged,
        'show-code': flag,  # Option to show/hide code block
    }

    def run(self):
        from sphinx.util import logging
        logger = logging.getLogger(__name__)
        
        # Get the code content
        code = '\n'.join(self.content)
        
        # Get options
        width = self.options.get('width', '100%')
        height = self.options.get('height', 'auto')
        css_class = self.options.get('class', 'rich-table-example')
        show_code = 'show-code' in self.options
        
        # Container styling - preserve whitespace and prevent text wrapping
        container_style = f"width: {width}; height: {height}; overflow: auto; border: 1px solid #ddd; padding: 10px; margin: 10px 0; background: #fafafa;"
        
        # Execute the code and capture Rich output
        exec_globals = {}
        html_output = None
        error_html = None
        
        try:
            # Import necessary modules
            import rich.console
            import rich.table
            import pandas as pd
            import pirrtools
            
            # Create a console that records output
            recording_console = rich.console.Console(record=True, width=80)
            
            # Set up execution environment - intercept all Rich imports
            exec_globals.update({
                'pd': pd,
                'pirrtools': pirrtools,
                'console': recording_console,  # Provide pre-made console
                'recording_console': recording_console,  # Also make available directly
                '__builtins__': __builtins__,
            })
            
            # Mock the rich module entirely to ensure all imports use our console
            import types
            rich_mock = types.ModuleType('rich')
            console_mock = types.ModuleType('rich.console')
            console_mock.Console = lambda *args, **kwargs: recording_console
            rich_mock.console = console_mock
            
            table_mock = types.ModuleType('rich.table')
            table_mock.Table = rich.table.Table
            rich_mock.table = table_mock
            
            exec_globals['rich'] = rich_mock
            exec_globals['Console'] = lambda *args, **kwargs: recording_console
            exec_globals['Table'] = rich.table.Table
            
            # Execute the code, but patch any console assignments
            # Replace "console = Console()" with "console = recording_console"
            patched_code = code.replace('console = Console()', 'console = recording_console')
            patched_code = patched_code.replace('Console()', 'recording_console')
            
            exec(patched_code, exec_globals)
            
            # Export the Rich output to HTML  
            html_output = recording_console.export_html(inline_styles=True)
            
            # Extract just the body content from the HTML
            if '<body>' in html_output and '</body>' in html_output:
                start = html_output.find('<body>') + len('<body>')
                end = html_output.find('</body>')
                html_output = html_output[start:end].strip()
            
            # If no content was captured, there might be an execution issue
            if len(html_output) < 200:  # Empty or very short output suggests nothing was printed
                logger.warning(f"Short HTML output captured ({len(html_output)} chars), console may not have recorded output")
            
        except Exception as e:
            tb = traceback.format_exc()
            logger.warning(f"RichTableDirective execution failed: {e}\n{tb}")
            error_html = f'''
            <pre style="color: red; background: #fff5f5; padding: 10px; border: 1px solid #red;">
Error executing code:
{e}

{tb}
            </pre>
            '''
        
        # Create the nodes to return
        nodes_list = []
        
        # Always add the code block first
        code_block = nodes.literal_block(code, code)
        code_block['language'] = 'python'
        nodes_list.append(code_block)
        
        # Add the Rich output or error
        if html_output:
            # Add CSS to ensure proper formatting of Rich tables
            html_code = f'''
            <div class="{css_class}" style="{container_style}">
                <style>
                .{css_class} pre {{
                    white-space: pre !important;
                    overflow-x: auto !important;
                    font-family: 'Courier New', Consolas, Monaco, monospace !important;
                    line-height: 1.2 !important;
                    margin: 0 !important;
                    padding: 0 !important;
                }}
                .{css_class} code {{
                    white-space: pre !important;
                    font-family: inherit !important;
                    background: transparent !important;
                    padding: 0 !important;
                    border: none !important;
                }}
                </style>
                {html_output}
            </div>
            '''
        else:
            html_code = f'''
            <div class="{css_class}" style="{container_style}">
                {error_html or "<pre>Unknown error occurred</pre>"}
            </div>
            '''
        
        # Create HTML node for the output
        html_node = nodes.raw('', html_code, format='html')
        nodes_list.append(html_node)
        
        return nodes_list


def setup(app):
    """Register the directive with Sphinx."""
    app.add_directive('rich-table', RichTableDirective)
    
    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }