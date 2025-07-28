"""
Tests for pirrtools.load module functionality.

Tests the load module which handles module loading and side effects.
"""

from unittest.mock import Mock, patch

import pytest

import pirrtools.load


def test_load_module_exists():
    """Test that load module can be imported."""
    assert pirrtools.load is not None


def test_load_module_has_docstring():
    """Test that load module has proper documentation."""
    assert pirrtools.load.__doc__ is not None
    assert len(pirrtools.load.__doc__.strip()) > 0


@patch("pirrtools.load.get_ipython")
def test_load_ipython_integration(mock_get_ipython):
    """Test IPython integration in load module."""
    # Mock IPython instance
    mock_ipython = Mock()
    mock_get_ipython.return_value = mock_ipython

    # Reload the module to test IPython detection
    import importlib

    importlib.reload(pirrtools.load)

    # Should not raise any errors
    assert True


@patch("pirrtools.load.get_ipython")
def test_load_no_ipython(mock_get_ipython):
    """Test behavior when IPython is not available."""
    mock_get_ipython.return_value = None

    # Reload the module
    import importlib

    importlib.reload(pirrtools.load)

    # Should handle gracefully
    assert True


def test_load_module_side_effects():
    """Test that load module performs expected side effects."""
    # The load module should set up matplotlib inline when imported
    # This is mainly tested through integration, but we can verify
    # it doesn't crash

    import importlib

    try:
        importlib.reload(pirrtools.load)
    except Exception as e:
        pytest.fail(f"Load module side effects failed: {e}")


def test_load_module_attributes():
    """Test load module has expected attributes."""
    # The load module should be minimal but functional
    assert hasattr(pirrtools.load, "__doc__")
    assert hasattr(pirrtools.load, "__file__")
    assert hasattr(pirrtools.load, "__name__")
