from darkpoly import *
import os
from gmpy2 import *
import unittest


class MyTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logd = 10

        rand = os.urandom(120)

        self.state = random_state(int.from_bytes(rand, 'big'))
        self.p = next_prime(mpz_rrandomb(self.state, 120))
        self.q = mpz(2) ** (self.logd * 2 * 120)

    def test_verify(self):
        coefficients = [mpz_random(self.state, self.p) for i in range(2 ** self.logd)]
        poly = Polynomial(self.q, coefficients)
        com = poly_commit(self.q, poly=poly)
        x = mpz_random(self.state, self.p)
        y, proof = eval_proof(self.q, poly, self.p, x, com)
        valid = verify_eval(self.q, com, proof, len(poly), self.p, x, y)

        self.assertEqual(valid, True)
        self.assertEqual(y, poly.eval_at(x, self.p))

    def test_param_commit(self):
        coefficients = [mpz_random(self.state, self.p) for i in range(2 ** self.logd)]
        poly = Polynomial(self.q, coefficients)
        com = poly_commit(self.q, poly=poly)
        params = create_params(self.q, 2 ** self.logd)
        commit2 = poly_commit(self.q, poly=poly, params=params)
        self.assertEqual(com, commit2)

    def test_small_params(self):
        coefficients = [mpz_random(self.state, self.p) for i in range(2 ** self.logd)]
        poly = Polynomial(self.q, coefficients)
        com = poly_commit(self.q, poly=poly)
        params = create_params(self.q, 2 ** (self.logd + 1))
        commit2 = poly_commit(self.q, poly=poly, params=params)
        self.assertEqual(com, commit2)

    def test_poe(self):
        C = RSAGroup.generator() ** 3245
        Cprime = C ** (self.q ** 23)
        pi = poe_proof(0, C, self.q, 23)
        C_result = compute_poe(0, C, pi, self.q, 23)
        print(Cprime)
        print(C_result)
        self.assertEqual(Cprime, C_result)


if __name__ == '__main__':
    unittest.main()
