#!/usr/bin/env python

from collections import namedtuple

Step = namedtuple("Step", 'action,preconds,add_list,del_list')

steps = [Step('drive-son-to-school', ['son-at-home', 'car-works'], ['son-at-school'], ['son-at-home']),
        Step('shop-installs-battery', ['car-needs-battery', 'shop-knows-problem', 'shop-has-money'], ['car-works'], []),
        Step('tell-shop-problem', ['in-communication-with-shop'], ['shop-knows-problem'], []),
        Step('telephone-shop', ['know-phone-number'], ['in-communication-with-shop'], []),
        Step('look-up-number', ['have-a-phone-book'], ['know-phone-number'], []),
        Step('give-shop-money', ['have-money'], ['shop-has-money'], ['have-money'])]

state = ['son-at-home', 'car-needs-battery', 'have-money', 'have-a-phone-book']
#state = ['son-at-home', 'car-needs-battery', 'have-money']

def find_all_steps(goal):
    result = []
    for step in steps:
        if goal in step.add_list:
            result.append(step)
    return result

def GPS(goal):
    global state
    print("My goal is", goal)
    if goal in state:
        print("We have achieved", goal)
        return True
    nsteps = find_all_steps(goal)
    if len(nsteps) == 0:
        print("we have no way of achieving this")
    for step in nsteps:
        print("I need to do", step.action, "in order to reach my goal")
        if all(GPS(pc) == True for pc in step.preconds):
            for a in step.add_list:
                if a not in state:
                    state.append(a)
            for d in step.del_list:
                try:
                    state.remove(d)
                except ValueError:
                    pass
        else:
            for pc in step.preconds:
                GPS(pc)


GPS('son-at-school')
if 'son-at-school' in state:
    print('Solved')
print(state)
