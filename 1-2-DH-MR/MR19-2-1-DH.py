import  random
from RabinMiller import genPrime
from gmpy2 import invert
import time

def prepare():
    g = random.randint(2**129,2**151)
    a = random.randint(14,134)
    b = random.randint(14,134)
    c = g ** a
    R = g ** b
    return g,c,R

def get_prime():
    q = genPrime(128)
    p = genPrime(128)
    return p,q

def main(want_message):
    p, q = get_prime()
    if want_message == 0:
        g,r0,R = prepare()
        c = random.randint(14, 50)
        R = pow(R, c, p)
        R_inv = invert(R, p)
        r1 = r0 * R_inv
        A0 = r0 ^ (pow(r1, c, p))
        A1 = r1 ^ (pow(r0, c, p))
    else:
        g,r1,R = prepare()
        c = random.randint(14,50)
        R = pow(R,c,p)
        R_inv = invert(R,p)
        r0 = r1 * R_inv
        A0 = r0 ^ (pow(r1,c,p))
        A1 = r1 ^ (pow(r0,c,p))
    return A0,A1


if __name__ == "__main__":
     A0,A1 = main(random.randint(0,1))
