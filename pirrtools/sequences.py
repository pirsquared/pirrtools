from typing import Generator, List, Union, Dict
import pandas as pd
from itertools import product, count, islice
from numpy import prod
from math import gcd
from functools import reduce


class FibCalculator:
    def __init__(self):
        """Initialize the FibCalculator with a base cache."""
        self._cache: Dict[int, int] = {0: 0, 1: 1, 2: 1}

    def __call__(self, n: int) -> int:
        """
        Calculate the nth Fibonacci number using memoization and the fast doubling algorithm.

        Args:
            n (int): The index of the Fibonacci number to calculate. Must be non-negative.

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
    """
    Generate prime numbers.

    Yields:
        The next prime number.
    """
    D = {}
    yield 2

    for q in islice(count(3), 0, None, 2):
        p = D.pop(q, None)
        if p:
            x = q + p + p
            while x in D:
                x += p + p
            D[x] = p
        else:
            D[q * q] = q
            yield q


def get_prime_factorization_generator(n: int) -> Generator[int, None, None]:
    """
    Generate the prime factorization of a number.

    Args:
        n: The number to factorize.

    Yields:
        The next prime factor.
    """
    p = get_prime_generator()
    i = next(p)
    while i**2 <= n:
        if n % i:
            i = next(p)
        else:
            yield i
            n //= i
    yield n


def count_prime_factors(n: int) -> pd.Series:
    """
    Count the prime factors of a number.

    Args:
        n: The number to factorize.

    Returns:
        A pandas Series of counts of the prime factors of n.
    """
    prime_factors = list(get_prime_factorization_generator(n))
    return pd.value_counts(prime_factors, sort=False)


def get_divisors(n: int) -> List[int]:
    """
    Get the divisors of a number.

    Args:
        n: The number to find divisors for.

    Returns:
        A sorted list of divisors of n.
    """
    prime_factors = count_prime_factors(n)
    primes, counts = prime_factors.index.tolist(), prime_factors.tolist()

    return sorted(
        prod(divisor) for divisor in product(
            *[list(map(lambda x: prime**x, range(count + 1))) for prime, count in zip(primes, counts)]
        )
    )[:-1]


def lcm(*a: Union[int, List[int]]) -> int:
    """
    Calculate the Least Common Multiple of a set of numbers.

    Args:
        a: The numbers to find the LCM of.

    Returns:
        The LCM of the numbers.
    """
    return reduce(lambda x, y: int(x * y / gcd(x, y)), a)
