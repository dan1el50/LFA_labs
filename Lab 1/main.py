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


