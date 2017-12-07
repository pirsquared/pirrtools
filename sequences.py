import pandas as pd
from itertools import product, count, islice
from numpy import prod
from math import gcd
from functools import reduce


def fast_fib(n, *, cache={0: 0, 1: 1, 2: 1}):
    """Use of mutable default as memory is bad practice!!!"""
    if n in cache:
        return cache[n]
    k0 = n // 2
    k1 = k0 + 1
    fk0, fk1 = fast_fib(k0), fast_fib(k1)
    cache[2 * k0] = fk0 * (2 * fk1 - fk0)
    cache[2 * k0 + 1] = fk0 * fk0 + fk1 * fk1
    return cache[n]


def get_prime_generator():
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


def get_prime_factorization_generator(n):
    p = get_prime_generator()
    i = next(p)
    while i * i <= n:
        if n % i == 0:
            yield i
            n = n // i
        else:
            i = next(p)
    yield n


def count_prime_factors(n):
    prime_factors = list(get_prime_factorization_generator(n))
    k = pd.value_counts(
        prime_factors,
        sort=False
    )
    return k


def get_divisors(n):
    prime_factors = count_prime_factors(n)
    primes = prime_factors.index.tolist()
    counts = prime_factors.tolist()

    return sorted(map(
        prod,
        product(
            *[[x ** y for y in range(c + 1)]
              for x, c in zip(primes, counts)]
        )
    ))[:-1]


def lcm(*a):
    """Least Common Multiple"""
    return reduce(lambda x, y: int(x * y / gcd(x, y)), a)
