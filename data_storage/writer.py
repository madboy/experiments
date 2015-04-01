#!/usr/bin/env python
import sys
import datetime
import random

users = ['Anna', 'Panna', 'Dregen', 'Apa', 'Lapa', 'Dapa', 'Dijon']
messages = ['hungry', 'content', 'happy', 'sad', 'glad', 'mad', 'drunk', 'skunker', 'sleepy', 'derpy', 'catter', 'hatter']

def certainty():
	return str(random.randint(1, 100))

def message():
	return random.choice(messages)

def writer(handle, lines):
    for i in range(lines):
        log_text = "%s %s %s %s\n" % (datetime.datetime.now(), random.choice(users), certainty(), message())
        handle.write(log_text)

if __name__ == '__main__':
    filename = sys.argv[1]
    count = int(sys.argv[2])
    with open(filename, 'a') as f:
        writer(f, count)
