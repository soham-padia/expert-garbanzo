# src/paillier.py

import random
from sympy import mod_inverse

class Paillier:
    def __init__(self, bit_length=1024):
        self.p = self.generate_large_prime(bit_length)
        self.q = self.generate_large_prime(bit_length)
        self.n = self.p * self.q
        self.n_squared = self.n ** 2
        self.g = self.n + 1  # g = n + 1

        # λ(n) = lcm(p-1, q-1)
        self.lam = (self.p - 1) * (self.q - 1) // self.gcd(self.p - 1, self.q - 1)

    def generate_large_prime(self, bit_length):
        while True:
            prime_candidate = random.getrandbits(bit_length)
            if self.is_prime(prime_candidate):
                return prime_candidate

    def is_prime(self, n, k=5):  # Miller-Rabin primality test
        if n <= 1:
            return False
        if n <= 3:
            return True
        d = n - 1
        while d % 2 == 0:
            d //= 2
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            while d != n - 1:
                x = (x * x) % n
                d *= 2
                if x == 1:
                    return False
                if x == n - 1:
                    break
            else:
                return False
        return True

    def encrypt(self, plaintext):
        # Choose random r in Z_n
        r = random.randint(1, self.n - 1)
        # c = g^m * r^n mod n^2
        c = (pow(self.g, plaintext, self.n_squared) * pow(r, self.n, self.n_squared)) % self.n_squared
        return c

    def decrypt(self, ciphertext):
        # m = (L(c^λ mod n^2) * μ mod n)
        u = pow(ciphertext, self.lam, self.n_squared)
        l = (u - 1) // self.n
        m = (l * mod_inverse(self.lam, self.n)) % self.n
        return m

    def add_encrypted(self, c1, c2):
        # c1 * c2 mod n^2
        return (c1 * c2) % self.n_squared

    @staticmethod
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
