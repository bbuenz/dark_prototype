from math import *


class Polynomial:
    def __init__(self, q: int, coefficients=None, encoding=0):
        self.q = q
        if coefficients == None:
            self.coefficients = from_encoding(encoding, q)
        else:
            self.coefficients = coefficients

    def __add__(self, other):
        return Polynomial(self.q,
                          coefficients=list(map(lambda t: t[0] + t[1], zip(self.coefficients, other.coefficients))))

    def __pow__(self, other, modulo=None):
        if modulo is None:
            new_coeff = [x * other for x in self.coefficients]
        else:
            new_coeff = [x * other % modulo for x in self.coefficients]
        return Polynomial(self.q, coefficients=new_coeff)

    def __str__(self):
        return str(self.coefficients)

    def __len__(self):
        return len(self.coefficients)

    def __iter__(self):
        return iter(self.coefficients)

    def __getitem__(self, item):
        return self.coefficients[item]

    def __int__(self):
        return self.encode()

    def eval_at(self, x, N=None):
        result = self.coefficients[-1]
        for i in range(-2, -len(self.coefficients) - 1, -1):
            if N == None:
                result = result * x + self.coefficients[i]
            else:
                result = (result * x + self.coefficients[i]) % N
        return result

    def encode(self) -> int:
        return self.eval_at(self.q)

    def left(self):
        leftcoeff = self.coefficients[:len(self.coefficients) // 2]
        return Polynomial(q=self.q, coefficients=leftcoeff)

    def right(self):
        rightcoeff = self.coefficients[len(self.coefficients) // 2:]
        return Polynomial(q=self.q, coefficients=rightcoeff)
    ## We assume that encoding is the encoding of a polynomial with positive integers only


def from_encoding(encoding: int, q: int) -> list:
    d = int(log(encoding, q)) + 1

    si = [encoding % q ** i for i in range(d + 1)]
    coefficients = [(si[i + 1] - si[i]) // q ** i for i in range(d - 1, -1, -1)]
    return coefficients
