#!/usr/bin/env python
#
# From a list of target names, generate a target list for ESO proposals

import mysci


sources = ['IRAS01003-2238']

for source in sources:
    res = mysci.queryNED(source)
    print("\\Target{A}{" + source + "}{" + \
          mysci.DecimaltoSeg(res['RA'].value,RA=True) + "}{" + \
          mysci.DecimaltoSeg(res['Dec'].value, RA=False) + "}{2}{}{" + \
          str(res['angsize']['major'].value) + " min}{}{}")
