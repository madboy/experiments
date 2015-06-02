#!/usr/bin/env python

import string
import random
import time
from pprint import pprint as pp

def print_cipher(ct):
    counter = 1
    row = []
    for c in ct:
        row.append(str(c))
        if counter < row_length:
            counter += 1
        else:
            print("\t".join(row))
            counter = 1
            row = []
    print("\t".join(row))

def add_nulls(cipher_text):
    padding = random.randint(4,10)
    while len(cipher_text) < row_length or ((len(cipher_text)+padding) % row_length) != 0:
        null = random.choice(map_range[alpha_len:])
        cipher_text.insert(random.randrange(len(cipher_text)+1), null)
        padding -= 1
        if padding < 0:
            padding = 0
    return cipher_text

def encode(plain):
    plain_text = ''.join(plain.split())
    cipher_text = []

    random.seed(time.time())
    for c in plain_text.upper():
        pos = alpha.find(c)
        if pos == -1:
            cipher_text.append(random.choice(map_range[alpha_len:]))
        else:
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
    elif text == "show secret":
        pp(get_mapping())
    elif text == "guess solution":
        print_cipher(encode("i know the secret"))
    elif text == "help":
        print("some available commands are:")
        print("change mode")
        print("exit")
    elif encode_mode:
        print_cipher(encode(text))
    elif not encode_mode:
        print(decode(text))
    else:
        print("I have no idea how to do that!")
