#!/usr/bin/env python

import string
import random
import time
from pprint import pprint as pp

def print_cipher(ct):
    while ct:
        try:
            print "{:2d} {:2d} {:2d} {:2d} {:2d}".format(*ct[:row_length])
            ct[:row_length] = []
        except IndexError:
            print(ct)
            break

def add_nulls(cipher_text):
    padding = random.randint(4,10)
    nulls = row_length - ((len(cipher_text) + padding) % row_length) + padding
    for i in range(0, nulls):
        null = random.choice(map_range[alpha_len:])
        cipher_text.insert(random.randrange(len(cipher_text)+1), null)
    return cipher_text

def encode(plain):
    plain_text = ''.join(plain.split())
    cipher_text = []

    random.seed(time.time())
    for i, c in enumerate(plain_text.upper()):
        pos = alpha.find(c)
        if pos == -1:
            cipher_text.append(random.choice(map_range[alpha_len:]))
        else:
            # if we have more of the same character in a row we'll skip it
            next_c = None
            try:
                next_c = plain_text.upper()[i+1]
            except IndexError:
                pass
            if c == next_c:
                continue
            cipher_text.append(map_range[pos])

    return add_nulls(cipher_text)

def decode(cipher):
    cipher_text = cipher.split(' ')
    plain_text = ""
    for c in cipher_text:
        try:
            pos = map_range.index(int(c))
        except ValueError:
            continue
        try:
            plain_text += alpha[pos]
        except IndexError:
            pass
    return plain_text

def get_mapping():
    return zip(alpha, map_range)

alpha = string.ascii_uppercase + string.digits + string.punctuation
alpha_len = len(alpha)

map_range = range(0,100)
random.seed(100)
random.shuffle(map_range)

row_length = 5
column_width = 5

encode_mode = True

while True:
    text = raw_input("enter your text: ")
    if text == "exit":
        print("Thanks! Please come again")
        break
    elif text == "change mode":
        encode_mode = not encode_mode
        pass
    elif text == "show me the secret!":
        pp(get_mapping())
    elif text == "guess solution":
        print_cipher(encode("i know the secret"))
    elif text.upper() == "HELP":
        print("some available commands are:")
        print("change mode")
        print("exit")
    elif encode_mode:
        print_cipher(encode(text))
    elif not encode_mode:
        print(decode(text))
    else:
        print("I have no idea how to do that!")
