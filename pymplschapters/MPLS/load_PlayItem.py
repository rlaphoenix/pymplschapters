# -*- coding: utf-8 -*-

def load_PlayItem(fobj, length2):
    # NOTE: see https://github.com/lerks/BluRay/wiki/PlayItem

    # Import modules ...
    import struct

    # Load sub-functions ...
    from .load_STNTable import load_STNTable

    # Initialize variables ...
    ans = {}
    length2a = 0                                                                                                        # [B]

    # Read the binary data ...
    ans[u"Length"], = struct.unpack(u">H", fobj.read(2));                                                               length2 += 2
    ans[u"ClipInformationFileName"] = fobj.read(5).decode('utf-8');                                                     length2 += 5; length2a += 5
    ans[u"ClipCodecIdentifier"] = fobj.read(4).decode('utf-8');                                                         length2 += 4; length2a += 4
    ans[u"MiscFlags1"], = struct.unpack(u">H", fobj.read(2));                                                           length2 += 2; length2a += 2
    ans[u"IsMultiAngle"] = bool(ans[u"MiscFlags1"]&(1<<11))
    ans[u"RefToSTCID"], = struct.unpack(u">B", fobj.read(1));                                                           length2 += 1; length2a += 1
    ans[u"INTime"], = struct.unpack(u">I", fobj.read(4));                                                               length2 += 4; length2a += 4
    ans[u"OUTTime"], = struct.unpack(u">I", fobj.read(4));                                                              length2 += 4; length2a += 4
    ans[u"UOMaskTable"], = struct.unpack(u">Q", fobj.read(8));                                                          length2 += 8; length2a += 8
    ans[u"MiscFlags2"], = struct.unpack(u">B", fobj.read(1));                                                           length2 += 1; length2a += 1
    ans[u"StillMode"], = struct.unpack(u">B", fobj.read(1));                                                            length2 += 1; length2a += 1
    if ans[u"StillMode"] == int(0x01):
        ans[u"StillTime"], = struct.unpack(u">H", fobj.read(2));                                                        length2 += 2; length2a += 2
    else:
        fobj.read(2).decode('utf-8');                                                                                   length2 += 2; length2a += 2
    if ans[u"IsMultiAngle"]:
        raise Exception("IsMultiAngle has not been implemented as the specification is not byte-aligned (IsDifferentAudios is 6-bit and IsSeamlessAngleChange is 1-bit)")

    # Load STNTable section ...
    res, length2, length2a, length2b = load_STNTable(fobj, length2, length2a)
    ans[u"STNTable"] = res

    # Pad out the read ...
    if length2a != ans[u"Length"]:
        l = ans[u"Length"] - length2a                                                                                   # [B]
        fobj.read(l);                                                                                                   length2 += l; length2a += l

    # Return answer ...
    return ans, length2, length2a
