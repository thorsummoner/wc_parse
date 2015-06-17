#!/usr/bin/env python2

class WorldcraftCommandEncoder(object):
    def __init__(self):
        super(WorldcraftCommandEncoder, self).__init__()

    def iterencode(self, obj):
        raise NotImplementedError

    def encode(self, obj):
        raise NotImplementedError

