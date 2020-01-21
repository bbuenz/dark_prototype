from darkpoly import *
import os
from gmpy2 import *
import timeit

logd = 10

rand = os.urandom(120)

state = random_state(int.from_bytes(rand, 'big'))
p = next_prime(mpz_rrandomb(state, 120))
q = mpz(2) ** (logd * 2 * 120)

coefficients = [mpz_random(state, p) for i in range(2 ** logd)]
poly = Polynomial(q, coefficients)
params = create_params(q, 2 ** logd)
x = mpz_random(state, p)
commitment = poly_commit(q, poly=poly, params=params)
y, proof = eval_proof(q, poly, p, x, commitment=commitment, params=params)
poe_Q = poe_proof(q, commitment, 2, logd)


def run_proof():
    x = mpz_random(state, p)
    y, proof = eval_proof(q, poly, p, x)


def run_proof_with_params():
    x = mpz_random(state, p)
    y, proof = eval_proof(q, poly, p, x, params=params)


def run_commit():
    C = poly_commit(q, poly=poly)


def run_commit_with_params():
    C = poly_commit(q, poly=poly, params=params)


def run_verify():
    eval = verify_eval(q, commitment, proof, 2 ** logd, p, x, y)


def run_poe_proof():
    eval = poe_proof(q, commitment, 2, logd)
    hash(eval)


def run_poe_verify():
    eval = compute_poe(q, commitment, poe_Q, 2, logd)
    hash(eval)
