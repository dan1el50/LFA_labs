# Laboratory work nr. 4 - Regular expressions
### Course: Formal Languages & Finite Automata
### Author: Cojocaru Daniel

----
# Theory

## *Regular Expressions*

Regular expressions (regex) are sequences of characters that define search patterns, primarily used for string matching
and text processing. They serve as powerful tools in many fields, including programming, data validation, text
processing, and natural language processing.

Regular expressions are widely used in different domains. They help in text searching and pattern matching, such as
finding email addresses in a document. In lexical analysis, they recognize tokens in programming languages, while in
data validation, they check if user input matches specific formats, like phone numbers or passwords. They are also used
in text transformation tasks, such as replacing substrings in a file, and play a role in compilers and interpreters for
parsing source code.

## *Basic Components*
A regular expression consists of various components that define how patterns match text. Literals are characters that
match themselves directly, such as the pattern abc matching the exact string "abc." Metacharacters are special symbols
that introduce flexibility in pattern definition, while quantifiers specify how many times a certain pattern should
appear in a string.

The asterisk `*` matches zero or more occurrences of the preceding element, while the plus sign `+` ensures at least one
occurrence. The caret `^` is sometimes used to denote power in certain contexts, though in regex, it often signifies the
start of a string. The vertical bar `|` acts as an OR operator, allowing a pattern to match one of multiple possible
options. For example, `(abc|def)` matches either "abc" or "def".

Grouping in regex is achieved using parentheses (), allowing for more complex pattern definitions. Alternation,
represented by |, functions as a logical OR, enabling a pattern to match one of multiple possible options. For example,
the pattern (cat|dog)house matches both "cathouse" and "doghouse". Quantifiers determine the number of times a specific
pattern should appear. The * quantifier allows zero or more occurrences, while + requires at least one occurrence. The ?
quantifier permits zero or one occurrence, making the preceding element optional.

A string may be generated in the following way using a regular expression. For example let's suppose we have this
regular expression: `(a|b)c(d|e)*f+g?` then to form a string we will chose either `a` or `b` from the first parenthesis
then we add `c` then we chose `d` or `e` and include it either 0 times or as many as we want then we input `f` either
once or as many times as we want and in the end we either add `g` or not.

## Objectives:
1. Write and cover what regular expressions are, what they are used for;

2. Below you will find 3 complex regular expressions per each variant. Take a variant depending on your number in the list of students and do the following:

    a. Write a code that will generate valid combinations of symbols conform given regular expressions (examples will be shown).

    b. In case you have an example, where symbol may be written undefined number of times, take a limit of 5 times (to evade generation of extremely long combinations);

    c. Bonus point: write a function that will show sequence of processing regular expression (like, what you do first, second and so on)

Write a good report covering all performed actions and faced difficulties.
# Implementation description
## *1.Regex*
### *Regex 1*
```
def regex1():
    a_b = random.choice(['a', 'b'])
    c_d = random.choice(['c', 'd'])
    e_count = random.randint(1, 5)
    g = random.choice([True, False])
    result = f"{a_b}{c_d}{'E' * e_count}{'G' if g else ''}"
    print(f"Step 1: Process (a|b). Choosing '{a_b}'. Current string: {a_b}")
    print(f"Step 2: Process (c|d). Choosing '{c_d}'. Current string: {a_b}{c_d}")
    print(f"Step 3: Process E+. Generating {e_count} times 'E'. Current string: {a_b}{c_d}{'E' * e_count}")
    if g:
        print(f"Step 4: Process G?. Including 'G'. Current string: {result}")
    else:
        print(f"Step 4: Process G?. Skipping 'G'. Current string: {a_b}{c_d}{'E' * e_count}")
    return result
```

The function `regex1()` generates a random string that matches the regular expression `(a|b)(c|d)E⁺G?`, while also printing
step-by-step how the string is formed. It begins by selecting a random letter, either `'a'` or `'b'`, from the first group `(
a|b)`, and immediately prints the current state of the string. Then, it selects a random letter, either `'c'` or `'d'`, from
the second group `(c|d)`, appends it to the result, and updates the console output accordingly. Next, it generates between
one and five repetitions of the letter `'E'` to satisfy the `E+` requirement and prints the updated string. Finally, it
randomly decides whether to include the optional `'G'`, as dictated by `G?`, either appending it and indicating its
inclusion in the console or skipping it and printing that it was omitted. The function returns the fully generated
string.

### *Regex 2*
```
def regex2():
    p = 'P'
    q_r_s = random.choice(['Q', 'R', 'S'])
    t = 'T'
    uv_w_x = ''.join(random.choice(['UV', 'W', 'X']))
    z = random.randint(1, 5)
    random_zero_to_five = random.randint(0, 5)
    result = f"{p}{q_r_s}{t}{uv_w_x * random_zero_to_five}{'Z' * z}"
    print(f"Step 1: Process 'P'. Fixed character. Current string: {p}")
    print(f"Step 2: Process (Q|R|S). Choosing '{q_r_s}'. Current string: {p}{q_r_s}")
    print(f"Step 3: Process 'T'. Fixed character. Current string: {p}{q_r_s}{t}")
    if uv_w_x:
        print(f"Step 4: Process (UV|W|X)*. Generated '{uv_w_x}' {random_zero_to_five} times. Current string: {p}{q_r_s}{t}{uv_w_x * random_zero_to_five}")
    else:
        print(f"Step 4: Process (UV|W|X)*. Skipped (empty). Current string: {p}{q_r_s}{t}")
    print(f"Step 5: Process Z+. Generating {z} times 'Z'. Current string: {result}")
    return result
```

The function `regex2()` generates a random string that matches the regular expression `P(Q|R|S)T(UV|W|X)*Z+`, while also
printing step-by-step how the string is constructed. It begins by appending the fixed letter `'P'` to the result and
printing the initial state. Next, it selects a random letter from `Q`, `R`, or `S` for the `(Q|R|S)` group, updates the result,
and prints the current string. The fixed character `'T'` is then added, with an updated console output. Following this,
the function selects either `'UV'`, `'W'`, or `'X'` and decides how many times (between 0 and 5) it should be repeated, as
dictated by the `(UV|W|X)*` pattern. If this section is generated, the console prints the chosen sequence and how many
times it appears; otherwise, it prints that the section was skipped. Lastly, it generates a sequence of `'Z'` characters,
ensuring at least one repetition but allowing up to five, as required by `Z+`, and appends it to the result. The final
constructed string is printed and returned.

### *Regex 3*
```
def regex3():
    one = '1'
    zero_or_one = ''.join(random.choice(['0', '1']))
    two = '2'
    three_or_four = ''.join(random.choice(['3', '4']))
    last = '36'
    random_zero_to_five = random.randint(0, 5)
    result = f"{one}{zero_or_one * random_zero_to_five}{two}{three_or_four * 5}{last}"
    print(f"Step 1: Process '1'. Fixed character. Current string: {one}")
    if zero_or_one:
        print(f"Step 2: Process (0|1)*. Generated '{zero_or_one}' {random_zero_to_five} times. Current string: {one}{zero_or_one * random_zero_to_five}")
    else:
        print(f"Step 2: Process (0|1)*. Skipped (empty). Current string: {one}")
    print(f"Step 3: Process '2'. Fixed character. Current string: {one}{zero_or_one * random_zero_to_five}{two}")
    print(
        f"Step 4: Process (3|4)⁵. Generated '{three_or_four}' 5 times. Current string: {one}{zero_or_one * random_zero_to_five}{two}{three_or_four * 5}")
    print(f"Step 5: Process '36'. Fixed ending. Current string: {result}")
    return result
```

The function `regex3()` generates a random string that matches the regular expression `1(0|1)*2(3|4)⁵36`, while also
printing step-by-step how the string is formed. It starts by appending the fixed character `'1'` and displaying the
initial state. Then, it selects either `'0'` or `'1'` and determines how many times (between 0 and 5) it should be repeated,
as dictated by the `(0|1)*` pattern. If this section is generated, the function prints the chosen sequence and its
repetitions; otherwise, it prints that this part was skipped. Next, the fixed character `'2'` is added to the string,
followed by the generation of exactly five repetitions of either `'3'` or `'4'`, as required by `(3|4)⁵`. The generated
section is printed with its final state. Finally, the fixed sequence `"36"` is appended, completing the pattern. The
function prints the final constructed string and returns it.

### *Regex Processing*
```
def regex1():
    a_b = random.choice(['a', 'b'])
    c_d = random.choice(['c', 'd'])
    e = random.randint(1,5)
    g = random.choice([True, False])
    if g:
        return f"{a_b}{c_d}{'E' * e}{'G'}"
    else:
        return f"{a_b}{c_d}{'E' * e}"
```

The function `trace_regex_processing()` is responsible for executing a given regex-generating function and displaying its
output in a structured way. It starts by printing the name of the regex being processed. Then, it calls the provided
function `(regex_func)`, which generates a random string while printing step-by-step how it was formed. Finally, it prints
the fully constructed string as the final output. This function serves as a wrapper to ensure that each regex function
runs in a consistent and informative manner.

## *2.Main*
### *Main*
```
from regex import regex1, regex2, regex3, trace_regex_processing

print("Tracing regex processing:")
trace_regex_processing(regex1, "Regex 1")
trace_regex_processing(regex2, "Regex 2")
trace_regex_processing(regex3, "Regex 3")
```

This script serves as the main entry point for executing and tracing the regex generation process. It imports the
functions `regex1`, `regex2`, `regex3`, and `trace_regex_processing` from the regex module. The script begins by printing `"
Tracing regex processing:"`, indicating that it is about to process the regular expressions. Then, it calls
`trace_regex_processing()` for each regex function, sequentially generating and printing step-by-step how each string is
formed, followed by the final generated string. This ensures that all three regex patterns are executed and displayed in
an organized manner.

## *Output*
![img_1.png](img_1.png)

# Conclusion
In this lab, I explored the use of regular expressions and implemented a program that generates random strings
conforming to specific regex patterns. I started by understanding the structure of each regular expression and then
developed functions that generate valid strings while following step-by-step processing logic. Additionally, I
implemented a bonus feature that provides a detailed breakdown of how each string is formed, making it easier to
visualize how regex rules apply in practice.
Through this process, I reinforced my understanding of pattern matching, quantifiers, alternations, and optional
elements within regular expressions. Implementing the step-by-step tracing function helped me see how regex components
contribute to final outputs, making the concept more intuitive. Overall, this lab was a great exercise in both
theoretical understanding and practical application of regular expressions.
