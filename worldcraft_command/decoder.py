#!/usr/bin/env python2

import re
import string
import struct

from collections import OrderedDict

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


class WorldcraftCommandDecoder(object):
    """docstring for WorldcraftCommandDecoder"""

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
        return self.NON_ASCI.split(value, 1)[0].strip()

    def _unpack(self, packs, file_handle):
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
        file_handle = StringIO.StringIO(raw)
        name, num_entries = self._unpack(self.WC_FILE, file_handle).values()

        entries = dict()
        for _ in range(num_entries):
            config, num_commands = self._unpack(self.WC_COMMANDS, file_handle).values()
            entries[config] = list()
            commands = entries[config]
            for _ in range(num_commands):
                commands.append(
                    self._unpack(self.WC_COMMAND, file_handle)
                )

        return (name, entries)
