def fsm_from_dict(dictionary):
    states = {name: {} for name in dictionary}
    for name, transitions in dictionary.items():
        state = states[name]
        for symbol, next_name in transitions.items():
            state[symbol] = states[next_name]
    return states

def fsm_from_tuples(tuples):
    states = {name: {} for name, _, _ in tuples}
    for cur_name, symbol, next_name in tuples:
        states[cur_name][symbol] = states[next_name]
    return states

class FSM(object):
    def __init__(self, initial, rules, final, callbacks=()):
        if isinstance(rules, dict):
            self.states = fsm_from_dict(rules)
        elif isinstance(rules, list):
            self.states = fsm_from_tuples(rules)

        self.state = self.states[initial]
        self.final = set(id(self.states[name]) for name in final)
        self.callbacks = {id(self.states[name]): fn for name, fn in callbacks}

    def feed(self, symbol):
        self.state = self.state[symbol]
        s = id(self.state)
        if s in self.callbacks:
            self.callbacks[s]()
        return self

    def is_final(self):
        return id(self.state) in self.final


if __name__ == '__main__':
    test_dict = {'q0': {0: 'q0', 1: 'q1'}, 'q1': {0: 'q0', 1: 'q1'}}
    test_tuples = [('q0', 0, 'q0'), ('q0', 1, 'q1'),
                   ('q1', 0, 'q0'), ('q1', 1, 'q1')]

    f = FSM('q0', test_dict, ['q1'])
    print f.feed(0).feed(0).feed(1).is_final()
