#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""
Worldcraft Commands Line Utillities
"""

import argparse

from worldcraftcommand import package_data
from worldcraftcommand import user_data

from worldcraftcommand import wc

DEFAULT = package_data('default.wc')

ARGP = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawTextHelpFormatter,
)
ARGP.add_argument('--config', help='`.wc` File to Read.', default=DEFAULT)
ARGP.add_argument('profile', nargs='?', help='Profile Name')

def main(argp=None):
    if argp is None:
        argp = ARGP.parse_args()

    print(__doc__)
    print(user_data('default.wc'))
    with open(DEFAULT) as file_handle:
        profiles = wc.load(file_handle)

    if argp.profile is None:
        pprint(profiles.keys())
    else:

        pprint(argp.profile)
        pprint(profiles[argp.profile])
        pprint(type(profiles[argp.profile]))

        print('-'*80)
        print(profiles[argp.profile].posix())
        print('-'*80)

from pprint import pprint
