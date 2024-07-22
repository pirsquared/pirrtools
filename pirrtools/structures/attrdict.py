"""A dictionary that allows access to its keys as attributes."""


class AttrDict(dict):
    """A dictionary that allows access to its keys as attributes.

    Example:

    >>> d = AttrDict({'a': 1, 'b': 2})
    >>> d.a
    1

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convert nested dictionaries to AttrDict instances
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = AttrDict(value)

    def __getattr__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError as exc:
            raise AttributeError(
                f"'AttrDict' object has no attribute '{item}'"
            ) from exc

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, item):
        try:
            del self[item]
        except KeyError as exc:
            raise AttributeError(
                f"'AttrDict' object has no attribute '{item}'"
            ) from exc

    def __dir__(self):
        return list(self.keys()) + super().__dir__()

    def __getitem__(self, key):
        return super().setdefault(key, type(self)())

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            value = type(self)(value)
        super().__setitem__(key, value)
