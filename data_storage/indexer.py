#!/usr/bin/env python
import pickle
import sys
from collections import defaultdict

valid_indices = {'date': 0, 'name': 1, 'certainty': 2, 'message': 3}
idx = defaultdict(list)


def get_key(col_nbr, line):
    cols = line.split('\t')
    index_key = cols[col_nbr]
    return index_key


def indexer(source, index_key):
    if index_key in valid_indices:
        index_file = "%s_%s.idx" % (index_key, 'index')
        col_nbr = valid_indices[index_key]
        with open(index_file, 'wb') as i:
            for line in source.readlines():
                line = line.strip()
                index_key = get_key(col_nbr, line)
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