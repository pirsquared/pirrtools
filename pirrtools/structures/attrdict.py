"""Enhanced dictionary with attribute-style access.

This module provides the AttrDict class, which extends the standard
Python dictionary to allow accessing keys as attributes, making it
more convenient for interactive use and structured data access.
"""

__all__ = ["AttrDict"]


class AttrDict(dict):
    """Dictionary subclass that supports attribute-style access to keys.

    This class extends the standard dict to allow accessing dictionary
    keys as attributes, providing a more convenient syntax for nested
    data structures. Nested dictionaries are automatically converted
    to AttrDict instances.

    Attributes are created dynamically based on dictionary keys, and
    missing keys create new empty AttrDict instances when accessed.

    Examples:
        >>> d = AttrDict({'a': 1, 'b': 2})
        >>> d.a
        1
        >>> d.c.d = 'nested'  # Creates nested structure
        >>> d.c.d
        'nested'

        >>> nested = AttrDict({'x': {'y': {'z': 42}}})
        >>> nested.x.y.z
        42

    Note:
        Attribute names that conflict with dict methods (like 'keys', 'items')
        will still access the dict methods, not the stored values.
    """

    def __init__(self, *args, **kwargs):
        """Initialize AttrDict with automatic nested conversion.

        Args:
            *args: Positional arguments passed to dict constructor.
            **kwargs: Keyword arguments passed to dict constructor.

        Note:
            Any nested dictionaries in the input are automatically
            converted to AttrDict instances for consistent attribute access.
        """
        super().__init__(*args, **kwargs)
        # Convert nested dictionaries to AttrDict instances
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = type(self)(value)

    def __getattr__(self, item):
        """Get dictionary value as attribute.

        Args:
            item (str): The attribute/key name to access.

        Returns:
            The value associated with the key.

        Raises:
            AttributeError: If the key doesn't exist.
        """
        try:
            return super().__getitem__(item)
        except KeyError as exc:
            raise AttributeError(
                f"'AttrDict' object has no attribute '{item}'"
            ) from exc

    def __setattr__(self, key, value):
        """Set dictionary value as attribute.

        Args:
            key (str): The attribute/key name to set.
            value: The value to associate with the key.
        """
        self[key] = value

    def __delattr__(self, item):
        """Delete dictionary key as attribute.

        Args:
            item (str): The attribute/key name to delete.

        Raises:
            AttributeError: If the key doesn't exist.
        """
        try:
            del self[item]
        except KeyError as exc:
            raise AttributeError(
                f"'AttrDict' object has no attribute '{item}'"
            ) from exc

    def __dir__(self):
        """Return list of available attributes (dictionary keys).

        Returns:
            list: List of dictionary keys available as attributes.
        """
        return list(self.keys())

    def __getitem__(self, key):
        """Get item with automatic AttrDict creation for missing keys.

        Args:
            key: The dictionary key to access.

        Returns:
            The value for the key, or a new empty AttrDict if key doesn't exist.
        """
        return super().setdefault(key, type(self)())

    def __setitem__(self, key, value):
        """Set item with automatic dict-to-AttrDict conversion.

        Args:
            key: The dictionary key to set.
            value: The value to set. Plain dicts are converted to AttrDict.
        """
        if isinstance(value, dict) and not isinstance(value, AttrDict):
            value = type(self)(value)
        super().__setitem__(key, value)
