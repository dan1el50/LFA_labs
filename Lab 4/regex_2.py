import random

MAX_REPEAT = 3  # max repeat for *, +

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

def parse_group_once(expr):
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

# --- MAIN --- #

# Simulated user input
full_input = "P(Q|R|S)T(UV|W|X)*Z+"

# Split regex and constant suffix using comma
if ',' in full_input:
    regex_part, fixed_suffix = full_input.split(',', 1)
else:
    regex_part, fixed_suffix = full_input, ''

generated = parse_group_once(regex_part)
final_output = generated + fixed_suffix

print(f"Generated string: {final_output}")
