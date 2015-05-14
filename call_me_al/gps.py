state = ['son-at-home', 'car-needs-battery', 'have-money', 'have-a-phone-book']

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
        'preconds': ['have-phone-book'],
        'add-list': ['know-phone-number'],
        'del-list': []},
    {'action': 'give-shop-money',
        'preconds': ['have-money'],
        'add-list': ['shop-has-money'],
        'del-list': ['have-money']}]

def GPS(goals):
    for goal in goals:
        achieve(goal)

def achieve(goal):
    return (goal in state) or apply_op(find_all_ops(goal))

def find_all_ops(goal):
    result = []
    for op in ops:
        if goal in op['add-list']:
            result.append(op)
    return result

def apply_op(ops):
    global state
    for op in ops:
        for goal in op['preconds']:
            if not achieve(goal):
                for d in op['del-list']:
                    try:
                        state.remove(d)
                    except ValueError:
                        pass
                for a in op['add-list']:
                    if a not in state:
                        state.append(a)

GPS(['son-at-school'])
print(state)
