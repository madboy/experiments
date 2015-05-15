#!/usr/bin/env python

state = ['son-at-home', 'car-needs-battery', 'have-money', 'have-a-phone-book']
#state = ['son-at-home', 'car-needs-battery', 'have-money']

ops = [{'action': 'drive-son-to-school',
        'preconds': ['son-at-home', 'car-works'],
        'add-list': ['son-at-school'],
        'del-list': ['son-at-home']},
    {'action': 'shop-installs-battery',
        'preconds': ['car-needs-battery', 'shop-knows-problem', 'shop-has-money'],
        'add-list': ['car-works'],
        'del-list': []},
    {'action': 'tell-shop-problem',
        'preconds': ['in-communication-with-shop'],
        'add-list': ['shop-knows-problem'],
        'del-list': []},
    {'action': 'telephone-shop',
        'preconds': ['know-phone-number'],
        'add-list': ['in-communication-with-shop'],
        'del-list': []},
    {'action': 'look-up-number',
        'preconds': ['have-a-phone-book'],
        'add-list': ['know-phone-number'],
        'del-list': []},
    {'action': 'give-shop-money',
        'preconds': ['have-money'],
        'add-list': ['shop-has-money'],
        'del-list': ['have-money']}]

def find_all_ops(goal):
    result = []
    for op in ops:
        if goal in op['add-list']:
            result.append(op)
    return result

def GPS(goals):
    print("we are trying to solve", goals)
    counter = 1
    for goal in goals:
        while not achieve(goal):
            if counter > 20:
                print("we cannot solve this within 20 steps")
                return
            print("trying again")
            counter += 1

def achieve(goal):
    # I'll achieve a goal by meeting all the preconditions
    print("Achieving", goal)
    if goal in state:
        print("We have achieved", goal)
        return True
    else:
        do_these = find_all_ops(goal)
        for op in do_these:
            do(op)

def do(op):
    global state
    if all(achieve(goal) == True for goal in op['preconds']):
        print("Executing", op['action'])
        for a in op['add-list']:
            if a not in state:
                state.append(a)
        for d in op['del-list']:
            try:
                state.remove(d)
            except ValueError:
                pass

GPS(['son-at-school'])
print(state)
