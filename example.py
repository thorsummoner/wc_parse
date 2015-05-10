#!/usr/bin/env python2

import worldcraft_command

from pprint import pprint

def main():
    with open('stock_wc/CmdSeq.wc', 'r') as file_handle:
        pprint(worldcraft_command.load(file_handle))

if __name__ == '__main__':
    main()
