import random
from finite_automaton import FiniteAutomaton


class Grammar:
    def __init__(self, vn, vt, p, s):
        self.vn = vn
        self.vt = vt
        self.p = p
        self.s = s

    def generate_string(self):
        current_string = self.s
        while True:
            found_non_terminal = False
            for symbol in current_string:
                if symbol in self.vn:
                    replacement = random.choice(self.p.get(symbol, [symbol]))
                    current_string = current_string.replace(symbol, replacement, 1)
                    found_non_terminal = True
                    break
            if not found_non_terminal:
                break
        return current_string

    def generate_n_strings(self, n=5):
        return [self.generate_string() for _ in range(n)]

    def to_finite_automaton(self):
        transitions = {}
        for left_side, replacements in self.p.items():
            for replacement in replacements:
                if len(replacement) > 1:
                    next_state = replacement[1]
                else:
                    next_state = None
                transitions[(left_side, replacement[0])] = next_state
        return FiniteAutomaton(set(self.vn), self.vt, transitions, self.s, {None})