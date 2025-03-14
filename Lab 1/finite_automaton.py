class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.Q = states
        self.sigma = alphabet
        self.delta = transitions
        self.q0 = start_state
        self.F = final_states

    def string_belongs_to_language(self, input_string):
        current_state = self.q0
        for char in input_string:
            if (current_state, char) in self.delta:
                current_state = self.delta[(current_state, char)]
            else:
                return False
        return current_state in self.F