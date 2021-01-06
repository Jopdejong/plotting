#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plotbase import webplot

import argparse



parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-i", "--input-dirs",default=[], nargs="+",
			help="input directories to create a webplot site")
parser.add_argument("-d", "--date",default=False, action="store_true",
			help="store date in the output sitedirectory")

args = parser.parse_args()

print args.input_dirs
for input_dir in args.input_dirs: 
	webplot.webplot(input_dir, recursive=True,copy=True, nodate=args.date)
