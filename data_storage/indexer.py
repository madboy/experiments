#!/usr/bin/env python
import pickle
import sys

valid_indices = ['date', 'name', 'certainty', 'message']


def indexer(source, index):
    if valid_indices.count(index):
        index_file = "%s_%s.idx" % (index, 'index')
        with open(index_file, 'wb') as i:
            idx = {}
            for line in source.readlines():
                cols = line.split(' ')
                row = {'date': ' '.join(cols[0:2]),
                       'name': cols[2],
                       'certainty': cols[3],
                       'message': cols[4].rstrip()}
                index_key = row[index]
                if idx.get(index_key):
                    idx[index_key].append(line.strip())
                else:
                    idx[index_key] = [line.strip()]
            pickle.dump(idx, i)
            i.close()
            print("The pickling has been done")
    else:
        print("Invalid index key given")


if __name__ == '__main__':
    filename = sys.argv[1]
    index = sys.argv[2]
    with open(filename, 'rb') as f:
        indexer(f, index)