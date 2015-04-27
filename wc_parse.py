#!/usr/bin/env python2

"""
    wc_parse

    wc file parser
"""

import argparse

ARGP = argparse.ArgumentParser(
    description='Extract values from Source SDK .wc files.'
)
ARGP.add_argument('file_path', help="Path to .wc file.")

class _open(file):
    """
        Open wrapper with read_ahead.
    """
    def read_ahead(self, numbytes=None):
        """
            Read some bytes and set the cursor back.

            Params:
                n int: number if bytes to read.

            Retunrs:
                str: bytes read.
        """
        cursor_position = self.tell()
        bytes_read = self.read(numbytes)
        self.seek(cursor_position)

        return bytes_read

def wc_parse(file_path):
    """
        Parse wc file at file_path

        Params:
            file_path str: path to wc file.

        Returns:
            dict: Parsed confiruation options.
    """
    output = dict()

    with _open(file_path, 'rb') as file_handle:
        # Trim file header
        file_handle.seek(39)

        try:
            while True:
                # Read 140 bytes, trim at the first zero byte
                name = file_handle.read(140).split('\x00', 1)[0]

                # Indicates EOF
                if name == '':
                    raise StopIteration()

                output[name] = list()

                try:
                    while True:
                        # Read: command 260, arguments 536
                        callm = file_handle.read(260).split('\x00', 1)[0]
                        calla = file_handle.read(536).split('\x00', 1)[0]
                        output[name].append((callm, calla))

                        # Check the next character
                        next_byte = file_handle.read_ahead(1)
                        if next_byte != '\x01':
                            # If we don't get a continuation character, break.
                            raise StopIteration()

                        # On continuation, discard the next eight bytes.
                        _ = file_handle.read(8)

                except StopIteration:
                    # No more commands for this script.
                    pass

        except StopIteration:
            # No more scripts in this .wc file
            pass

    return output

def main(argp=None):
    """
        Cli Method
    """
    if not argp:
        argp = ARGP.parse_args()

    print(wc_parse(argp.file_path))


if __name__ == '__main__':
    main()
