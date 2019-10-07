# -*- coding: utf-8 -*-

def load_SubPlayItem(fobj, length2, length2a):
    # NOTE: see https://github.com/lerks/BluRay/wiki/SubPlayItem

    # Import modules ...
    import struct

    # Initialize variables ...
    ans = {}
    length2b = 0                                                                                                        # [B]

    # Read the binary data ...
    ans[u"Length"], = struct.unpack(u">H", fobj.read(2));                                                               length2 += 2; length2a += 2

    # NOTE: SubPlayItem is not implemented

    # Pad out the read ...
    if length2b != ans[u"Length"]:
        l = ans[u"Length"] - length2b                                                                                   # [B]
        fobj.read(l);                                                                                                   length2 += l; length2a += l; length2b += l

    # Return answer ...
    return ans, length2, length2a, length2b
