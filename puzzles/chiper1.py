#!/usr/bin/env python

import string
import random
import time

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
    while ((len(cipher_text)+padding) % row_length) != 0:
        null = random.choice(map_range[alpha_len:])
        cipher_text.insert(random.randrange(len(cipher_text)+1), null)
        padding -= 1
        if padding < 0:
            padding = 0
    return cipher_text

def decode(cipher):
    cipher_text = cipher.split(' ')
    print("I will try to decipher this", cipher_text)

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
        print("mode is now %s" % ("encode" if encode else "decode"))
    elif text == "show secret":
        print(map_range)
    elif text == "guess solution":
        print_cipher(create_cipher("i know the secret"))
    else:
        print_cipher(create_cipher(plain_text))
