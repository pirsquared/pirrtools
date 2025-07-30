"""
This module provides utility functions for mathematical operations and computations,
including Fibonacci number calculation, prime number generation, prime factorization,
divisor calculation, and least common multiple (LCM) calculation.

Classes:
    - FibCalculator: A class for calculating Fibonacci numbers using memoization and the
      fast doubling algorithm.

Functions:
    - get_prime_generator: Generate an infinite sequence of prime numbers.
    - get_prime_factorization_generator: Generate the prime factorization of a number.
    - count_prime_factors: Count the prime factors of a number and return a pandas
      Series.
    - get_divisors: Get the divisors of a number.
    - lcm: Calculate the Least Common Multiple (LCM) of a set of numbers.

Examples:
    >>> fib = FibCalculator()
    >>> fib(10)
    55

    >>> primes = get_prime_generator()
    >>> next(primes)
    2
    >>> next(primes)
    3

    >>> list(get_prime_factorization_generator(28))
    [2, 2, 7]

    >>> count_prime_factors(28)
    2    2
    7    1
    dtype: int64

    >>> get_divisors(28)
    [1, 2, 4, 7, 14]

    >>> lcm(12, 15)
    60

Note:
    This module relies on the pandas and numpy libraries.
"""

from collections.abc import Generator
from functools import reduce
from itertools import count, islice, product
from math import gcd
from typing import Union

import pandas as pd
from numpy import prod


class FibCalculator:
    """
    A class for calculating Fibonacci numbers using memoization and the fast doubling
    algorithm.

    The `FibCalculator` class provides a method to compute the nth Fibonacci number
    efficiently by caching previously computed values and using the fast doubling
    algorithm. This method is particularly efficient for large Fibonacci numbers.

    Methods:
        - __init__: Initialize the FibCalculator with a base cache.
        - __call__: Calculate the nth Fibonacci number.

    Example:
        >>> fib = FibCalculator()
        >>> fib(10)
        55

    Reference:
        Fast Doubling Algorithm for Fibonacci Numbers:
        https://www.nayuki.io/page/fast-fibonacci-algorithms

    Attributes:
        _cache (Dict[int, int]): A cache to store previously computed Fibonacci numbers.
    """

    def __init__(self):
        """Initialize the FibCalculator with a base cache."""
        self._cache: dict[int, int] = {0: 0, 1: 1, 2: 1}

    def __call__(self, n: int) -> int:
        """Calculate the nth Fibonacci number using memoization and the fast doubling
        algorithm.

        Args:
            n (int): The index of the Fibonacci number to calculate. Must be
              non-negative.

        Returns:
            int: The nth Fibonacci number.

        Raises:
            ValueError: If n is a negative integer.

        Reference:
            Fast Doubling Algorithm for Fibonacci Numbers:
            https://www.nayuki.io/page/fast-fibonacci-algorithms
        """
        if n < 0:
            raise ValueError("Index must be a non-negative integer")

        if n in self._cache:
            return self._cache[n]

        k0, k1 = n // 2, n // 2 + 1
        fk0, fk1 = self(k0), self(k1)
        self._cache[2 * k0] = fk0 * (2 * fk1 - fk0)
        self._cache[2 * k0 + 1] = fk0**2 + fk1**2

        return self._cache[n]


def get_prime_generator() -> Generator[int, None, None]:
    """Generate prime numbers.

    Yields:
        The next prime number.
    """
    prime_lookup = {}
    yield 2

    for q in islice(count(3), 0, None, 2):
        p = prime_lookup.pop(q, None)
        if p:
            x = q + p + p
            while x in prime_lookup:
                x += p + p
            prime_lookup[x] = p
        else:
            prime_lookup[q * q] = q
            yield q


def get_prime_factorization_generator(n: int) -> Generator[int, None, None]:
    """Generate the prime factorization of a number.

    Args:
        n: The number to factorize.

    Yields:
        The next prime factor.
    """
    primes = get_prime_generator()
    for prime in primes:
        if prime * prime > n:
            break
        while n % prime == 0:
            yield prime
            n //= prime

    if n > 1:
        yield n


def count_prime_factors(n: int) -> pd.Series:
    """Count the prime factors of a number.

    Args:
        n: The number to factorize.

    Returns:
        A pandas Series of counts of the prime factors of n.
    """
    prime_factors = list(get_prime_factorization_generator(n))
    return pd.Series(prime_factors).value_counts(sort=False)


def get_divisors(n: int) -> list[int]:
    """Get the divisors of a number.

    Args:
        n: The number to find divisors for.

    Returns:
        A sorted list of divisors of n.
    """
    prime_factors = count_prime_factors(n)

    return sorted(
        map(
            prod,
            product(
                *(
                    [prime**i for i in range(count_prime + 1)]
                    for prime, count_prime in prime_factors.items()
                )
            ),
        )
    )[
        :-1
    ]  # Return all divisors except n itself (proper divisors)


def lcm(*a: Union[int, list[int]]) -> int:
    """Calculate the Least Common Multiple of a set of numbers.

    Args:
        a: The numbers to find the LCM of.

    Returns:
        The LCM of the numbers.
    """
    return reduce(lambda x, y: int(x * y / gcd(x, y)), a)
