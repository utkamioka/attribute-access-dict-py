class Map(dict):
    """
    >>> m = Map(a=10, b=20)
    >>> m.a
    10
    >>> m.b
    20
    >>> m.c = 30
    >>> m.c
    30
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


if __name__ == "__main__":
    import doctest
    doctest.testmod()
