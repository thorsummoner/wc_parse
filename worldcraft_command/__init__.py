r"""Worldcraft Command (Source SDK Hammer Script)
<https://developer.valvesoftware.com/wiki/WC> is a proprietary script
database format used by Source SDK Hammer for storing user compiler
scripting.

:mod:`worldcraft_command` exposes an API familiar to users of the
standard library :mod:`json`, :mod:`marshal` and :mod:`pickle` modules.

TODO Encoding::

    >>> import worldcraft_command

TODO Decoding::

    >>> import worldcraft_command

"""
__version__ = '1.0.0-beta'
__all__ = [
    'dump', 'dumps', 'load', 'loads',
    'WorldcraftCommandDecoder', 'WorldcraftCommandEncoder',
]

__author__ = 'Dylan Grafmyre <thorsummoner@live.com>'

from .decoder import WorldcraftCommandDecoder
from .encoder import WorldcraftCommandEncoder


def dump(obj, file_handle, cls=None):
    """Serialize ``obj`` as a WorldcraftCommand formatted stream to
    ``file_handle`` (a ``.write()``-supporting file-like object).
    """
    if cls is None:
        cls = WorldcraftCommandEncoder

    iterable = cls().iterencode(obj)
    for chunk in iterable:
        file_handle.write(chunk)


def dumps(obj, cls=None):
    """Serialize ``obj`` to a WorldcraftCommand formatted ``str``.
    """
    if cls is None:
        cls = WorldcraftCommandEncoder
    return cls().encode(obj)


def load(file_handle, cls=None):
    """Deserialize ``file_handle`` (a ``.read()``-supporting file-like
    object containing a WorldcraftCommand document) to a Python object.
    """
    return loads(file_handle.read(), cls=cls)


def loads(raw, cls=None):
    """Deserialize ``raw`` (a ``str`` instance containing a
    WorldcraftCommand document) to a Python object.
    """
    if cls is None:
        cls = WorldcraftCommandDecoder

    return cls().decode(raw)
