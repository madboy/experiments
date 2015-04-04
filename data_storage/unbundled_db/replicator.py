#!/usr/bin/env python
import json
import sys

name_view = {}
message_view = {}
views = {"name": name_view, "message": message_view}
view_files = {"name": 'name_view.idx', "message": 'message_view.idx'}
valid_indices = {'date': 0, 'name': 1, 'certainty': 2, 'message': 3}
commit_size = 0

def get_key(col_nbr, line):
    cols = line.split('\t')
    index_key = cols[col_nbr]
    return index_key

def replication(commit_log):
    """push data from the writer to the view"""
    global commit_size
    local_commit_log = commit_log
    length = len(local_commit_log)
    diff = length - commit_size
    if diff != 0:
        for row in local_commit_log[-diff:]:
            for k, view in views.iteritems():
                vk = get_key(valid_indices[k], row)
                view[vk] = row
                with open(view_files[k], 'wb') as vf:
                    json.dump(view, vf)
        commit_size = length
    else:
        print("no updates for me to look at")

if __name__ == '__main__':
    log = sys.argv[1]
    with open(log, 'rb') as cl:
        replication(cl.readlines())
