"""
Worldcraft Commands Line Utillities
"""

from worldcraftcommand import package_data

DEFAULT = package_data('default.wc')

def main():
    print(__doc__)

    with open(DEFAULT) as file_handle:
        print(file_handle.read())
    exit(1)
