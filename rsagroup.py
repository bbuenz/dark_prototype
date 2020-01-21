from gmpy2 import mpz
import gmpy2
#829 bit RSA number https://en.wikipedia.org/wiki/RSA_numbers#RSA-250
N = mpz("2140324650240744961264423072839333563008614715144755017797754920881418023447\
          1401366433455190958046796109928518724709145876873962619215573630474547705208\
          0511905649310668769159001975940569345745223058932597669747168173806936489469\
          9871578494975937497937")


class RSAGroup:

    def __init__(self, value):
        self.value = value % N

    @classmethod
    def generator(cls):
        return RSAGroup(2)

    def __mul__(self, other):
        return RSAGroup(self.value * other.value % N)

    def __pow__(self, power, modulo=None):
        return RSAGroup(pow(self.value, power, N))

    def __str__(self):
        return "%s mod %s" % (str(self.value), str(N))

    def __eq__(self, other):
        return self.value == other.value

    def __truediv__(self, other):
        return RSAGroup(gmpy2.divm(self.value, other.value, N))
