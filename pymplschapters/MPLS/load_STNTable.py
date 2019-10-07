# -*- coding: utf-8 -*-

def load_STNTable(fobj, length2, length2a):
    # NOTE: see https://github.com/lerks/BluRay/wiki/STNTable

    # Import modules ...
    import struct

    # Load sub-functions ...
    from .load_StreamAttributes import load_StreamAttributes
    from .load_StreamEntry import load_StreamEntry

    # Initialize variables ...
    ans = {}
    length2b = 0                                                                                                        # [B]

    # Read the binary data ...
    ans[u"Length"], = struct.unpack(u">H", fobj.read(2));                                                               length2 += 2; length2a += 2
    fobj.read(2);                                                                                                       length2 += 2; length2a += 2; length2b += 2
    ans[u"NumberOfPrimaryVideoStreamEntries"], = struct.unpack(u">B", fobj.read(1));                                    length2 += 1; length2a += 1; length2b += 1
    ans[u"NumberOfPrimaryAudioStreamEntries"], = struct.unpack(u">B", fobj.read(1));                                    length2 += 1; length2a += 1; length2b += 1
    ans[u"NumberOfPrimaryPGStreamEntries"], = struct.unpack(u">B", fobj.read(1));                                       length2 += 1; length2a += 1; length2b += 1
    ans[u"NumberOfPrimaryIGStreamEntries"], = struct.unpack(u">B", fobj.read(1));                                       length2 += 1; length2a += 1; length2b += 1
    ans[u"NumberOfSecondaryAudioStreamEntries"], = struct.unpack(u">B", fobj.read(1));                                  length2 += 1; length2a += 1; length2b += 1
    ans[u"NumberOfSecondaryVideoStreamEntries"], = struct.unpack(u">B", fobj.read(1));                                  length2 += 1; length2a += 1; length2b += 1
    ans[u"NumberOfSecondaryPGStreamEntries"], = struct.unpack(u">B", fobj.read(1));                                     length2 += 1; length2a += 1; length2b += 1
    fobj.read(5);                                                                                                       length2 += 5; length2a += 5; length2b += 5

    # Loop over stream list names ...
    for name in [u"PrimaryVideoStreamEntries", u"PrimaryAudioStreamEntries", u"PrimaryPGStreamEntries", u"SecondaryPGStreamEntries", u"PrimaryIGStreamEntries", u"SecondaryAudioStreamEntries", u"SecondaryVideoStreamEntries"]:
        # Loop over entries and add to list ...
        ans[name] = []
        for i in range(ans[u"NumberOf{0:s}".format(name)]):
            tmp = {}
            res, length2, length2a, length2b, length2c = load_StreamEntry(fobj, length2, length2a, length2b)
            tmp[u"StreamEntry"] = res
            res, length2, length2a, length2b, length2c = load_StreamAttributes(fobj, length2, length2a, length2b)
            tmp[u"StreamAttributes"] = res
            ans[name].append(tmp)

    # Pad out the read ...
    if length2b != ans[u"Length"]:
        l = ans[u"Length"] - length2b                                                                                   # [B]
        fobj.read(l);                                                                                                   length2 += l; length2a += l; length2b += l

    # Return answer ...
    return ans, length2, length2a, length2b
