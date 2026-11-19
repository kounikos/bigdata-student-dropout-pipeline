#!/usr/bin/env python

# import sys to read and write data to terminal
import sys

keywords = ("weather", "forecast", "shiny", "rainy", "temperature")

for line in sys.stdin:
    line = line.strip()
    words = line.split()

    for word in words:
        #write results to terminal, if the word is one of our keywords
        if word in keywords:
            print (f"{word}\t{1}")