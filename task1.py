from math import prod as product
from numbers import Number
from itertools import combinations

"""
Finds the highest value product producible by three elements from the given list
Interpreted highest as meaning most positive, so 2 is higher than 1, and -1 is higher than -2
"""
def max_product(l):
    assert len(l) >= 3 and all(isinstance(n, Number) for n in l),\
        "List must contain only numbers and have a length gte 3"
    return max(map(product, combinations(l, 3)))


assert max_product([1, 10, 2, 6, 5, 3] ) == 300  # highest value requires product of three positive numbers
assert max_product([1, 2, -3, 4, 5, -7]) == 105  # highest value requires product of two negative numbers
assert max_product([-1, -2, -3, -4, -5]) == -6  # highest value is smallest possible negative value
assert max_product([1, 2, -3]) == -6
