#!/usr/bin/env python2

"""
    wc_parse

    wc file parser
"""

import argparse
import binascii
import re
import string
import textwrap

from pprint import pprint

ARGP = argparse.ArgumentParser(
    description='Extract values from Source SDK .wc files.'
)
ARGP.add_argument('file_path', help="Path to .wc file.")

BYTE_FLAG = {
    '\x00': False,
    '\x01': True,
}

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

    def seek_ahead(self, numbytes):
        """
            Seek forward without reading.

            Args:
                numbytes int: Number of bytes to skip ahead by.

            Retunrs:
                None
        """
        self.seek(self.tell() + numbytes)

class WcStr(object):
    """wc file string"""

    FLAG_BYTES = 8
    NON_ASCI = re.compile('[^{}]'.format(re.escape(string.printable)))

    def __init__(self, value, flags):
        super(WcStr, self).__init__()
        self.raw = flags+value
        self.value = self.NON_ASCI.split(value, 1)[0].strip()
        self.flags = flags

    def __str__(self):
        return self.value

    def __repr__(self):
        return '{}{}{}'.format(
            ' '.join([
                # Hex represent flags
                '\033[30;1m{}\033[0m'.format(
                    binascii.hexlify(c)
                ) for c in self.flags
            ]),
            (' ' if self.flags else ''),
            repr(self.value)
        )

    def bool_flag_at(self, idx):
        """
            Interpret a byte as a boolean

            Args:
                idx int: 0-based offset in self.flags to look at.

            Returns:
                bool: Translation from module BYTE_FLAG dict.

            Raises:
                ValueError: When byte not in BYTE_FLAG
        """
        if not self.flags[idx] in BYTE_FLAG:
            raise ValueError(
                'Flag byte `{}` at {}, is not boolean.'.format(
                    binascii.hexlify(self.flags[idx]),
                    idx
                )
            )

        return BYTE_FLAG[self.flags[idx]]

    @classmethod
    def new_bytes(cls, raw_value, flag_bytes=None):
        """
            New from bytes, interpret first n-bytes as a flag sequence.

            Args:
                raw_value str: Sequence of bytes.
                flag_bytes int: Number of header bytes to use as flags.

            Returns:
                WcStr
        """
        if flag_bytes is None:
            flag_bytes = cls.FLAG_BYTES

        return cls(
            raw_value[flag_bytes:],
            raw_value[:flag_bytes]
        )

class WcAction(object):
    """docstring for WcAction"""

    @property
    def enabled(self):
        """
            Get state of enabled flag.

            Returns:
                bool
        """
        return BYTE_FLAG[self.call.flags[0]]

    def __init__(self, call, args, check, unknown):
        super(WcAction, self).__init__()
        self.call = call
        self.args = args
        self.check = check
        self.unknown = unknown

    def __str__(self):

        output = textwrap.dedent('''
            call         {}
            args         {}
            check        {}
            unknown      {}
        ''').format(
            repr(self.call),
            # binascii.hexlify(call.raw)
            repr(self.args),
            # binascii.hexlify(args.raw)
            repr(self.check),
            # binascii.hexlify(check.raw)
            repr(self.unknown),
            # binascii.hexlify(unknown.raw)
        )

        return output

    def __repr__(self):
        output = '{}{} {}'.format(
            ('' if self.enabled else '# '),
            self.call,
            self.args
        )

        return output

class WcScript(list):
    """docstring for WcScript"""
    def __init__(self, name):
        super(WcScript, self).__init__()
        self.name = name


def wc_parse(file_path):
    """
        Parse wc file at file_path

        Params:
            file_path str: path to wc file.

        Returns:
            dict: Parsed configuration options.
    """
    output = dict()

    with _open(file_path, 'rb') as file_handle:

        # File title
        title = WcStr.new_bytes(file_handle.read(31), flag_bytes=0)

        try:
            while True:
                name = WcStr.new_bytes(file_handle.read(140))
                # Indicates EOF
                if str(name) == '':
                    raise StopIteration()

                output[str(name)] = WcScript(name)

                try:
                    while True:
                        # Read: command 260, arguments 268, check file path 268
                        call = WcStr.new_bytes(file_handle.read(260))
                        args = WcStr.new_bytes(file_handle.read(260))
                        check = WcStr.new_bytes(file_handle.read(260))
                        # Discard sixteen bytes or unknown.
                        unknown = WcStr.new_bytes(file_handle.read(16), 16)

                        end = WcStr.new_bytes(file_handle.read_ahead(8), 8)

                        output[str(name)].append(
                            WcAction(
                                call,
                                args,
                                check,
                                unknown
                            )
                        )

                        if not end.bool_flag_at(4):
                            file_handle.seek_ahead(8)
                        else:
                            raise StopIteration()

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

    pprint(
        wc_parse(argp.file_path),
        width=120
    )


if __name__ == '__main__':
    main()
