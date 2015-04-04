#!/usr/bin/env python
import sys
import datetime
import random
import time

users = ['Anna', 'Panna', 'Dregen', 'Apa', 'Lapa', 'Dapa', 'Dijon']
messages = ['hungry', 'content', 'happy', 'sad', 'glad', 'mad', 'drunk', 'skunker', 'sleepy', 'derpy', 'catter',
            'hatter']


def certainty():
    return str(random.randint(1, 100))


def message():
    return random.choice(messages)


def writer(handle, lines, s=0):
    for i in range(lines):
        time.sleep(s)
        log_text = "%s\t%s\t%s\t%s\n" % (datetime.datetime.now(), random.choice(users), certainty(), message())
        handle.write(log_text)
        handle.flush()


if __name__ == '__main__':
    filename = sys.argv[1]
    count = int(sys.argv[2])
    s = 0
    if len(sys.argv) > 3:
        s = float(sys.argv[3])
    with open(filename, 'a') as f:
        writer(f, count, s)
