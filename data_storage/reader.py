#!/usr/bin/env python
import sys

def reader(source, search):
	for l in source.readlines():
		if search in l:
			print(l.strip())

if __name__ == '__main__':
    filename = sys.argv[1]
    search = sys.argv[2]
    with open(filename, 'rb') as f:
        reader(f, search)
