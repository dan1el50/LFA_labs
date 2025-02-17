# Laboratory work nr. 1 - Regular grammars
### Course: Formal Languages & Finite Automata
### Author: Cojocaru Daniel

----

## **Theory**
Formal languages are the foundation for many areas in computer science. They provide the means to rigorously define syntax and structure for both programming and natural languages. A formal language is built using several components:
- **Alphabet:** A finite set of symbols.
- **Vocabulary:** The set of strings (words) that can be formed from the alphabet.
- **Grammar:** A set of production rules that describe how words in the language can be generated. These rules enforce the structure of valid strings.

In this laboratory work, the focus was on regular grammars and their connection to finite automata.

### **1. Regular Grammars**
A **regular grammar** is a type of **formal grammar** that is particularly simple yet powerful enough to describe many useful languages. They are often defined in one of two forms (right-linear or left-linear):
- **Right-linear grammars:** All production rules are of the form A → aB or A → a, where A and B are non-terminal symbols and a is a terminal symbol.
- **Left-linear grammars:** Production rules follow the form A → Ba or A → a.

The grammar if defined as:

**G = (VN, VT, P, S)**

- **VN (Non-Terminals)** - A finite set of symbols like `"S", "A", "B"` etc.
- **VT (Terminals)** – A finite set of actual symbols in the language like `a, b, d`.
- **P (Productions rules)** – A set of rules that map non-terminals to a list of possible substitutions.
- **S (Start Symbol)** – The initial non-terminal.

#### **Chomsky Hierarchy of Grammars**
Noam Chomsky classified grammars into four types based on their expressive power:
1. **Type 0 (Unrestricted Grammars)** – No constraints on production rules.
2. **Type 1 (Context-Sensitive Grammars)** – Productions must have the same length or bigger than the string length.
3. **Type 2 (Context-Free Grammars)** – Each rule must have just one **non-terminal** on the left side.
4. **Type 3 (Regular Grammars)** – Rules must follow specific linear restrictions.

### **2. Finite Automata**
A **finite automaton** is an abstract machine used to recognize patterns within input strings. It is represented as **FA = (Q, Σ, δ, q0, F)** and consists of:
- **States (Q):** A finite set of conditions or configurations.
- **Alphabet (Σ):** A set of symbols the automaton can read.
- **Transition Function (δ):** Rules that describe how the automaton moves from one state to another given an input symbol.
- **Start State (q₀):** The state where computation begins.
- **Final States (F):** A set of states that determine whether the input string is accepted.
  
There also exists 2 types of **Finite Automaton**:
- **Deterministic Finite Automaton (DFA**) – Each state has exactly one transition per input symbol; no ambiguity in state transitions.
- **Non-Deterministic Finite Automaton (NFA)** – A state can have multiple transitions for the same input symbol, including ε (epsilon) transitions.

---

## **Objectives**
The main goals of this laboratory work were to:

1. **Discover what a language is:** Understand the components that make a language formal.
2. **Set up a project:** Create a GitHub repository and develop a solution in a programming language that simplifies the implementation of the tasks.
3. **Implement a Grammar and Finite Automaton:**
- **Grammar:** Define a type/class to represent the grammar, including its components such as non-terminals, terminals, production rules, and start symbol.
- **String Generation:** Implement a method that can generate 5 valid strings from the language defined by the grammar.
- **Conversion:** Create functionality to convert a Grammar object into a FiniteAutomaton object.
- **Finite Automaton Testing:** For the finite automaton, implement a method to check whether an input string is accepted by the automaton through state transitions.


---
# **Implementation Description**
## **1. Grammar Class**

### **Grammar constructor**
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
---

### **Generating a String**
```
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
```
This fution starts with the start symbol and iteratively replaces non-terminals using production rules. It uses a random choice to ensure different valid strings are generated and stops once the string contains only terminal symbols.

---

### **Generating a number of strings**
```
    def generate_n_strings(self, n=5):
        return [self.generate_string() for _ in range(n)]
```
This function generates a number of strings based on the input parameter. It runs a for loop and therefore for each itteration it generates valid string based on the production rules.

---

### **Converting Grammar to Finite Automaton**
```
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
```
This function converts the grammar into a finite automaton by mapping production rules into state transitions. Each non-terminal (VN) becomes a state, and each production rule defines a transition. If a      production has multiple symbols (e.g., `A → aB`), it transitions to B after reading a. If a production produces a terminal-only word (e.g., `A → a`), it transitions to a final state (None). The result is a finite automaton that recognizes the same language as the grammar.

---

## **2. Finite Automaton Class**

### **Finite Automaton Constructor**
```
class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.Q = states
        self.sigma = alphabet
        self.delta = transitions
        self.q0 = start_state
        self.F = final_states
```
This constructor initializes a Finite Automaton by defining its key components. Q represents the set of states, sigma is the input alphabet, delta stores the transition rules, q0 is the start state, and F contains the final (accepting) states. These elements define how the automaton processes input strings and determines whether they belong to the language.

---

### **Checking String Validation**
```
    def string_belongs_to_language(self, input_string):
        current_state = self.q0
        for char in input_string:
            if (current_state, char) in self.delta:
                current_state = self.delta[(current_state, char)]
            else:
                return False
        return current_state in self.F
```
This function checks whether a given input string belongs to the language recognized by the finite automaton. It starts from the initial state (q0) and processes each character of the string by following the transition rules (delta). If a valid transition exists, the automaton moves to the next state, otherwise, it returns False. After processing all characters, the function returns True if the final state is in the set of accepting states (F), meaning the string is valid; otherwise, it returns False.

---

## **3. Main**
```
from grammar import Grammar
vn = {"S", "B", "D", "Q"}
vt = {"a", "b", "c", "d"}
p = {
    "S": ["aB", "bB"],
    "B": ["cD"],
    "D": ["dQ", "a"],
    "Q": ["bB", "dQ"]
}
s = "S"
grammar = Grammar(vn, vt, p, s)
valid_strings = grammar.generate_n_strings()
print("Generated Strings:", valid_strings)
finite_automaton = grammar.to_finite_automaton()
strings = ["abdc", "bca", "aca", "acddda"]
for string in strings:
    result = finite_automaton.string_belongs_to_language(string)
    print(f"'{string}' is valid {result}")
```
This Main defines a regular grammar, generates valid strings, converts it into a finite automaton, and checks if given strings belong to the language. It initializes the grammar with non-terminals, terminals, production rules, and a start symbol. The grammar generates five random strings and is then converted into a finite automaton. Finally, several test strings are checked to determine if they are valid according to the automaton's rules.

---
# **Conclusion**
In this laboratory work, I explored the basics of formal languages, regular grammars, and finite automata. I implemented a Grammar class to define and generate valid strings using production rules and converted it into a Finite Automaton to recognize the same language. By testing different input strings, I verified how a finite automaton processes language recognition. This helped me better understand the relationship between grammars and automata and how these concepts are applied in areas like lexical analysis and pattern matching.

---

## **References**
- **Introduction to Finite Automaton** https://www.geeksforgeeks.org/introduction-of-finite-automata/
- **YouTube video on DFA** https://www.youtube.com/watch?v=Qa6csfkK7_I
- **Introduction to Grammar in Theory of Computation https://www.geeksforgeeks.org/introduction-to-grammar-in-theory-of-computation/
