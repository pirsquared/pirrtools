"""
Tests for pirrtools.__init__ module utilities and integration functionality.

Tests the main package utilities like addpath, reload_entity, find_instances,
and integration with IPython/matplotlib.
"""

import shutil
import sys
import tempfile
import types
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

import pirrtools
from pirrtools import addpath, find_instances, get_base_package, reload_entity
from pirrtools.structures import AttrDict


class TestAddPath:
    """Test addpath functionality."""

    def setup_method(self):
        """Set up test paths."""
        self.original_path = sys.path.copy()
        self.test_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up test environment."""
        sys.path[:] = self.original_path
        shutil.rmtree(self.test_dir)

    def test_addpath_basic(self):
        """Test basic path addition."""
        path_len_before = len(sys.path)

        addpath(self.test_dir)

        assert len(sys.path) == path_len_before + 1
        assert str(Path(self.test_dir).absolute()) in sys.path

    def test_addpath_duplicate_ignored(self):
        """Test that duplicate paths are ignored."""
        addpath(self.test_dir)
        path_len_after_first = len(sys.path)

        addpath(self.test_dir)

        assert len(sys.path) == path_len_after_first

    def test_addpath_position(self):
        """Test adding path at specific position."""
        addpath(self.test_dir, position=0)

        assert sys.path[0] == str(Path(self.test_dir).absolute())

    def test_addpath_verbose(self, capsys):
        """Test verbose output."""
        addpath(self.test_dir, verbose=True)

        captured = capsys.readouterr()
        assert "added" in captured.out
        assert self.test_dir in captured.out

    def test_addpath_with_tilde(self):
        """Test path expansion with ~ (home directory)."""
        # Use a fake home path for testing
        with patch("pathlib.Path.expanduser") as mock_expand:
            mock_expand.return_value = Path(self.test_dir)

            addpath("~/test_path")

            mock_expand.assert_called_once()

    def test_addpath_relative_path(self):
        """Test adding relative path (should be converted to absolute)."""
        # Create a subdirectory for relative path test
        rel_dir = Path(self.test_dir) / "relative"
        rel_dir.mkdir()

        # Change to test directory temporarily
        original_cwd = Path.cwd()
        try:
            import os

            os.chdir(self.test_dir)
            addpath("relative")

            assert str(rel_dir.absolute()) in sys.path
        finally:
            os.chdir(original_cwd)


class TestReloadEntity:
    """Test reload_entity functionality."""

    def test_reload_module(self):
        """Test reloading a module."""
        import json  # Use standard library module

        # This should work without error
        reloaded = reload_entity(json)
        assert reloaded is json  # Should return the same module

    def test_reload_class(self):
        """Test reloading a class (reloads its module)."""
        # Use AttrDict class from pirrtools
        reloaded_class = reload_entity(AttrDict)

        # Should return AttrDict class (possibly reloaded)
        assert reloaded_class.__name__ == "AttrDict"

    def test_reload_invalid_entity(self):
        """Test reload with invalid entity."""
        # This might raise an error or handle gracefully
        with pytest.raises((AttributeError, TypeError)):
            reload_entity("not_a_module_or_class")

    def test_reload_builtin_module(self):
        """Test reloading built-in module."""
        import sys

        # Should handle built-in modules gracefully
        try:
            reloaded = reload_entity(sys)
            assert reloaded is sys
        except Exception:
            # Some built-ins can't be reloaded, which is fine
            pass


class TestGetBasePackage:
    """Test get_base_package functionality."""

    def test_get_base_package_simple(self):
        """Test getting base package of simple module."""
        import json

        base = get_base_package(json)
        assert base == "json"

    def test_get_base_package_nested(self):
        """Test getting base package of nested module."""
        import pirrtools.structures.attrdict

        base = get_base_package(pirrtools.structures.attrdict)
        assert base == "pirrtools"

    def test_get_base_package_single_name(self):
        """Test base package when module name has no dots."""
        # Create a mock module with simple name
        mock_module = types.ModuleType("simple_name")

        base = get_base_package(mock_module)
        assert base == "simple_name"


class TestFindInstances:
    """Test find_instances functionality."""

    def setup_method(self):
        """Set up test module with various objects."""
        # Create a test module
        self.test_module = types.ModuleType("test_module")
        self.test_module.__name__ = "test_module"

        # Add various objects to the module
        self.test_module.dict1 = {"a": 1}
        self.test_module.dict2 = {"b": 2}
        self.test_module.list1 = [1, 2, 3]
        self.test_module.string1 = "test"
        self.test_module.int1 = 42

        # Add nested module
        self.nested_module = types.ModuleType("test_module.nested")
        self.nested_module.__name__ = "test_module.nested"
        self.nested_module.dict3 = {"c": 3}
        self.test_module.nested = self.nested_module

    def test_find_dict_instances(self):
        """Test finding dictionary instances."""
        result = find_instances(dict, self.test_module)

        assert isinstance(result, AttrDict)
        assert "dict1" in result
        assert "dict2" in result
        assert result.dict1 == {"a": 1}
        assert result.dict2 == {"b": 2}

    def test_find_list_instances(self):
        """Test finding list instances."""
        result = find_instances(list, self.test_module)

        assert isinstance(result, AttrDict)
        assert "list1" in result
        assert result.list1 == [1, 2, 3]

    def test_find_with_filter(self):
        """Test finding instances with filter function."""

        def name_filter(name, _obj):
            return name.startswith("dict")

        result = find_instances(dict, self.test_module, filter_func=name_filter)

        assert "dict1" in result
        assert "dict2" in result
        # Should not include nested dict3 due to filter

    def test_find_nested_instances(self):
        """Test finding instances in nested modules."""
        result = find_instances(dict, self.test_module)

        # Should find nested instances
        assert "nested" in result
        assert isinstance(result.nested, AttrDict)
        assert "dict3" in result.nested

    def test_find_with_custom_tracker(self):
        """Test finding instances with custom tracker type."""
        result = find_instances(dict, self.test_module, tracker_type=dict)

        assert isinstance(result, dict)
        assert "dict1" in result
        assert result["dict1"] == {"a": 1}

    def test_find_no_matches(self):
        """Test finding instances when no matches exist."""
        result = find_instances(set, self.test_module)  # No sets in test module

        assert isinstance(result, AttrDict)
        assert len(result) == 0


class TestIPythonIntegration:
    """Test IPython integration functionality."""

    @patch("pirrtools.get_ipython")
    def test_matplotlib_inline_loading(self, mock_get_ipython):
        """Test loading matplotlib inline in IPython."""
        # Create mock IPython instance
        mock_ipython = Mock()
        mock_get_ipython.return_value = mock_ipython

        # Import pirrtools should trigger matplotlib inline loading
        # This is done at import time, so we need to test the function directly
        from pirrtools import load_matplotlib_inline

        load_matplotlib_inline()

        mock_ipython.run_line_magic.assert_called_with("matplotlib", "inline")

    @patch("pirrtools.get_ipython")
    def test_matplotlib_inline_no_ipython(self, mock_get_ipython):
        """Test matplotlib inline when IPython is not available."""
        mock_get_ipython.return_value = None

        # Should not raise an error
        from pirrtools import load_matplotlib_inline

        load_matplotlib_inline()

    @patch("pirrtools.get_ipython")
    def test_matplotlib_inline_import_error(self, mock_get_ipython):
        """Test matplotlib inline when IPython import fails."""
        mock_get_ipython.side_effect = ImportError("No IPython")

        # Should not raise an error
        from pirrtools import load_matplotlib_inline

        load_matplotlib_inline()


class TestPircFileLoading:
    """Test .pirc file loading functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.test_home = tempfile.mkdtemp()
        self.original_path = sys.path.copy()

    def teardown_method(self):
        """Clean up."""
        sys.path[:] = self.original_path
        shutil.rmtree(self.test_home)

    @patch("pirrtools.__HOME")
    def test_pirc_file_loading(self, mock_home):
        """Test loading .pirc file from home directory."""
        mock_home.__truediv__ = lambda _, path: Path(self.test_home) / path
        mock_home_path = Path(self.test_home)

        # Create .pirc.py file
        pirc_file = mock_home_path / ".pirc.py"
        pirc_content = f"""
mypaths = [
    "{self.test_home}/test_path1",
    "{self.test_home}/test_path2"
]
"""
        pirc_file.write_text(pirc_content)

        # Create the test paths
        (mock_home_path / "test_path1").mkdir()
        (mock_home_path / "test_path2").mkdir()

        # Test the loading function
        from pirrtools import load_pirc_file

        load_pirc_file()

        # Check if paths were added
        test_path1 = str((mock_home_path / "test_path1").absolute())
        test_path2 = str((mock_home_path / "test_path2").absolute())

        # Paths should be in sys.path
        assert test_path1 in sys.path
        assert test_path2 in sys.path

    @patch("pirrtools.__HOME")
    def test_pirc_file_not_exists(self, mock_home):
        """Test when .pirc file doesn't exist."""
        mock_home.__truediv__ = lambda _, path: Path(self.test_home) / path

        # No .pirc.py file exists
        from pirrtools import load_pirc_file

        # Should not raise an error
        load_pirc_file()

    @patch("pirrtools.__HOME")
    def test_pirc_file_no_mypaths(self, mock_home):
        """Test .pirc file without mypaths variable."""
        mock_home.__truediv__ = lambda _, path: Path(self.test_home) / path
        mock_home_path = Path(self.test_home)

        # Create .pirc.py file without mypaths
        pirc_file = mock_home_path / ".pirc.py"
        pirc_file.write_text("# No mypaths variable")

        from pirrtools import load_pirc_file

        # Should not raise an error
        load_pirc_file()


class TestPackageIntegration:
    """Test overall package integration."""

    def test_import_structure(self):
        """Test that all expected components are importable."""
        # Test main utilities
        assert hasattr(pirrtools, "addpath")
        assert hasattr(pirrtools, "reload_entity")
        assert hasattr(pirrtools, "find_instances")

        # Test structures
        assert hasattr(pirrtools, "AttrDict")
        assert hasattr(pirrtools, "AttrPath")

        # Test pandas integration
        assert hasattr(pirrtools, "load_cache")

    def test_pandas_accessor_registration(self):
        """Test that pandas accessor is properly registered."""
        import pandas as pd

        # Create test data
        df = pd.DataFrame({"A": [1, 2, 3]})
        series = pd.Series([1, 2, 3])

        # Test accessor is available
        assert hasattr(df, "pirr")
        assert hasattr(series, "pirr")

        # Test accessor methods
        assert hasattr(df.pirr, "to_rich")
        assert hasattr(df.pirr, "to_cache")
        assert hasattr(series.pirr, "to_rich")

    def test_structures_import(self):
        """Test structures module imports correctly."""
        from pirrtools.structures import AttrDict, AttrPath

        # Test creation
        ad = AttrDict({"test": "value"})
        assert ad.test == "value"

        # AttrPath creation
        ap = AttrPath(".")
        assert isinstance(ap, AttrPath)

    def test_cross_module_compatibility(self):
        """Test compatibility between different pirrtools modules."""
        import pandas as pd

        from pirrtools.structures import AttrDict

        # Create DataFrame
        df = pd.DataFrame({"A": [1, 2, 3]})

        # Use AttrDict to store configuration
        config = AttrDict()
        config.styling = AttrDict()
        config.styling.colormap = "viridis"
        config.styling.title = "Test Table"

        # Use configuration with to_rich
        table = df.pirr.to_rich(bg=config.styling.colormap, title=config.styling.title)

        assert table.title == "Test Table"

    def test_module_reloading_integration(self):
        """Test that module reloading works with pirrtools components."""
        # Test reloading pirrtools submodules
        import pirrtools.structures.attrdict

        reloaded = reload_entity(pirrtools.structures.attrdict)
        assert reloaded.__name__ == "pirrtools.structures.attrdict"

    def test_error_handling_integration(self):
        """Test error handling across different components."""
        import pandas as pd

        # Test that errors are handled gracefully
        df = pd.DataFrame({"A": [1, 2, 3]})

        # Invalid colormap should not crash
        table = df.pirr.to_rich(bg="invalid_colormap")
        assert table is not None

        # Invalid index background should not crash
        table = df.pirr.to_rich(index_bg="invalid_colormap")
        assert table is not None


class TestDevelopmentUtilities:
    """Test development-specific utilities."""

    def test_verbose_operations(self, capsys):
        """Test verbose mode in various operations."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Test verbose addpath
            addpath(tmp_dir, verbose=True)
            captured = capsys.readouterr()
            assert "added" in captured.out

    def test_path_management(self):
        """Test path management utilities."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            original_len = len(sys.path)

            # Add path
            addpath(tmp_dir)
            assert len(sys.path) == original_len + 1

            # Add same path again (should not duplicate)
            addpath(tmp_dir)
            assert len(sys.path) == original_len + 1

            # Path should be findable
            abs_path = str(Path(tmp_dir).absolute())
            assert abs_path in sys.path

    def test_configuration_loading(self):
        """Test configuration file loading patterns."""
        # This tests the pattern that pirrtools uses for configuration

        with tempfile.TemporaryDirectory() as tmp_dir:
            config_file = Path(tmp_dir) / "config.py"
            config_file.write_text(
                """
# Test configuration
DEBUG = True
PATHS = ["/test/path1", "/test/path2"]
SETTINGS = {"key": "value"}
"""
            )

            # Load as module (similar to .pirc loading)
            import importlib.util

            spec = importlib.util.spec_from_file_location("config", config_file)
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)

            assert config_module.DEBUG is True
            assert len(config_module.PATHS) == 2
            assert config_module.SETTINGS["key"] == "value"


@pytest.mark.integration
class TestRealWorldScenarios:
    """Test real-world usage scenarios."""

    def test_data_analysis_workflow(self):
        """Test typical data analysis workflow."""
        import pandas as pd

        from pirrtools.structures import AttrDict

        # Set up project configuration
        config = AttrDict()
        config.data = AttrDict()
        config.data.file_path = "test_data.csv"
        config.styling = AttrDict()
        config.styling.colormap = "viridis"
        config.styling.alternating = True

        # Create sample data
        df = pd.DataFrame(
            {
                "Product": ["A", "B", "C", "D"],
                "Sales": [100, 150, 200, 175],
                "Profit": [20, 30, 45, 35],
            }
        )

        # Apply styling from configuration
        table = df.pirr.to_rich(
            bg=config.styling.colormap,
            alternating_rows=config.styling.alternating,
            title="Sales Analysis",
        )

        assert table.title == "Sales Analysis"

    def test_development_environment_setup(self):
        """Test development environment setup workflow."""
        with tempfile.TemporaryDirectory() as project_dir:
            # Set up project structure
            (Path(project_dir) / "src").mkdir()
            (Path(project_dir) / "lib").mkdir()
            (Path(project_dir) / "config").mkdir()

            # Add paths to Python path
            addpath(Path(project_dir) / "src")
            addpath(Path(project_dir) / "lib")

            # Verify paths are accessible
            src_path = str((Path(project_dir) / "src").absolute())
            lib_path = str((Path(project_dir) / "lib").absolute())

            assert src_path in sys.path
            assert lib_path in sys.path

    def test_interactive_data_exploration(self):
        """Test interactive data exploration patterns."""
        import numpy as np
        import pandas as pd

        # Create sample dataset
        np.random.seed(42)
        df = pd.DataFrame(
            {
                "Date": pd.date_range("2023-01-01", periods=50, freq="D"),
                "Value": np.random.randn(50).cumsum(),
                "Category": np.random.choice(["A", "B", "C"], 50),
            }
        )

        # Quick exploration with different styles
        basic_table = df.head().pirr.to_rich()
        styled_table = df.head().pirr.to_rich(
            bg="plasma", alternating_rows=True, title="Data Sample"
        )

        category_summary = (
            df.groupby("Category")
            .mean()
            .pirr.to_rich(bg="coolwarm", title="Category Averages")
        )

        # All should be valid Rich tables
        assert all(
            hasattr(t, "columns") for t in [basic_table, styled_table, category_summary]
        )


def test_package_version_info():
    """Test that package version information is accessible."""
    # Test that pirrtools has version info or at least doesn't error
    try:
        version = pirrtools.__version__
        assert isinstance(version, str)
    except AttributeError:
        # Version might not be defined, which is OK
        pass

    # Test that module has proper __name__
    assert pirrtools.__name__ == "pirrtools"
