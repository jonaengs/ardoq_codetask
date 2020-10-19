from math import prod as product

def max_product(l):
    neg = sorted(filter(lambda x: x < 0, l))
    pos = sorted(filter(lambda x: x > 0, l))
    return max(pos[-1] * product(neg[:2]), product(pos[-3:]))


assert max_product([1, 10, 2, 6, 5, 3] ) == 300
assert max_product([1, 2, -3, 4, 5, -7]) == 105