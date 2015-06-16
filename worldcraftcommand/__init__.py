"""
WorldCraftCommand Library
"""

# Root
import os

_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
    )
)

def package_data(resource):
    return os.path.join(_ROOT, 'data', resource)

# Scripts
from . import compiler
from . import gnome
from . import util


