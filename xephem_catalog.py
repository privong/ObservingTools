#!/usr/bin/env python
#
# xephem_catalog.py
#
# Take a csv or tsv catalog and convert it into an xephem .edb catalog
#
# Copyright (c) 2015–2016,2018 George C. Privon

import numpy as np
import argparse
import datetime


parser = argparse.ArgumentParser(description='Convert a csv or tsv catalog \
                                              into an xephem edb catalog.')
parser.add_argument('catalog', type=str, help='Input catalog')
parser.add_argument('--output', '-o', type=str, default=None,
                    help='Output file. If not specified, input name will be \
                          used with edb suffix.')
parser.add_argument('--objtype', '-t', type=str, default='f',
                    help='Object type. See http://www.clearskyinstitute.com/xephem/help/xephem.html#mozTocId468501')
parser.add_argument('--s2a', type=str, default=' ',
                    help='Subfield 2A, if objtype is "f".')
parser.add_argument('--s2b', type=str, default=None,
                    help='Subfield 2B, if objtype is "f".')
parser.add_argument('--cols','-c', type=str, default=None,
                    help='Columns to use for name, RA, Dec, magnitude')
parser.add_argument('--equinox', '-e', type=str, default='2000',
                    help='Equinox of coordinates. 2000 (default) or 1950.')
parser.add_argument('--srcprefix', type=str, default=None,
                    help='Add a prefix to the source name.')
args = parser.parse_args()

data = open(args.catalog)

if args.output is None:
    args.output = args.catalog.rsplit('.', 1)[0] + '.edb'
if args.cols is None:
    args.cols = (0, 1, 2, 3)
else:
    args.cols = [int(x) for x in args.cols.split(',')]

outf = open(args.output, 'w')
outf.write('# edb catalog generated automatically from ' + args.catalog + '\n')
outf.write('# Generated at ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '.\n')

srcprefix = ''
comments = 0
for i,entry in enumerate(data):
    if entry[0] == '#' or entry[0] == '!':
        comments += 1
        continue
    entry = entry.split(',')
    if len(entry) > 0:
        if args.srcprefix == 'SOAR':
            srcprefix = '[{0:1d}]'.format(i-comments)
        outf.write(srcprefix + entry[args.cols[0]].rstrip('\n') + ',')
        outf.write('f|G,')
        outf.write(entry[args.cols[1]].rstrip('\n') + ',')
        outf.write(entry[args.cols[2]].rstrip('\n') + ',')
        try:
            outf.write(entry[args.cols[3]].rstrip('\n') + ',')
        except:
            outf.write('6,')
        outf.write(args.equinox + '\n')

outf.close()
