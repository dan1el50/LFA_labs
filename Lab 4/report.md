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
### *Expand token*
```
def expand_token_once(token, modifier):
    if modifier == '*':
        return token * random.randint(0, MAX_REPEAT)
    elif modifier == '+':
        return token * random.randint(1, MAX_REPEAT)
    elif modifier == '?':
        return token if random.choice([True, False]) else ''
    elif modifier.startswith('^'):
        count = int(modifier[1:])
        return token * count
    else:
        return token
```

This function, `expand_token_once`, takes a single character (or group) and a modifier, then returns a randomly expanded
version of that token based on the modifier rules. For example, `*` repeats it 0 to 3 times, `+` repeats it 1 to 3 times, `?`
includes it with 50% chance, and `^n` repeats it exactly `n` times. If there's no modifier, it just returns the token as-is.

### *Group parser*
```
def (expr):
    i = 0
    result = ''
    while i < len(expr):
        if expr[i] == '(':
            # parse group
            start = i + 1
            count = 1
            while i + 1 < len(expr) and count > 0:
                i += 1
                if expr[i] == '(': count += 1
                elif expr[i] == ')': count -= 1
            group_content = expr[start:i]
            options = group_content.split('|')
            chosen = random.choice(options)

            # check for modifier
            modifier = ''
            if i + 1 < len(expr) and expr[i + 1] in '*+?':
                modifier = expr[i + 1]
                i += 1
            elif i + 1 < len(expr) and expr[i + 1] == '^':
                j = i + 2
                while j < len(expr) and expr[j].isdigit():
                    j += 1
                modifier = expr[i + 1:j]
                i = j - 1

            result += expand_token_once(chosen, modifier)

        elif expr[i].isdigit() or expr[i].isalpha():
            char = expr[i]
            modifier = ''
            if i + 1 < len(expr) and expr[i + 1] in '*+?':
                modifier = expr[i + 1]
                i += 1
            elif i + 1 < len(expr) and expr[i + 1] == '^':
                j = i + 2
                while j < len(expr) and expr[j].isdigit():
                    j += 1
                modifier = expr[i + 1:j]
                i = j - 1

            result += expand_token_once(char, modifier)

        i += 1
    return result
```

This function, `parse_group_once`, takes a simplified regex-like expression and generates a randomized string based on its
structure. It supports character groups enclosed in parentheses, which may contain options separated by `|`, and selects
one randomly. It also handles modifiers like `*`, `+`, `?`, and `^n` to control how many times a character or group is repeated.
The function processes the expression left to right, expanding each token or group accordingly and building the final
result.

## *2.Main*
### *Main*
```
full_input = "P(Q|R|S)T(UV|W|X)*Z+"

# Split regex and constant suffix using comma
if ',' in full_input:
    regex_part, fixed_suffix = full_input.split(',', 1)
else:
    regex_part, fixed_suffix = full_input, ''

generated = parse_group_once(regex_part)
final_output = generated + fixed_suffix

print(f"Generated string: {final_output}")
```

This part of the code defines the input expression and processes it. It first checks if the input contains a comma—if
so, it splits the string into a regex-like pattern `(regex_part)` and a fixed suffix `(fixed_suffix)` to append at the end.
Then, it uses `parse_group_once` to generate a randomized string from the pattern and adds the fixed suffix. Finally, it
prints the complete generated result.

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
