#!/usr/bin/env python
import sys
from collections import defaultdict
import json

valid_indices = {'date': 0, 'name': 1, 'certainty': 2, 'message': 3}
idx = defaultdict(list)

def get_key(col_nbr, line):
    cols = line.split('\t')
    index_key = cols[col_nbr]
    return index_key


def indexer(source, index_key):
    if index_key in valid_indices:
        index_file = "%s_%s.idx" % (index_key, 'jsonindex')
        col_nbr = valid_indices[index_key]
        with open(index_file, 'wb') as i:
            for line in source.readlines():
                line = line.strip()
                index_key = get_key(col_nbr, line)
                idx[index_key].append(line)
            json.dump(dict(idx), i)
            print("Index has been created")
    else:
        print("Invalid index key given")


if __name__ == '__main__':
    source_file = sys.argv[1]
    index = sys.argv[2]
    with open(source_file, 'rb') as s:
        indexer(s, index)
