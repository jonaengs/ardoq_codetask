from math import prod as product
from numbers import Number

"""
Finds the highest value product producible by three elements from the given list
Assume highest => most positive. So 2 is higher than 1, and -1 is higher than -2
"""
def max_product(l):
    assert len(l) >= 3
    assert all(isinstance(n, Number) for n in l)

    neg = sorted(filter(lambda x: x < 0, l))
    pos = sorted(filter(lambda x: x > 0, l))

    return max(
        pos[-1] * product(neg[:2]) if len(pos) >= 1 and len(neg) >= 2 else float("-inf"), 
        product(pos[-3:]) if len(pos) >= 3 else float("-inf"), 
        product(neg[-3:]) if len(neg) >= 3 else float("-inf")
    )


assert max_product([1, 10, 2, 6, 5, 3] ) == 300  # largest value requires product of three positive numbers
assert max_product([1, 2, -3, 4, 5, -7]) == 105  # largest value requires product of two negative numbers
assert max_product([-1, -2, -3, -4, -5]) == -6  # largest value is smallest negative value
