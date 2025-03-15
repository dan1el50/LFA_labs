# Laboratory work nr. 3 - Lexer & Scanner
### Course: Formal Languages & Finite Automata
### Author: Cojocaru Daniel

----
# Theory

## *Lexer*
Lexical analysis is the first phase of a compiler and is responsible for breaking an input text (such as a source code file) into meaningful lexical tokens. This process is performed by a lexer (also called a scanner or tokenizer). The lexer reads a sequence of characters and groups them into lexemes, which are then categorized into tokens.

## Chomsky Hierarchy of Grammars
1. **Type 0 (Unrestricted Grammars)** – Productions: α → β, where α and β are any sequences of terminals and non-terminals.
2. **Type 1 (Context-Sensitive Grammars)** – Productions: |α|<= |β|.
3. **Type 2 (Context-Free Grammars)** – Productions: A → β, where A is a non-terminal, and β is any combination of terminals and non-terminals.
4. **Type 3 (Regular Grammars)** – Productions: A → aB or A → a, where a is a terminal and B is a non-terminal.
## Objectives:
1. Understand what an automaton is and what it can be used for.
2. Continuing the work in the same repository and the same project, the following need to be added:
   - Provide a function in your grammar type/class that could classify the grammar based on Chomsky hierarchy.
   - For this you can use the variant from the previous lab.
3. According to your variant number (by universal convention it is register ID), get the finite automaton definition and do the following tasks:
   - Implement conversion of a finite automaton to a regular grammar.
   -  Determine whether your FA is deterministic or non-deterministic.
   -  Implement some functionality that would convert an NDFA to a DFA.
   -  Represent the finite automaton graphically (Optional, and can be considered as a bonus point):

You can use external libraries, tools or APIs to generate the figures/diagrams.
Your program needs to gather and send the data about the automaton and the lib/tool/API return the visual representation.


# Implementation description
## **1.Finite Automaton*
### *Finite Automaton Constructor*
```
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
```
It first assigns the fundamental elements:
- `self.Q` stores the set of states.
- `self.sigma` holds the input alphabet (set of symbols).
- `self.delta` is initialized as an empty dictionary to store transitions.
- `self.q0` represents the start state.
- `self.F` contains the set of final (accepting) states.

Then, the method processes the transition function by looping through the given transitions dictionary. If a `(state, symbol)` pair is not yet in `self.delta`, it initializes an empty list. The `.extend(next_states)` method then adds the possible next states for that transition. This ensures that multiple transitions can exist for the same `(state, symbol)` pair, allowing support for non-deterministic finite automata (NDFA).

### *To Regular Grammar*
```
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
```

The `to_regular_grammar` method converts a finite automaton into an equivalent regular grammar. The method iterates through the transition function of the automaton. For each transition, it checks whether the current state is already in `p.` If not, it initializes an empty list. Then, for each next state, it constructs a production rule where the input symbol is followed by the next state and adds it to the list of productions for the current state. Finally, the method ensures that final states include epsilon (ε) transitions. It loops through all final states, initializes an empty production list if necessary, and appends an empty string to represent ε. The constructed grammar is then returned as a `Grammar` object using the extracted components.

### *Is Deterministic*
```
    def is_deterministic(self):
        for (state, symbol), next_states in self.delta.items():
            if len(next_states) > 1:  # More than one transition for (state, symbol)
                return False
            if symbol == "": 
                return False
        return True
```

The `is_deterministic` method checks whether the finite automaton is deterministic. It iterates through the transition function and examines each `(state, symbol)` pair. If a transition leads to more than one possible next state, the automaton is non-deterministic, so the method immediately returns `False`. Additionally, if an epsilon (ε) transition is found, meaning a transition occurs without consuming an input symbol, the method also returns `False`. If neither condition is met throughout the loop, the automaton is deterministic, and the method returns `True`.

### *Convert NFA to DFA*
```
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
```

The `convert_nfa_to_dfa` method transforms a non-deterministic finite automaton (NFA) into an equivalent deterministic finite automaton (DFA) using the subset construction algorithm. The method then enters a loop, processing each unprocessed DFA state. For each input symbol in the alphabet, it determines the set of reachable NFA states by iterating over all states in the current DFA state. If a transition exists, the corresponding next states are added to a new set. This set is converted into a frozenset to ensure consistency and uniqueness. If the computed next state is non-empty and hasn't been processed yet, it is added to the DFA state list and the queue for further processing. The computed transition is then stored in the DFA transition dictionary. Additionally, if any of the states in the computed next state belong to the NFA's final states, the entire state set is marked as a final state in the DFA. Finally, the method returns a new `FiniteAutomaton` instance representing the resulting DFA, with the constructed states, transitions, start state, and final states.

## *2.Grammar Class*
### *Grammar Constructor*
```
class Grammar:
    def __init__(self, vn, vt, p, start_symbol):
        self.vn = vn
        self.vt = vt
        self.p = p
        self.s = s
```

This constructor initializes a grammar by defining its core components:
- vn: Non-terminals (used to derive strings).
- vt: Terminals (the actual symbols of the language).
- p: Production rules mapping non-terminals to valid replacements.
- start_symbol: The entry point for generating strings.

## *Chomsky Hierarchy*
```
    def classify_chomsky_hierarchy(self):
        is_regular = True
        is_context_free = True
        is_context_sensitive = True

        for left, right in self.p.items():
            for production in right:
                # Check Type 3 (Regular Grammar)
                if not (len(left) == 1 and left in self.vn and
                        (len(production) == 1 and production[0] in self.vt or
                         len(production) == 2 and production[0] in self.vt and production[1] in self.vn)):
                    is_regular = False

                # Check Type 2 (Context-Free Grammar)
                if len(left) > 1:
                    is_context_free = False

                # Check Type 1 (Context-Sensitive Grammar)
                if len(left) > len(production):
                    is_context_sensitive = False

        if is_regular:
            return "Type 3: Regular Grammar"
        elif is_context_free:
            return "Type 2: Context-Free Grammar"
        elif is_context_sensitive:
            return "Type 1: Context-Sensitive Grammar"
        else:
            return "Type 0: Unrestricted Grammar"
```

The classify_chomsky_hierarchy method determines the type of grammar based on the Chomsky hierarchy. It starts by assuming the grammar satisfies all three main types: regular (Type 3), context-free (Type 2), and context-sensitive (Type 1), then analyzes each production rule to check its structure. 
- A grammar is regular if each rule follows either A → a or A → aB, where A is a non-terminal, a is a terminal, and B is another non-terminal. If any rule does not match this pattern, the grammar is not regular.
- It is context-free if each production has a single non-terminal on the left-hand side. If any rule has multiple symbols on the left, the grammar is not context-free.
- For context-sensitive grammars, the left-hand side of each production must not be longer than the right-hand side. If any rule violates this, the grammar is not context-sensitive.

The method then returns the most restrictive classification that still holds, assigning Type 3 (Regular) if possible, then Type 2 (Context-Free), then Type 1 (Context-Sensitive), and finally Type 0 (Unrestricted Grammar) if none of the conditions are met.

## *3.Main*
```
from finite_automaton import FiniteAutomaton
from grammar import Grammar
# Define the Grammar
vn = {"S", "A", "B"}
vt = {"a", "b"}
p = {
    "S": ["aA", "bB"],
    "A": ["aB", "b"],
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
```

The main.py script defines a grammar and a finite automaton (FA), then performs multiple operations to analyze and transform them. 
- First, it initializes a grammar with a set of non-terminals, terminals, and production rules, then classifies it according to the Chomsky hierarchy.
- Next, it defines an FA, checks whether it is deterministic (DFA) or non-deterministic (NDFA), and converts it into an equivalent regular grammar.
- Lastly, an NFA is defined and displayed before being converted into a DFA using the subset construction algorithm. The resulting DFA is printed along with its transitions and final states.

The script provides a structured demonstration of automata theory concepts, including FA to grammar conversion and NFA to DFA transformation.

## Conclusions / Screenshots / Results
![image](https://github.com/user-attachments/assets/7aada380-8d64-4f6e-a94b-6ddb8044c333)
![image](https://github.com/user-attachments/assets/1ef536fd-0c44-4a8a-a069-8e1ed2b2e63c)

# Conclusion
In this lab, I explored finite automata, determinism, and formal grammars, applying these concepts through practical implementations. I classified a given grammar using Chomsky’s hierarchy, analyzed whether a finite automaton was deterministic or non-deterministic, and converted an NFA into a DFA using the subset construction algorithm. I also transformed an FA into a regular grammar, reinforcing the connection between automata and formal languages. By converting non-deterministic automata into deterministic ones, I ensured a more structured and predictable model, which is essential for applications like parsing and compiler design. This lab helped me better understand automata theory and its real-world applications.

## References
https://www.geeksforgeeks.org/conversion-from-nfa-to-dfa/

https://www.youtube.com/watch?v=jMxuL4Xzi_A
