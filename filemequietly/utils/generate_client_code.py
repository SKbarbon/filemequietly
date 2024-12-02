import string, random


def generate_random_code():
    part1 = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
    part2 = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
    return f"{part1}-{part2}"