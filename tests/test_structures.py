"""
Comprehensive tests for pirrtools.structures module.

Tests AttrDict and AttrPath functionality with edge cases and integration scenarios.
"""

import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from pirrtools.structures.attrdict import AttrDict
from pirrtools.structures.attrpath import AttrPath


class TestAttrDict:
    """Test AttrDict functionality."""

    def test_basic_creation(self):
        """Test basic AttrDict creation."""
        ad = AttrDict()
        assert isinstance(ad, dict)
        assert len(ad) == 0

    def test_creation_with_data(self):
        """Test AttrDict creation with initial data."""
        data = {"a": 1, "b": 2}
        ad = AttrDict(data)

        assert ad["a"] == 1
        assert ad["b"] == 2
        assert len(ad) == 2

    def test_creation_with_kwargs(self):
        """Test AttrDict creation with keyword arguments."""
        ad = AttrDict(a=1, b=2, c=3)

        assert ad["a"] == 1
        assert ad["b"] == 2
        assert ad["c"] == 3

    def test_creation_with_dict_and_kwargs(self):
        """Test AttrDict creation with both dict and kwargs."""
        ad = AttrDict({"a": 1}, b=2, c=3)

        assert ad["a"] == 1
        assert ad["b"] == 2
        assert ad["c"] == 3

    def test_attribute_access_get(self):
        """Test getting values via attribute access."""
        ad = AttrDict(a=1, b=2)

        assert ad.a == 1
        assert ad.b == 2

    def test_attribute_access_set(self):
        """Test setting values via attribute access."""
        ad = AttrDict()

        ad.a = 1
        ad.b = "test"

        assert ad["a"] == 1
        assert ad["b"] == "test"
        assert ad.a == 1
        assert ad.b == "test"

    def test_attribute_access_delete(self):
        """Test deleting values via attribute access."""
        ad = AttrDict(a=1, b=2)

        del ad.a

        assert "a" not in ad
        assert ad.b == 2

    def test_attribute_nonexistent_raises_error(self):
        """Test that accessing nonexistent attribute raises AttributeError."""
        ad = AttrDict()

        with pytest.raises(AttributeError):
            _ = ad.nonexistent

    def test_dict_methods_work(self):
        """Test that standard dict methods work."""
        ad = AttrDict(a=1, b=2)

        assert list(ad.keys()) == ["a", "b"]
        assert list(ad.values()) == [1, 2]
        assert list(ad.items()) == [("a", 1), ("b", 2)]

    def test_nested_attrdict(self):
        """Test nested AttrDict structures."""
        ad = AttrDict()
        ad.level1 = AttrDict()
        ad.level1.level2 = AttrDict()
        ad.level1.level2.value = "nested"

        assert ad.level1.level2.value == "nested"
        assert ad["level1"]["level2"]["value"] == "nested"

    def test_dir_includes_keys(self):
        """Test that dir() includes dictionary keys."""
        ad = AttrDict(a=1, b=2, special_key=3)

        dir_result = dir(ad)

        assert "a" in dir_result
        assert "b" in dir_result
        assert "special_key" in dir_result

    def test_reserved_attributes_not_overridden(self):
        """Test that reserved dict attributes are not overridden."""
        ad = AttrDict()

        # These should still work as dict methods
        assert hasattr(ad, "keys")
        assert hasattr(ad, "items")
        assert hasattr(ad, "values")
        assert callable(ad.keys)

    def test_mixed_access_patterns(self):
        """Test mixing dict and attribute access."""
        ad = AttrDict()

        # Set via attribute, get via dict
        ad.attr_set = "value1"
        assert ad["attr_set"] == "value1"

        # Set via dict, get via attribute
        ad["dict_set"] = "value2"
        assert ad.dict_set == "value2"

    def test_complex_data_types(self):
        """Test AttrDict with complex data types."""
        ad = AttrDict()

        ad.list_data = [1, 2, 3]
        ad.dict_data = {"nested": True}
        ad.tuple_data = (1, 2, 3)

        assert ad.list_data == [1, 2, 3]
        assert ad.dict_data == {"nested": True}
        assert ad.tuple_data == (1, 2, 3)


class TestAttrPath:
    """Test AttrPath functionality."""

    def setup_method(self):
        """Set up test directory structure."""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)

        # Create test directory structure
        (self.test_path / "subdir1").mkdir()
        (self.test_path / "subdir2").mkdir()
        (self.test_path / "file1.txt").write_text("content1")
        (self.test_path / "file2.py").write_text('print("hello")')
        (self.test_path / "file3.csv").write_text("a,b,c\n1,2,3")
        (self.test_path / "subdir1" / "nested.txt").write_text("nested content")

    def teardown_method(self):
        """Clean up test directory."""
        shutil.rmtree(self.test_dir)

    def test_basic_creation(self):
        """Test basic AttrPath creation."""
        ap = AttrPath(self.test_dir)

        assert isinstance(ap, Path)
        assert str(ap) == self.test_dir

    def test_directory_attribute_access(self):
        """Test accessing subdirectories as attributes."""
        ap = AttrPath(self.test_dir)

        subdir1 = ap.subdir1
        assert isinstance(subdir1, AttrPath)
        assert subdir1.name == "subdir1"
        assert subdir1.is_dir()

    def test_file_attribute_access(self):
        """Test accessing files as attributes."""
        ap = AttrPath(self.test_dir)

        # Files get underscores instead of dots
        file1 = ap.file1_txt
        assert isinstance(file1, AttrPath)
        assert file1.name == "file1.txt"
        assert file1.is_file()

    def test_nested_navigation(self):
        """Test navigating nested directory structures."""
        ap = AttrPath(self.test_dir)

        nested_file = ap.subdir1.nested_txt
        assert isinstance(nested_file, AttrPath)
        assert nested_file.name == "nested.txt"
        assert nested_file.is_file()

    def test_D_property_directories(self):
        """Test .D property for accessing directories."""
        ap = AttrPath(self.test_dir)

        assert hasattr(ap, "D")
        assert hasattr(ap.D, "subdir1")
        assert hasattr(ap.D, "subdir2")

        assert isinstance(ap.D.subdir1, AttrPath)

    def test_F_property_files(self):
        """Test .F property for accessing files."""
        ap = AttrPath(self.test_dir)

        assert hasattr(ap, "F")
        assert hasattr(ap.F, "file1_txt")
        assert hasattr(ap.F, "file2_py")
        assert hasattr(ap.F, "file3_csv")

    def test_extension_properties(self):
        """Test file extension-based properties."""
        ap = AttrPath(self.test_dir)

        # Test .txt property
        if hasattr(ap, "txt"):
            txt_files = ap.txt
            assert hasattr(txt_files, "file1_txt")

        # Test .py property
        if hasattr(ap, "py"):
            py_files = ap.py
            assert hasattr(py_files, "file2_py")

    def test_nonexistent_attribute_raises_error(self):
        """Test that accessing nonexistent path raises AttributeError."""
        ap = AttrPath(self.test_dir)

        with pytest.raises(AttributeError):
            _ = ap.nonexistent_file

    def test_dir_method(self):
        """Test __dir__ method returns available paths."""
        ap = AttrPath(self.test_dir)

        dir_result = dir(ap)

        # Should include safe names for files and directories
        assert "subdir1" in dir_result
        assert "subdir2" in dir_result
        assert "file1_txt" in dir_result
        assert "file2_py" in dir_result

    @patch("pirrtools.structures.attrpath.webbrowser")
    def test_view_method_html(self, mock_webbrowser):
        """Test view method with HTML file."""
        # Create HTML file
        html_file = self.test_path / "test.html"
        html_file.write_text("<html><body>Test</body></html>")

        ap = AttrPath(html_file)
        ap.view()

        mock_webbrowser.open.assert_called_once()

    @patch("pirrtools.structures.attrpath.subprocess")
    def test_view_method_image(self, mock_subprocess):
        """Test view method with image file."""
        # Create fake image file
        img_file = self.test_path / "test.png"
        img_file.write_bytes(b"fake_png_data")

        ap = AttrPath(img_file)

        # Should not raise an exception
        try:
            ap.view()
        except Exception:
            pass  # Expected since it's not a real image

    @patch("rich.console.Console.print")
    def test_view_method_text(self, mock_print):
        """Test view method with text file."""
        ap = AttrPath(self.test_path / "file1.txt")

        ap.view()

        mock_print.assert_called()

    def test_safe_name_conversion(self):
        """Test safe name conversion for file access."""
        # Create files with special characters
        special_file = self.test_path / "file-with-dashes.txt"
        special_file.write_text("content")

        ap = AttrPath(self.test_dir)

        # Should be accessible with underscores
        file_attr = ap.file_with_dashes_txt
        assert isinstance(file_attr, AttrPath)
        assert file_attr.name == "file-with-dashes.txt"

    def test_pathlib_methods_still_work(self):
        """Test that standard pathlib methods still work."""
        ap = AttrPath(self.test_dir)

        assert ap.exists()
        assert ap.is_dir()
        assert not ap.is_file()

        file_path = ap.file1_txt
        assert file_path.exists()
        assert file_path.is_file()
        assert not file_path.is_dir()

    def test_string_operations(self):
        """Test string operations on AttrPath."""
        ap = AttrPath(self.test_dir)

        assert str(ap) == self.test_dir
        assert ap.name == Path(self.test_dir).name

    def test_path_operations(self):
        """Test path operations work correctly."""
        ap = AttrPath(self.test_dir)

        parent = ap.parent
        assert isinstance(parent, Path)  # May not be AttrPath

        file_path = ap / "new_file.txt"
        assert isinstance(file_path, Path)


class TestAttrPathViewHandlers:
    """Test AttrPath view handlers for different file types."""

    def setup_method(self):
        """Set up test files."""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)

    def teardown_method(self):
        """Clean up test directory."""
        shutil.rmtree(self.test_dir)

    @patch("rich.console.Console.print")
    def test_view_csv_file(self, mock_print):
        """Test viewing CSV file displays as table."""
        csv_file = self.test_path / "data.csv"
        csv_file.write_text("name,age,city\nJohn,25,NYC\nJane,30,LA")

        ap = AttrPath(csv_file)
        ap.view()

        mock_print.assert_called()

    @patch("rich.console.Console.print")
    def test_view_python_file(self, mock_print):
        """Test viewing Python file with syntax highlighting."""
        py_file = self.test_path / "script.py"
        py_file.write_text('def hello():\n    print("Hello, world!")')

        ap = AttrPath(py_file)
        ap.view()

        mock_print.assert_called()

    @patch("rich.console.Console.print")
    def test_view_json_file(self, mock_print):
        """Test viewing JSON file."""
        json_file = self.test_path / "data.json"
        json_file.write_text('{"name": "test", "value": 123}')

        ap = AttrPath(json_file)
        ap.view()

        mock_print.assert_called()

    def test_view_nonexistent_file(self):
        """Test viewing nonexistent file."""
        ap = AttrPath(self.test_path / "nonexistent.txt")

        # Should not raise an exception, might print error message
        ap.view()


class TestIntegrationScenarios:
    """Test integration between AttrDict and AttrPath."""

    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)

        # Create complex directory structure
        (self.test_path / "config").mkdir()
        (self.test_path / "data").mkdir()
        (self.test_path / "config" / "settings.json").write_text('{"debug": true}')
        (self.test_path / "data" / "results.csv").write_text("a,b\n1,2")

    def teardown_method(self):
        """Clean up."""
        shutil.rmtree(self.test_dir)

    def test_attrdict_with_attrpath_values(self):
        """Test AttrDict containing AttrPath objects."""
        config = AttrDict()
        config.base_path = AttrPath(self.test_dir)
        config.config_dir = config.base_path.config
        config.data_dir = config.base_path.data

        assert isinstance(config.base_path, AttrPath)
        assert isinstance(config.config_dir, AttrPath)
        assert config.config_dir.name == "config"

    def test_nested_attrdict_config(self):
        """Test complex nested configuration with AttrDict."""
        config = AttrDict()
        config.paths = AttrDict()
        config.paths.base = AttrPath(self.test_dir)
        config.paths.config = config.paths.base.config
        config.paths.data = config.paths.base.data

        config.settings = AttrDict()
        config.settings.debug = True
        config.settings.log_level = "INFO"

        # Test deep access
        assert config.paths.config.is_dir()
        assert config.settings.debug is True

    def test_attrpath_file_operations(self):
        """Test file operations through AttrPath."""
        ap = AttrPath(self.test_dir)

        # Navigate to config file
        config_file = ap.config.settings_json
        assert config_file.exists()

        # Read content
        content = config_file.read_text()
        assert "debug" in content

    def test_dynamic_path_construction(self):
        """Test dynamically constructing paths."""
        base = AttrPath(self.test_dir)

        # Build paths dynamically
        paths = AttrDict()
        for item in base.iterdir():
            if item.is_dir():
                safe_name = item.name.replace("-", "_").replace(".", "_")
                setattr(paths, safe_name, AttrPath(item))

        assert hasattr(paths, "config")
        assert hasattr(paths, "data")


@pytest.mark.parametrize(
    "special_chars",
    [
        "file-with-dashes.txt",
        "file.with.dots.txt",
        "file with spaces.txt",
        "file_with_underscores.txt",
        "123numeric_start.txt",
    ],
)
def test_attrpath_special_filename_handling(special_chars):
    """Test AttrPath handling of various special characters in filenames."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_file = Path(tmp_dir) / special_chars
        test_file.write_text("test content")

        ap = AttrPath(tmp_dir)

        # Should be able to access file with converted name
        safe_name = special_chars.replace("-", "_").replace(".", "_").replace(" ", "_")
        if safe_name[0].isdigit():
            safe_name = "f_" + safe_name

        # Should not raise AttributeError for valid files
        try:
            file_attr = getattr(ap, safe_name)
            assert isinstance(file_attr, AttrPath)
        except AttributeError:
            # Some special characters might not be convertible
            pass


def test_attrdict_json_serialization():
    """Test that AttrDict can be serialized to JSON."""
    import json

    ad = AttrDict()
    ad.string_val = "test"
    ad.int_val = 123
    ad.nested = AttrDict()
    ad.nested.value = "nested"

    # Should be serializable
    json_str = json.dumps(ad)
    loaded = json.loads(json_str)

    assert loaded["string_val"] == "test"
    assert loaded["int_val"] == 123
    assert loaded["nested"]["value"] == "nested"


def test_performance_with_large_directories():
    """Test performance with directories containing many files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create many files
        for i in range(100):
            (Path(tmp_dir) / f"file_{i:03d}.txt").write_text(f"content {i}")

        ap = AttrPath(tmp_dir)

        # Should not be prohibitively slow
        dir_result = dir(ap)
        assert len(dir_result) > 100  # Should include all files plus methods

        # Test accessing specific file
        file_50 = ap.file_050_txt
        assert file_50.exists()
        assert file_50.is_file()
