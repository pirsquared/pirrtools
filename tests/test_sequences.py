"""
This module contains test functions to be used with the pytest framework.
"""

import pytest

from pirrtools.sequences import (
    FibCalculator,
    count_prime_factors,
    get_divisors,
    get_prime_factorization_generator,
    get_prime_generator,
    lcm,
)


def test_fib_calculator_negative():
    """
    Test case for FibCalculator with negative index.
    """
    fib = FibCalculator()
    with pytest.raises(ValueError, match="Index must be a non-negative integer"):
        fib(-1)


def test_fib_calculator():
    """
    Test case for FibCalculator with positive indices.
    """
    fib = FibCalculator()
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(3) == 2
    assert fib(4) == 3
    assert fib(5) == 5
    assert fib(10) == 55
    assert fib(20) == 6765
    assert fib(30) == 832040
    assert fib(50) == 12586269025


def test_get_prime_generator():
    """
    Test case for get_prime_generator function.
    """
    prime_gen = get_prime_generator()
    primes = [next(prime_gen) for _ in range(10)]
    assert primes == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def test_get_prime_factorization_generator():
    """
    Test case for get_prime_factorization_generator function.
    """
    factors_28 = list(get_prime_factorization_generator(28))
    factors_100 = list(get_prime_factorization_generator(100))
    factors_17 = list(get_prime_factorization_generator(17))

    assert factors_28 == [2, 2, 7]
    assert factors_100 == [2, 2, 5, 5]
    assert factors_17 == [17]


def test_count_prime_factors():
    """
    Test case for count_prime_factors function.
    """
    factors_28 = count_prime_factors(28)
    factors_100 = count_prime_factors(100)
    factors_17 = count_prime_factors(17)

    assert factors_28.to_dict() == {2: 2, 7: 1}
    assert factors_100.to_dict() == {2: 2, 5: 2}
    assert factors_17.to_dict() == {17: 1}


def test_get_divisors():
    """
    Test case for get_divisors function.
    """
    divisors_28 = get_divisors(28)
    divisors_100 = get_divisors(100)
    divisors_17 = get_divisors(17)

    assert divisors_28 == [1, 2, 4, 7, 14]
    assert divisors_100 == [1, 2, 4, 5, 10, 20, 25, 50]
    assert divisors_17 == [1]


def test_lcm():
    """
    Test case for lcm function.
    """
    assert lcm(4, 6) == 12
    assert lcm(3, 5, 7) == 105
    assert lcm(10, 15, 20) == 60
    assert lcm(21, 6) == 42
    assert lcm(1, 1, 1) == 1
    assert lcm(0, 1) == 0  # Edge case, including 0 in lcm should return 0
