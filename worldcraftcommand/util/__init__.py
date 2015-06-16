"""
Worldcraft Commands Line Utillities
"""

from worldcraftcommand import package_data
from worldcraftcommand import user_data

DEFAULT = package_data('default.wc')

def main():
    print(__doc__)

    with open(DEFAULT) as file_handle:
        print(file_handle.read())
    print(user_data('default.wc'))
    exit(1)
