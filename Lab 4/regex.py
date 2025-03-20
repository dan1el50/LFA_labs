import random

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

def trace_regex_processing(regex_func, regex_name):
    print(f"\nProcessing {regex_name}:")
    generated_string = regex_func()
    print(f"Final generated string: {generated_string}\n")