#!/usr/bin/env python
import pickle
import sys
from collections import defaultdict

valid_indices = ['date', 'name', 'certainty', 'message']
idx = defaultdict(list)


def get_key(index, line):
    cols = line.split(' ')
    row = {'date': ' '.join(cols[0:2]),
           'name': cols[2],
           'certainty': cols[3],
           'message': cols[4]}
    index_key = row[index]
    return index_key


def indexer(source, index):
    if index in valid_indices:
        index_file = "%s_%s.idx" % (index, 'index')
        with open(index_file, 'wb') as i:
            for line in source.readlines():
                line = line.strip()
                index_key = get_key(index, line)
                idx[index_key].append(line)
            pickle.dump(idx, i)
            print("The pickling has been done")
    else:
        print("Invalid index key given")


if __name__ == '__main__':
    filename = sys.argv[1]
    index = sys.argv[2]
    with open(filename, 'rb') as f:
        indexer(f, index)