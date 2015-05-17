#!/usr/bin/env python

from collections import namedtuple

Step = namedtuple("Step", 'action,preconds,add_list,del_list')

steps = [Step('drive-son-to-school', ['son-at-home', 'car-works'], ['son-at-school'], ['son-at-home']),
        Step('shop-installs-battery', ['car-needs-battery', 'shop-knows-problem', 'shop-has-money'], ['car-works'], []),
        Step('tell-shop-problem', ['in-communication-with-shop'], ['shop-knows-problem'], []),
        Step('telephone-shop', ['know-phone-number'], ['in-communication-with-shop'], []),
        Step('look-up-number', ['have-a-phone-book'], ['know-phone-number'], []),
        Step('give-shop-money', ['have-money'], ['shop-has-money'], ['have-money'])]

#state = ['son-at-home', 'car-needs-battery', 'have-money', 'have-a-phone-book']
state = ['son-at-home', 'car-needs-battery', 'have-money']

def find_all_steps(goal):
    result = []
    for step in steps:
        if goal in step.add_list:
            result.append(step)
    return result

def GPS2(goal):
    global state
    print("My goal is", goal)
    if goal in state:
        print("We have achieved", goal)
        return True
    nsteps = find_all_steps(goal)
    if len(nsteps) == 0:
        print("******* we have no way of achieving this", goal)
        return False
    for step in nsteps:
        print("I need to do", step.action, "in order to reach my goal")
        if all(GPS(pc) == True for pc in step.preconds):
            state = set().union(*[state, step.add_list])
            state = state - set(step.del_list)
            return True
        else:
            for pc in step.preconds:
                GPS(pc)

def get_all_steps(goal, results = []):
    result = []
    for step in steps:
        if goal in step.add_list:
            result.append(step)
    if result == []:
        return results
    else:
        results.append(result)
        for step in result:
            for pc in step.preconds:
                results.append(get_all_steps(pc, results))
    return results

def achieve(goal):
    if goal in state:
        return True

def get_actions(actions):
    result = []
    for a in actions:
        if type(a) == list:
            pass
        else:
            result.append(a)
    return result

def flatten_list(l):
    return sum(l, [])

def GPS(goal):
    global state
    all_steps = get_all_steps(goal)
    all_steps = flatten_list(all_steps)
    all_steps = get_actions(all_steps)
    al = []
    for step in all_steps:
        al.append(step.add_list)
    al = flatten_list(al)
    print(al)
    possible_outcomes = []
    for step in all_steps:
        if all(pc in al for pc in step.preconds):
            possible_outcomes.append(step.add_list)
            #print("horray, we can do", step.action)
    print(possible_outcomes)
    possible_outcomes = flatten_list(possible_outcomes)
    if goal in possible_outcomes:
        print("Hell YEAH, we can solve this")
    else:
        print("UNPossible")
    #for step in all_steps:
        #if type(step) == list:
            #pass
        #else:
            #if all(achieve(pc) == True for pc in step.preconds):
                #state = set().union(*[state, step.add_list])
                #state = state - set(step.del_list)

goal = 'son-at-school'
#while GPS(goal):
#    if goal in state:
#        break
#    print "we're doing it"
#print(state)
print(state)
GPS(goal)
print(state)
