def get_number(word, m):
    n = ""
    for c in word:
        n += str(m[c])
    return int(n)

alphametic = "send+more=money"
mapping = {'d':1, 'e':1, 'm':1, 'n':1, 'o':1, 'r':1, 's':1, 'y':1}

lhs, money = alphametic.split('=')
send, more = lhs.split('+')



ordered = sorted(mapping.keys())

while True:
    for c in ordered:
        guess = raw_input("%s?: " % c)
        mapping[c] = guess

    answer = get_number(send, mapping) + get_number(more, mapping)

    if answer == get_number(money, mapping):
        print("Execellent, the solution is", mapping)
        break
    else:
        print("try again")
