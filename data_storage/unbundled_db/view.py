#!/usr/bin/env python
import sys
import json

def view(name, search):
    """all reads use the view

    the view is populated automatically by
    the replication stream.

    the view itself does not care how the data
    ended up there.
    """
    current_view = json.loads(name.read())
    print current_view.get(search)

if __name__ == '__main__':
    view_file = sys.argv[1]
    search = sys.argv[2]
    with open(view_file) as vf:
        view(vf, search)
