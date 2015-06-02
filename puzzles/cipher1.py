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

def create_cipher(plain):
    plain_text = ''.join(plain.split())
    cipher_text = []

    random.seed(time.time())
    for c in plain_text.upper():
        pos = alpha.find(c)
        if pos == -1:
            cipher_text.append(random.choice(map_range[alpha_len:]))
        else:
            cipher_text.append(map_range[pos])

    padding = random.randint(4,10)
    while len(cipher_text) < 5 or ((len(cipher_text)+padding) % row_length) != 0:
        null = random.choice(map_range[alpha_len:])
        cipher_text.insert(random.randrange(len(cipher_text)+1), null)
        padding -= 1
        if padding < 0:
            padding = 0
    return cipher_text

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

encode = True

while True:
    text = raw_input("enter your text: ")
    if text == "exit":
        print("Thanks! Please come again")
        break
    elif text == "change mode":
        encode = not encode
        pass
    elif text == "show secret":
        pp(get_mapping())
    elif text == "guess solution":
        print_cipher(create_cipher("i know the secret"))
    elif text == "help":
        print("some available commands are:")
        print("change mode")
        print("exit")
    elif encode:
        print_cipher(create_cipher(text))
    elif not encode:
        print(decode(text))
    else:
        print("I have no idea how to do that!")
