#!/usr/bin/env python

from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None

for line in sys.stdin:
    line = line.strip()
    # split on tab
    word, count = line.split("\t", 1)
    # convert count to int
    try:
        count = int(count)
    except ValueError:
        continue

    if current_word == word:
        current_count += count
    else:
        if current_word:
            print '{}\t{}'.format(current_word, current_count)
        current_count = count
        current_word = word

# output last word
if current_word == word:
    print '{}\t{}'.format(current_word, current_count)
