class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.Q = states
        self.sigma = alphabet
        self.delta = {}  # Dictionary to hold transitions as lists
        self.q0 = start_state
        self.F = final_states

        # Ensure transitions are stored as lists (for NDFA support)
        for (state, symbol), next_states in transitions.items():
            if (state, symbol) not in self.delta:
                self.delta[(state, symbol)] = []
            self.delta[(state, symbol)].extend(next_states)

    def to_regular_grammar(self):
        from grammar import Grammar
        vn = self.Q
        vt = self.sigma
        p = {}

        # Convert transitions to production rules
        for (state, symbol), next_states in self.delta.items():
            if state not in p:
                p[state] = []
            for next_state in next_states:
                p[state].append(symbol + next_state)

        # Add epsilon transitions for final states
        for final_state in self.F:
            if final_state not in p:
                p[final_state] = []
            p[final_state].append("")

        return Grammar(vn, vt, p, self.q0)

    def is_deterministic(self):
        for (state, symbol), next_states in self.delta.items():
            if len(next_states) > 1:  # More than one transition for (state, symbol)
                return False
            if symbol == "":
                return False
        return True

    def convert_nfa_to_dfa(self):
        dfa_states = []
        dfa_transitions = {}
        dfa_start_state = frozenset([self.q0])
        dfa_states.append(dfa_start_state)
        unprocessed_states = [dfa_start_state]
        dfa_final_states = set()

        while unprocessed_states:
            current_state = unprocessed_states.pop()
            for symbol in self.sigma:
                next_state = set()
                for nfa_state in current_state:
                    if (nfa_state, symbol) in self.delta:
                        next_state.update(self.delta[(nfa_state, symbol)])
                next_state = frozenset(next_state)

                if next_state:
                    if next_state not in dfa_states:
                        dfa_states.append(next_state)
                        unprocessed_states.append(next_state)
                    dfa_transitions[(current_state, symbol)] = next_state

                    if any(state in self.F for state in next_state):
                        dfa_final_states.add(next_state)

        return FiniteAutomaton(
            states=dfa_states,
            alphabet=self.sigma,
            transitions=dfa_transitions,
            start_state=dfa_start_state,
            final_states=dfa_final_states,
        )

    def display(self):
        print("States:", self.Q)
        print("Alphabet:", self.sigma)
        print("Transitions:")
        for (state, symbol), next_states in self.delta.items():
            print(f"  ({state}, '{symbol}') -> {next_states}")
        print("Start State:", self.q0)
        print("Final States:", self.F)