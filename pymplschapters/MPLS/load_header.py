# -*- coding: utf-8 -*-

def load_header(fobj):
    # NOTE: see https://github.com/lerks/BluRay/wiki/MPLS

    # Import modules ...
    import struct

    # Initialize variables ...
    ans = {}
    length0 = 0                                                                                                         # [B]

    # Read the binary data ...
    ans[u"TypeIndicator"] = fobj.read(4);                                                                               length0 +=  4
    ans[u"VersionNumber"] = fobj.read(4);                                                                               length0 +=  4
    ans[u"PlayListStartAddress"], = struct.unpack(u">I", fobj.read(4));                                                 length0 +=  4
    ans[u"PlayListMarkStartAddress"], = struct.unpack(u">I", fobj.read(4));                                             length0 +=  4
    ans[u"ExtensionDataStartAddress"], = struct.unpack(u">I", fobj.read(4));                                            length0 +=  4
    fobj.read(20);                                                                                                      length0 += 20

    # Return answer ...
    return ans, length0
