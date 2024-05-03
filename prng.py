
import random

# Random Number by Mersenne Twister
class MT:
    def random(self):
        random_number = random.randint(0, 102)
        return random_number % 3


# Random Number by Linear Congruential Generator
class LCG:
    def __init__(self, seed=123, a=1664525, c=1013904223, m=2**32):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m

    def extract_number(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed

    def random(self):
        return self.extract_number() % 3






# Random Number by Multiplicative Congruential Generator

class MCG:
    def __init__(self, seed=123, a=48271, m=2**31 - 1):
        self.seed = seed
        self.a = a
        self.m = m

    def _extract_number(self):
        self.seed = (self.a * self.seed) % self.m
        return self.seed

    def random(self):
        return self._extract_number() % 3

