#!/usr/bin/env python2

"""
    Decode wc files into keyed columnar sets of ordered config information
"""

import re
import string
import struct

from collections import OrderedDict

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

HEADER = 'Worldcraft Command Sequences'

class WcCmdSeq(dict):
    def __init__(self, header=None):
        super(WcCmdSeq, self).__init__()

        if header is None:
            header = HEADER

        self.header = header


class WorldcraftCommandDecoder(object):
    """WorldcraftCommandDecoder"""

    WC_FILE = OrderedDict(
        format_name='35s',
        num_configs='I'
    )
    WC_COMMANDS = OrderedDict(
        config_name='128s',
        num_commands='I'
    )
    WC_COMMAND = OrderedDict(
        enabled='?7x',
        command='260s',
        arguments='260s',
        post_enabled='?7x',
        post_path='260s',
        log_enabled='?7x'
    )

    NON_ASCI = re.compile('[^{}]'.format(re.escape(string.printable)))

    def __init__(self):
        super(WorldcraftCommandDecoder, self).__init__()

    def _ascii(self, value):
        """
            Split value on non-printable-ascii characters.

            Args:
                value str: WorldcraftCommand string data.

            Returns:
                str: Left most set of printable ascii characters.
        """
        return self.NON_ASCI.split(value, 1)[0].strip()

    def _unpack(self, packs, file_handle):
        """
            Wrapper for strut.unpack

            Handles only a single packed value at a time, I was unable
            to unpack data headers in one call, values were incorrect.

            Unpacked strings have non-printable ascii characters removed,
            trailing whitespace removed.

            Strings in WorldcraftCommand files are terminated by a \x00
            byte, so garbage suffixing that byte is split/trimmed as well.

            Args:
                packs OrderedDict: Named struck.pack values.
                file_handle file: Object to read bytes from.

            Returns:
                OrderedDict:
                    Key: Data name.
                    value: Cleaned data.

        """
        output = OrderedDict()
        for key, pack in packs.iteritems():
            value = struct.unpack(
                pack,
                file_handle.read(struct.calcsize(pack))
            )[0]

            if pack.endswith('s'):
                value = self._ascii(value)

            output[key] = value

        return output

    def decode(self, raw):
        """
            Primary decode method

            Args:
                raw: A file handle to a wc file.

            Returns:
                tuple:
                    0 str: Wc file header string. (Garbage)
                    1 WcCmdSeq:
                        key: Config Name
                        value list:
                            item OrderedDict:
                                key: Command data name.
                                value: Data from file.
        """
        file_handle = StringIO.StringIO(raw)
        name, num_entries = self._unpack(self.WC_FILE, file_handle).values()

        entries = WcCmdSeq()
        for _ in range(num_entries):
            config, num_commands = self._unpack(
                self.WC_COMMANDS, file_handle
            ).values()
            entries[config] = list()
            commands = entries[config]
            for _ in range(num_commands):
                commands.append(
                    self._unpack(self.WC_COMMAND, file_handle)
                )

        return entries
