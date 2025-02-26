from finite_automaton import FiniteAutomaton
from grammar import Grammar


# Define the Grammar
vn = {"S", "A", "B"}
vt = {"a", "b"}
p = {
    "S": ["aA", "bB"],
    "A": ["aB", "b"],  # A is final, so it has an ε-production
    "B": ["bA"]
}
s = "S"

# Create Grammar object
grammar = Grammar(vn, vt, p, s)

# Classify grammar based on Chomsky Hierarchy
grammar_type = grammar.classify_chomsky_hierarchy()
print(f"Grammar Type: {grammar_type}")

print("\n" + "="*40 + "\n")

# Define Finite Automaton
states = {"S", "A", "B"}
alphabet = {"a", "b"}
transitions = {
    ("S", "a"): ["A", "B"],
    ("S", "b"): ["B"],
    ("A", "a"): ["B"],
    ("B", "b"): ["A"]
}
start_state = "S"
final_states = {"A"}

# Create FA object
finite_automaton = FiniteAutomaton(states, alphabet, transitions, start_state, final_states)

# Check if the FA is deterministic
if finite_automaton.is_deterministic():
    print("The given FA is a Deterministic Finite Automaton (DFA).")
else:
    print("The given FA is a Non-Deterministic Finite Automaton (NDFA).")

# Convert FA to Regular Grammar
regular_grammar = finite_automaton.to_regular_grammar()

print("\n" + "="*40 + "\n")

# Print converted Regular Grammar
print("Converted FA to Regular Grammar:")
print("VN (Non-terminals):", regular_grammar.vn)
print("VT (Terminals):", regular_grammar.vt)
print("Productions (P):")
for left, right in regular_grammar.p.items():
    formatted_right = [r if r != "" else "ε" for r in right]  # Replace empty string with ε
    print(f"  {left} -> {', '.join(formatted_right)}")
print("Start Symbol (S):", regular_grammar.s)

print("\n" + "="*40 + "\n")

# Example NFA
nfa_states = {"q0", "q1", "q2"}
alphabet = {"a", "b"}
nfa_transitions = {
    ("q0", "a"): ["q0", "q1"],
    ("q0", "b"): ["q2"],
    ("q1", "a"): ["q2"],
    ("q2", "b"): ["q1"]
}
start_state = "q0"
final_states = {"q2"}

nfa = FiniteAutomaton(nfa_states, alphabet, nfa_transitions, start_state, final_states)
print("Original NFA:")
nfa.display()

print("\n" + "="*40)

dfa = nfa.convert_nfa_to_dfa()
print("\nConverted DFA")
print("VN (Non-terminals):", {', '.join(['{' + ', '.join(q) + '}' for q in dfa.Q])})
print("VT (Terminals):", dfa.sigma)
print("Productions (P):")
for (state, symbol), next_states in dfa.delta.items():
    print(f"  (({', '.join(state)}), '{symbol}') -> {next_states}")
print("Start Symbol (S):", ', '.join(dfa.q0))
print("Final States:", {f'({', '.join(f)})' for f in dfa.F})