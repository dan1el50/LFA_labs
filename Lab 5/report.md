# Laboratory work nr. 5 - Chomsky Normal Form
### Course: Formal Languages & Finite Automata
### Author: Cojocaru Daniel

----
# Theory

## *Context-Free Grammar*
A context-free grammar (CFG) is a formal grammar that consists of a set of production rules used to generate all possible strings in a given formal language. CFGs are widely used in compilers, parsers, and language design due to their expressive power. A CFG is defined as a 4-tuple:

**G = (V, Σ, P, S)**

- V: a finite set of variables (non-terminal symbols)
- Σ: a finite set of terminals (alphabet)
- P: a finite set of production rules of the form A → α, where A ∈ V and α ∈ (V ∪ Σ)*
- S: a start symbol (S ∈ V)

CFGs allow production rules with arbitrary lengths, including empty strings and unit productions.
## *Chomsky Normal Form (CNF)*
A CFG is said to be in Chomsky Normal Form if all production rules satisfy one of the following formats:

- A → BC, where A, B, C are non-terminal symbols (and B, C ≠ start symbol)
- A → a, where a is a terminal symbol
- (Optional: S → ε, but only if the language contains the empty string)

## *Steps to Convert CFG to CNF*
**Step 1: Remove ε-productions (nullable variables)**

To eliminate ε-productions, we begin by identifying all nullable variables—those that can derive the empty string ε. Once these are known, we examine every production that includes one or more nullable symbols on its right-hand side and generate new rules by removing any combination of those nullable symbols, effectively covering all possibilities where the nullable symbols may or may not appear. After generating these alternatives, we remove the original ε-productions from the grammar. The only exception is if the start symbol derives ε; in that case, we may retain the rule S → ε.

**Step 2: Eliminate unit productions**

Unit productions are rules where a non-terminal directly produces another single non-terminal, such as A → B. These rules are eliminated by replacing them with the full set of productions that the target non-terminal (B in this case) can generate. This process may be repeated recursively to fully remove chains of unit productions, ensuring that all remaining rules produce either terminals or combinations of non-terminals.

**Step 3: Replace terminals in long productions**

In Chomsky Normal Form, terminals are only allowed in productions where they appear alone on the right-hand side. If a production includes both terminals and non-terminals and is longer than one symbol (for example, A → aB or A → Ba), we replace each terminal with a new non-terminal that derives it. For instance, if we encounter the terminal 'a', we introduce a new rule like Ta → a, and then rewrite the original production as A → Ta B. This guarantees that all longer productions contain only variables.

**Step 4: Convert long right-hand sides into binary rules**

Any production with more than two symbols on the right-hand side needs to be split into binary rules. This is done by introducing new intermediate variables and rewriting the rule in stages. For example, a rule like A → B C D can be converted into A → X2, X2 → B X1, and X1 → C D. The breakdown is typically performed from right to left. To avoid duplicating effort and creating redundant intermediate variables, previously encountered right-hand side combinations can be stored and reused when the same pattern appears again, an optimization known as memoization.

## Objectives:
1. Learn about Chomsky Normal Form (CNF) [1].
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
    - The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
    - The implemented functionality needs executed and tested.
    - Also, another BONUS point would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.
# Implementation description
## *1.Converter*
### *Constructor*
```python
class CFGtoCNFConverter:
    def __init__(self, productions):
        self.productions = defaultdict(list)
        for lhs, rhs_list in productions.items():
            for rhs in rhs_list:
                self.productions[lhs].append(tuple(rhs))
        self.new_rules = defaultdict(list)
        self.terminal_map = {}
        self.counter = 1
        self.rhs_map = {}
        self.step = 0  # step counter
```
This code defines the `CFGtoCNFConverter` class, which is responsible for converting a context-free grammar (CFG) into Chomsky Normal Form (CNF). The `__init__` method initializes several internal data structures needed throughout the conversion process. It takes an input dictionary of grammar rules (`productions`) and stores them in a `defaultdict` where each left-hand side (non-terminal) maps to a list of right-hand side tuples. It also initializes auxiliary dictionaries and counters: `new_rules` for holding newly generated rules, `terminal_map` for mapping terminals to new variables, rhs_map for memoizing intermediate binary rule combinations, and `counter` for naming new variables systematically. The `step` attribute keeps track of which transformation step is currently being executed, mainly for organized printing and debugging.

### *Print Grammar*
```python
    def print_grammar(self, title=""):
        if title:
            print(f"\n=== Step {self.step}: {title} ===")
        for lhs in sorted(self.productions.keys()):
            rhs_list = [' '.join(rhs) for rhs in self.productions[lhs]]
            print(f"{lhs} → {' | '.join(rhs_list)}")
        self.step += 1
```
This method, `print_grammar`, is used to display the current state of the grammar during each step of the conversion process. It optionally accepts a `title` to describe the step (e.g., "After eliminating ε-productions") and prints it along with the step number. Then, it iterates through the non-terminal symbols in sorted order and prints each one followed by its corresponding productions in a clean, readable format. After printing, it increments the step counter so that the next call reflects the correct step number. This method is mainly for tracing the transformation steps in a structured and understandable way.

### *Eliminate Epsilon*
```python
    def eliminate_epsilon(self):
        nullable = set()
        for lhs, rhs_list in self.productions.items():
            for rhs in rhs_list:
                if rhs == ('ε',):
                    nullable.add(lhs)

        while True:
            changed = False
            for lhs, rhs_list in self.productions.items():
                for rhs in rhs_list:
                    if all(symbol in nullable for symbol in rhs):
                        if lhs not in nullable:
                            nullable.add(lhs)
                            changed = True
            if not changed:
                break

        updated = defaultdict(list)
        for lhs, rhs_list in self.productions.items():
            for rhs in rhs_list:
                if rhs == ('ε',):
                    continue
                indices = [i for i, s in enumerate(rhs) if s in nullable]
                for bits in itertools.product([True, False], repeat=len(indices)):
                    temp = list(rhs)
                    for i, use in zip(indices, bits):
                        if not use:
                            temp[i] = None
                    new_rhs = tuple([s for s in temp if s])
                    if new_rhs:
                        updated[lhs].append(new_rhs)
        self.productions = updated
        self.print_grammar("After eliminating ε-productions")
```
This method, `eliminate_epsilon`, removes ε-productions (productions that derive the empty string) from the grammar. It begins by identifying all nullable non-terminals—those that directly or indirectly derive ε. This is done by first collecting all rules of the form A → ε, then iteratively expanding the nullable set until no new symbols can be added.

Once all nullable symbols are identified, the method constructs a new set of rules where nullable symbols are optionally removed from the right-hand sides of existing productions. For each production containing nullable symbols, all combinations with and without those symbols are generated, excluding the empty production itself. Finally, the original ε-productions are excluded from the new grammar, and the updated rules replace the old ones. The updated grammar is then printed as part of Step 1.

### *Eliminate Unit Productions*
```python
    def eliminate_unit_productions(self):
        unit_pairs = set()
        for lhs, rhs_list in self.productions.items():
            for rhs in rhs_list:
                if len(rhs) == 1 and rhs[0].isupper():
                    unit_pairs.add((lhs, rhs[0]))

        while True:
            new_pairs = set(unit_pairs)
            for (a, b) in unit_pairs:
                for rhs in self.productions[b]:
                    if len(rhs) == 1 and rhs[0].isupper():
                        new_pairs.add((a, rhs[0]))
            if new_pairs == unit_pairs:
                break
            unit_pairs = new_pairs

        new_productions = defaultdict(list)
        for lhs, rhs_list in self.productions.items():
            for rhs in rhs_list:
                if len(rhs) == 1 and rhs[0].isupper():
                    continue
                new_productions[lhs].append(rhs)

        for a, b in unit_pairs:
            for rhs in self.productions[b]:
                if len(rhs) == 1 and rhs[0].isupper():
                    continue
                if rhs not in new_productions[a]:
                    new_productions[a].append(rhs)

        self.productions = new_productions
        self.print_grammar("After eliminating unit productions")
```
The `eliminate_unit_productions` method removes unit productions from the grammar—these are rules where a non-terminal directly produces another single non-terminal, like A → B. First, it collects all such unit pairs into a set. Then, it repeatedly expands this set to account for transitive relations, ensuring that if A → B and B → C exist, A → C is also included.

After identifying all unit pairs, the method constructs a new grammar where these unit productions are eliminated. Instead of keeping rules like A → B, it directly adds B’s non-unit rules to A. This effectively inlines the productions of each reachable non-terminal, eliminating unnecessary steps in derivation chains. The updated grammar is then saved and printed as part of the CNF conversion process.

### *Replace Terminals*
```python
    def replace_terminals(self):
        for lhs, rhs_list in list(self.productions.items()):
            new_rhs_list = []
            for rhs in rhs_list:
                if len(rhs) >= 2:
                    new_rhs = []
                    for symbol in rhs:
                        if not symbol.isupper():
                            if symbol not in self.terminal_map:
                                var = f"T{symbol}"  # use Ta, Tb instead of TA, TB
                                self.terminal_map[symbol] = var
                                self.new_rules[var].append((symbol,))
                            new_rhs.append(self.terminal_map[symbol])
                        else:
                            new_rhs.append(symbol)
                    new_rhs_list.append(tuple(new_rhs))
                else:
                    new_rhs_list.append(rhs)
            self.productions[lhs] = new_rhs_list
        self.print_grammar("After replacing terminals in long RHS")
```
The `replace_terminals` method ensures that all productions in the grammar comply with the CNF restriction that terminals can only appear alone on the right-hand side. For every production with a right-hand side of length two or more, it checks each symbol: if a terminal is found, it is replaced with a new non-terminal (e.g., `Ta` for `'a'` or `Tb` for `'b'`).

This replacement is done using a mapping (`terminal_map`) that ensures each terminal symbol is only replaced once, and the corresponding new rule (like `Ta → a`) is stored in `new_rules`. The updated right-hand side then contains only non-terminals, as required by CNF. Finally, the transformed grammar is printed to reflect this step in the conversion process.

### *Variable Reuse or Creation*
```python
    def get_or_create_var(self, rhs_pair):
        if rhs_pair in self.rhs_map:
            return self.rhs_map[rhs_pair]
        var = f"X{self.counter}"
        self.counter += 1
        self.rhs_map[rhs_pair] = var
        self.new_rules[var].append(rhs_pair)
        return var
```
The `get_or_create_var` method is responsible for managing the creation and reuse of intermediate variables when breaking down long right-hand sides into binary rules during CNF conversion. It takes a pair of symbols (`rhs_pair`) and checks if this specific pair has already been assigned a variable. If it has, the method returns the previously assigned variable name, ensuring that the same combination of symbols doesn't result in multiple redundant variables.

If the pair is new, the method generates a fresh variable name (like `X1`, `X2`, etc.) using a counter, stores this association in the `rhs_map` for future reuse, and adds the corresponding production rule to `new_rules`. This approach avoids duplication and keeps the grammar concise and consistent.

### *Long Rules Breaking*
```python
    def break_long_rules(self):
        new_productions = defaultdict(list)

        for lhs, rhs_list in self.productions.items():
            for rhs in rhs_list:
                if len(rhs) <= 2:
                    new_productions[lhs].append(rhs)
                else:
                    symbols = list(rhs)
                    while len(symbols) > 2:
                        last = symbols.pop()
                        second_last = symbols.pop()
                        new_rhs = (second_last, last)
                        var = self.get_or_create_var(new_rhs)
                        symbols.append(var)
                    new_productions[lhs].append(tuple(symbols))

        self.productions = new_productions

        for var, rules in self.new_rules.items():
            self.productions[var].extend(rules)

        self.print_grammar("After breaking long RHS into binary rules (with reuse)")
```
The `break_long_rules` method transforms all production rules with more than two symbols on the right-hand side into equivalent binary rules, as required by Chomsky Normal Form. For each such rule, it processes the right-hand side from **right to left**, breaking it down into pairs. For each pair of symbols, it either reuses an existing variable (if the same pair was already processed) or creates a new one using the `get_or_create_var` method.

This process continues until the right-hand side has only two symbols, at which point the rewritten rule is added to the new set of productions. After processing all rules, the method also includes any newly generated binary rules stored in `new_rules`. Finally, it prints the updated grammar to show the result of this transformation step. This approach ensures that the entire grammar adheres to the CNF format with binary productions.

### *Convertor*
```python
    def convert(self):
        self.print_grammar("Original Grammar")
        self.eliminate_epsilon()
        self.eliminate_unit_productions()
        self.replace_terminals()
        self.break_long_rules()
        return self.productions
```
The `convert` method is the main controller that executes the full transformation of a context-free grammar into Chomsky Normal Form. It begins by printing the original grammar for reference, then sequentially calls the core transformation methods: `eliminate_epsilon`, `eliminate_unit_productions`, `replace_terminals`, and `break_long_rules`. Each of these methods performs a specific normalization step and prints the updated grammar after completion. Once all steps are executed, the final CNF-converted grammar is returned. This method provides a clear, step-by-step execution of the entire CNF conversion process.
## *2.Main*
```python
cfg = {
    "S": [["b", "A"], ["B", "C"]],
    "A": [["a"], ["a", "S"], ["b", "A", "a", "A", "b"]],
    "B": [["A"], ["b", "S"], ["a", "A", "a"]],
    "C": [["ε"], ["A", "B"]],
    "D": [["A", "B"]]
}

converter = CFGtoCNFConverter(cfg)
converter.convert()
```
This final code snippet serves as the **main entry point** for executing the CNF conversion process. It defines an initial context-free grammar (`cfg`) using a dictionary, where each key is a non-terminal symbol and its value is a list of production rules represented as lists of symbols (terminals or non-terminals).

An instance of the `CFGtoCNFConverter` class is then created using this grammar as input. The `convert()` method is called on the converter object, which triggers the full sequence of steps to transform the input grammar into Chomsky Normal Form. During the process, intermediate steps are printed to the console, allowing the user to follow the transformation progress from the original CFG to the final CNF.

## *Output*
![image](https://github.com/user-attachments/assets/b55541d8-3d3e-44ea-8058-b3e840790624)
![image](https://github.com/user-attachments/assets/1fc36698-73b2-4658-af5f-14bffc912001)

# Conclusion
This laboratory work helped me understand the process of converting a context-free grammar (CFG) into Chomsky Normal Form (CNF), which is a standardized form useful in theoretical computer science and parsing algorithms. Through a step-by-step transformation, I learned how to eliminate ε-productions, remove unit productions, replace terminals in long rules, and convert right-hand sides into binary rules. Each transformation has a specific purpose and contributes to reshaping the grammar while preserving the original language it generates.

I also implemented a Python program that automates the conversion process. The program handles all the required steps and prints the grammar after each stage, making the transformation easier to follow and verify. Additionally, optimizations like reusing intermediate variables during rule splitting were included to avoid redundant productions and keep the grammar clean.

Overall, this lab helped me reinforce theoretical knowledge with practical implementation, and gave me a deeper understanding of how grammars can be simplified and standardized for formal analysis and parser design.
