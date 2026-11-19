#!/usr/bin/env python

# import sys to read and write data to terminal
import sys

current_column = None
current_count = 0
column = None


for line in sys.stdin:
    line = line.strip()
    # split on tab
    column, count = line.split("\t", 1)
    # convert count to int
    try:
        count = int(count)
    except ValueError:
        continue

    if current_column == column:
        current_count += count
    else:
        if current_column:
            print(f"{current_column}\t{current_count}")
        current_count = count
        current_column = column

# output last column  
if current_column == column:
    print(f"{current_column}\t{current_count}")
