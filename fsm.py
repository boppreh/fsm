def fsm_from_dict(dictionary):
    states = {name: {} for name in dictionary}
    for name, transitions in dictionary.items():
        state = states[name]
        for symbol, next_name in transitions.items():
            state[symbol] = states[next_name]
    return states

q0 = fsm_from_dict({'q0': {0: 'q0', 1: 'q1'},
                    'q1': {0: 'q0', 1: 'q1'}})['q0']

print q0[0][0][1][1][0] == q0
