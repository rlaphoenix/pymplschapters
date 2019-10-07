# -*- coding: utf-8 -*-

def load_ExtensionData(fobj):
    # NOTE: see https://github.com/lerks/BluRay/wiki/ExtensionData

    # Import modules ...
    import struct

    # Initialize variables ...
    ans = {}
    length4 = 0                                                                                                         # [B]

    # Read the binary data ...
    ans[u"Length"], = struct.unpack(u">I", fobj.read(4))
    if ans[u"Length"] != 0:
        ans[u"DataBlockStartAddress"], = struct.unpack(u">I", fobj.read(4));                                            length4 += 4
        fobj.read(3);                                                                                                   length4 += 4
        ans[u"NumberOfExtDataEntries"], = struct.unpack(u">B", fobj.read(1));                                           length4 += 1
        ans[u"ExtDataEntries"] = []
        for i in range(ans[u"NumberOfExtDataEntries"]):
            tmp = {}
            tmp[u"ExtDataType"], = struct.unpack(u">H", fobj.read(2));                                                  length4 += 2
            tmp[u"ExtDataVersion"], = struct.unpack(u">H", fobj.read(2));                                               length4 += 2
            tmp[u"ExtDataStartAddress"], = struct.unpack(u">I", fobj.read(4));                                          length4 += 4
            tmp[u"ExtDataLength"], = struct.unpack(u">I", fobj.read(4));                                                length4 += 4
            ans[u"ExtDataEntries"].append(tmp)

        # NOTE: ExtDataEntries is not implemented

        # Pad out the read ...
        if length4 != ans[u"Length"]:
            l = ans[u"Length"] - length4                                                                                # [B]
            fobj.read(l);                                                                                               length4 += l

    # Return answer ...
    return ans, length4
