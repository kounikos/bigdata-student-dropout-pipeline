#!/usr/bin/env python

# import sys to read and write data to terminal
import sys

for line in sys.stdin:
    line = line.strip()
    words = line.split()

    for word in words:
        #write results to terminal, for input in reducer.py
        print (f"{word}\t{1}")
