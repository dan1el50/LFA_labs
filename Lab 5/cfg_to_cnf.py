from collections import defaultdict
import itertools

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

    def print_grammar(self, title=""):
        if title:
            print(f"\n=== Step {self.step}: {title} ===")
        for lhs in sorted(self.productions.keys()):
            rhs_list = [' '.join(rhs) for rhs in self.productions[lhs]]
            print(f"{lhs} → {' | '.join(rhs_list)}")
        self.step += 1

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

    def get_or_create_var(self, rhs_pair):
        if rhs_pair in self.rhs_map:
            return self.rhs_map[rhs_pair]
        var = f"X{self.counter}"
        self.counter += 1
        self.rhs_map[rhs_pair] = var
        self.new_rules[var].append(rhs_pair)
        return var

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

    def convert(self):
        self.print_grammar("Original Grammar")
        self.eliminate_epsilon()
        self.eliminate_unit_productions()
        self.replace_terminals()
        self.break_long_rules()
        return self.productions

# --- Example input ---
cfg = {
    "S": [["b", "A"], ["B", "C"]],
    "A": [["a"], ["a", "S"], ["b", "A", "a", "A", "b"]],
    "B": [["A"], ["b", "S"], ["a", "A", "a"]],
    "C": [["ε"], ["A", "B"]],
    "D": [["A", "B"]]
}

converter = CFGtoCNFConverter(cfg)
converter.convert()
