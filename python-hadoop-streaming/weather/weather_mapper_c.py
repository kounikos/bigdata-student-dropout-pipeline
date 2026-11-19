#!/usr/bin/env python

# import sys to read and write data to terminal
import sys


# skip the first line (headers)
next(sys.stdin)

for line in sys.stdin:
    # make sure a line exists after skipping first one, or abort
    if not line:
        break
    line = line.strip()
    columns = line.split(',')
    for i, column in enumerate(columns):
        if i == 1:
            #write results to terminal, for input in reducer.py
            print (f"{column}\t{1}")
