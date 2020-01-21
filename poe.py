from rsagroup import RSAGroup
from gmpy2 import *
from util import hash_all


def poe_proof(salt, C: RSAGroup, q: int, exp: int):
    ell = next_prime(hash_all(salt, C, q, exp,248))
    quotient = (q ** exp) // ell
    Q = C ** quotient
    return Q


def compute_poe(salt, C: RSAGroup, Q: RSAGroup, q: int, exp: int):
    #Must use 2 lambda + log(2 lambda) challenge, 248 = lambda 120
    ell = next_prime(hash_all(salt, C, q, exp, 248))
    r = powmod(q, exp, ell)
    return Q ** ell * C ** r
