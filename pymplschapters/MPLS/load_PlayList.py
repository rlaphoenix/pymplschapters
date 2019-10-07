# -*- coding: utf-8 -*-

def load_PlayList(fobj):
    # NOTE: see https://github.com/lerks/BluRay/wiki/PlayList

    # Import modules ...
    import struct

    # Load sub-functions ...
    from .load_PlayItem import load_PlayItem
    from .load_SubPath import load_SubPath

    # Initialize variables ...
    ans = {}
    length2 = 0                                                                                                         # [B]

    # Read the binary data ...
    ans[u"Length"], = struct.unpack(u">I", fobj.read(4))
    fobj.read(2);                                                                                                       length2 += 2
    ans[u"NumberOfPlayItems"], = struct.unpack(u">H", fobj.read(2));                                                    length2 += 2
    ans[u"NumberOfSubPaths"], = struct.unpack(u">H", fobj.read(2));                                                     length2 += 2

    # Loop over PlayItems ...
    ans[u"PlayItems"] = []
    for i in range(ans[u"NumberOfPlayItems"]):
        # Load PlayItem section and append to PlayItems list ...
        res, length2, length2a = load_PlayItem(fobj, length2)
        ans[u"PlayItems"].append(res)

    # Loop over SubPaths ...
    ans[u"SubPaths"] = []
    for i in range(ans[u"NumberOfSubPaths"]):
        # Load SubPath section and append to SubPaths list ...
        res, length2, length2a = load_SubPath(fobj, length2)
        ans[u"SubPaths"].append(res)

    # Pad out the read ...
    if length2 != ans[u"Length"]:
        l = ans[u"Length"] - length2                                                                                    # [B]
        fobj.read(l);                                                                                                   length2 += l

    # Return answer ...
    return ans, length2
