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

    # keep count of temps + index
    for i, column in enumerate(columns):
        if i == 1:
            temp = float(column)
        
        if i == 2:
            temp += float(column)
            
    avg_temp = temp / 2

    #after assign to proper group, write results to terminal, for input in reducer.py
    if avg_temp >= 10 and avg_temp <= 20:
        print(f"[10,20]\t{1}")
    elif avg_temp >= 21 and avg_temp <= 30:
        print(f"[21,30]\t{1}")
    elif avg_temp >= 31 and avg_temp <= 40:
        print(f"[31,40]\t{1}")