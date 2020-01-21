from rsagroup import RSAGroup
from polynomial import Polynomial
from gmpy2 import *
from util import hash_all
from functools import reduce
import operator
from poe import *


def create_params(q, d):
    temp = RSAGroup.generator()
    params = []
    for i in range(d):
        params.append(temp)
        temp = temp ** q
    return params


def poly_commit(q, coeff: list = None, poly: Polynomial = None, params=None):
    if poly is None:
        poly = Polynomial(q=q, coefficients=coeff)
    if params is not None and len(params) >= len(poly):
        return reduce(operator.mul, map(lambda t: t[1] ** t[0], zip(poly, params)))

    return pow(RSAGroup.generator(), poly.encode())


def open(commit: RSAGroup, poly: Polynomial):
    return 0


def eval_proof(q: int, poly: Polynomial, p: int, x: int, commitment: RSAGroup = None, params=None):
    if commitment is None:
        commitment = poly_commit(q, poly=poly, params=params)
    y = poly.eval_at(x, p)
    salt = hash_all(q, commitment, p, x, y)

    proof = []
    while len(poly) > 1:
        left_poly = poly.left()
        right_poly = poly.right()
        comm_right = poly_commit(q, poly=right_poly, params=params)
        y_right = right_poly.eval_at(x, p)
        poe = poe_proof(salt, comm_right, q, len(right_poly))
        proof.append((comm_right, y_right, poe))
        alpha = hash_all(salt, comm_right, y_right)
        poly = left_poly ** alpha + right_poly
    return y, (proof, poly.coefficients[0])


def verify_eval(q: int, commitment: RSAGroup, proof, d: int, p: int, x: int, y: int) -> bool:
    salt = hash_all(q, commitment, p, x, y)
    d_temp = d
    for commitments in proof[0]:
        d_temp = d_temp // 2
        comm_right = commitments[0]
        y_right = commitments[1]

        y_left = (y - y_right * powmod(x, d_temp, p)) % p
        comm_right_prime = compute_poe(salt, comm_right, commitments[2], q, d_temp)
        comm_left = commitment / comm_right_prime
        alpha = hash_all(salt, comm_right, y_right)

        commitment = (comm_left ** alpha) * comm_right
        y = (y_left * alpha + y_right) % p

    final_f = proof[1]

    if final_f % p != y:
        print("It's not the same")
        return False
    if final_f >= p ** (d + 1):
        print(final_f.bit_length())
        return False
    else:
        return poly_commit(q, coeff=[final_f]) == commitment



