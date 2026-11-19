#!/usr/bin/env python

# import sys to read and write data to terminal
import sys

current_range = None
current_count = 0
t_range = None


for line in sys.stdin:
    line = line.strip()
    # split on tab
    t_range, count = line.split("\t", 1)
    # convert count to int
    try:
        count = int(count)
    except ValueError:
        continue

    if current_range == t_range:
        current_count += count
    else:
        if current_range:
            print(f"{current_range}\t{current_count}")
        current_count = count
        current_range = t_range

# output last one
if current_range == t_range:
    print(f"{current_range}\t{current_count}")
