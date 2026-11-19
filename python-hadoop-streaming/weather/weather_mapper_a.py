#!/usr/bin/env python

# import sys to read and write data to terminal
import sys


# skip the first line (headers)
next(sys.stdin)

for line in sys.stdin:
    # # make sure a line exists after skipping first one, or abort
    # if not line:
    #     break
    line = line.strip()
    columns = line.split(',')
    try:
        if columns[21] == "Yes":
            #write results to terminal, for input in reducer.py
            print (f"RainTomorrow\t{1}")
    except TypeError:
        continue
