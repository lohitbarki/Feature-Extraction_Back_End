from General.Connection import getVendorAllList
from General.Connection import inserVendor
from General.Connection import inserVersion
import sys

vendor = sys.argv[1];
feed_name = sys.argv[2];
url = sys.argv[3];


def isVendor_Present(vendor):
    vendor_List = getVendorAllList()
    for list in vendor_List:
        #print(list)
        #print(vendor)
        if list == vendor:
            return True
        else:
            return False


if not isVendor_Present(vendor):
    id = inserVendor(vendor);
    print(id)
    inserVersion(feed_name, url, str(id));