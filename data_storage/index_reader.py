#!/usr/bin/env python
import pickle
import sys


def index_reader(source, search):
    data = pickle.load(source)
    if search in data:
        print data.get(search)[-1]
    else:
        print ''


if __name__ == '__main__':
    source = sys.argv[1]
    search = sys.argv[2]
    with open(source, 'rb') as s:
        index_reader(s, search)