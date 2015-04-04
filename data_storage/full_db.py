#!/usr/bin/env python
import datetime
import random
from pprint import pprint as pp

commit_log = []
commit_size = 0
name_view = {}
message_view = {}
views = {"name": name_view, "message": message_view}

valid_indices = {'date': 0, 'name': 1, 'certainty': 2, 'message': 3}

users = ['Anna', 'Panna', 'Dregen', 'Apa', 'Lapa', 'Dapa', 'Dijon']
messages = ['hungry', 'content', 'happy', 'sad', 'glad', 'mad', 'drunk', 'skunker', 'sleepy', 'derpy', 'catter',
            'hatter']


def certainty():
    return str(random.randint(1, 100))


def message():
    return random.choice(messages)


def writer():
    """append only writer

    writes everything to a commit_log
    """
    log_text = "%s\t%s\t%s\t%s\n" % (datetime.datetime.now(), random.choice(users), certainty(), message())
    commit_log.append(log_text)

def view(name, search):
    """all reads use the view

    the view is populated automatically by
    the replication stream.

    the view itself does not care how the data
    ended up there.
    """
    current_view = views.get(name)
    return current_view.get(search)

def get_key(col_nbr, line):
    cols = line.split('\t')
    index_key = cols[col_nbr]
    return index_key

def replication():
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
        commit_size = length
    else:
        print("no updates for me to look at")


if __name__ == '__main__':
    for i in range(10):
        writer()

    pp(commit_log)

    replication()

    pp(name_view)
    pp(message_view)

    pp(view('name', 'Anna'))
    pp(view('message', 'superunsad'))

    for i in range(10):
        writer()

    replication()

    pp(name_view)
    pp(message_view)

    pp(view('name', 'Anna'))
    pp(view('message', 'superunsad'))
