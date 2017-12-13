from itertools import zip_longest


def _normalize(data, width):
    return tuple(
        map(
            lambda datum: f'{datum:^{width}}',
            data
        )
    )


def _is_str(s):
    return isinstance(s, str)


class Str2d(object):
    def __init__(self, str_):
        """Creates a 2-D string thing that can be concatenated
        vertically and horizontally

        :param str_: Can be a newline delimited list of strings.
          Or another Str2d object, or a iterable of strings.

        Example:
        >>> s1 = Str2d('Hello\nWorld\nmy\nname\nis')
        ... s2 = Str2d('How\nAre\nYou?')
        ... s3 = Str2d('### My Cool 2D String ###')
        ...
        ... s3 / (s1 + s2)
        ### My Cool 2D String ###
               Hello How
               World Are
                my   You?
               name
                is
        """

        self.data = tuple()

        if isinstance(str_, str):
            splits = str_.splitlines()
            self.data = _normalize(splits, max(map(len, splits)))
        elif isinstance(str_, type(self)):
            self.data = str_.data
        else:
            if hasattr(str_, '__iter__') and not isinstance(str_, str):
                data = tuple(str_)
                if all(map(_is_str, data)) and bool(data):
                    self.data = _normalize(data, max(map(len, data)))

    @property
    def width(self):
        return max(map(len, self.data))

    def __repr__(self):
        return '\n'.join(self.data)

    def __add__(self, other):
        other = type(self)(other)

        width = max(self.width, other.width)
        self_data = _normalize(self.data, width)
        other_data = _normalize(other.data, width)

        return type(self)(map(
            ' '.join,
            zip_longest(
                self_data,
                other_data,
                fillvalue=' ' * width
            )
        ))

    def __truediv__(self, other):
        other = type(self)(other)
        return type(self)(self.data + other.data)
