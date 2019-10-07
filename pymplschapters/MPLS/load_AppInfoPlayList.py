# -*- coding: utf-8 -*-

def load_AppInfoPlayList(fobj):
    # NOTE: see https://github.com/lerks/BluRay/wiki/AppInfoPlayList

    # Import modules ...
    import struct

    # Initialize variables ...
    ans = {}
    length1 = 0                                                                                                         # [B]

    # Read the binary data ...
    ans[u"Length"], = struct.unpack(u">I", fobj.read(4))
    fobj.read(1);                                                                                                       length1 += 1
    ans[u"PlaybackType"], = struct.unpack(u">B", fobj.read(1));                                                         length1 += 1
    if ans[u"PlaybackType"] == int(0x02) or ans[u"PlaybackType"] == int(0x03):
        ans[u"PlaybackCount"], = struct.unpack(u">H", fobj.read(2));                                                    length1 += 2
    else:
        fobj.read(2);                                                                                                   length1 += 2
    ans[u"UOMaskTable"], = struct.unpack(u">Q", fobj.read(8));                                                          length1 += 8
    ans[u"MiscFlags"], = struct.unpack(u">H", fobj.read(2));                                                            length1 += 2

    # Pad out the read ...
    if length1 != ans[u"Length"]:
        l = ans[u"Length"] - length1                                                                                    # [B]
        fobj.read(l);                                                                                                   length1 += l

    # Return answer ...
    return ans, length1
