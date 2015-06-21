"""
WorldCraftCommand Library
"""

# Root
import os

_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        'data',
    )
)
_USER = os.path.expanduser(
    os.path.join(
        '~',
        '.config',
        'worldcraftcommand',
    )
)

def package_data(resource):
    return os.path.join(_ROOT, resource)

def user_data(resource):
    return os.path.join(_USER, resource)

# Scripts
from . import compiler
from . import gnome
from . import util


