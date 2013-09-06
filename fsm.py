def rules_from_dict(dictionary):
    states = {name: {} for name in dictionary}
    for name, transitions in dictionary.items():
        state = states[name]
        for symbol, next_name in transitions.items():
            state[symbol] = states[next_name]
    return states

def rules_from_tuples(tuples):
    states = {name: {} for name, _, _ in tuples}
    for cur_name, symbol, next_name in tuples:
        states[cur_name][symbol] = states[next_name]
    return states

class FSM(object):
    def __init__(self, initial, rules, final, callbacks=()):
        if isinstance(rules, dict):
            self.states = rules_from_dict(rules)
        elif isinstance(rules, list):
            self.states = rules_from_tuples(rules)

        self.initial = self.states[initial]
        self.state = self.initial
        self.final = set(id(self.states[name]) for name in final)
        self.callbacks = {id(self.states[name]): fn for name, fn in callbacks}

    def feed(self, *symbols):
        for symbol in symbols:
            self.state = self.state[symbol]
            s = id(self.state)
            if s in self.callbacks:
                self.callbacks[s]()

    def is_final(self):
        return id(self.state) in self.final

    def reset(self):
        self.state = self.initial


if __name__ == '__main__':
    test_dict = {'q0': {0: 'q0', 1: 'q1'}, 'q1': {0: 'q0', 1: 'q1'}}
    test_tuples = [('q0', 0, 'q0'), ('q0', 1, 'q1'),
                   ('q1', 0, 'q0'), ('q1', 1, 'q1')]

    f = FSM('q0', test_dict, ['q1'])
    f.feed(0, 0, 1)
    print f.is_final()
