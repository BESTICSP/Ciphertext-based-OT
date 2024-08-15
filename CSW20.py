import math
import os
import random

import gmpy2
from data_process import hash_bignumber256, hash_bignumber, hash_bignumber512


class Alice(object):
    def __init__(self, p, g):
        self.p = p
        self.g = g

    def str_xor(self, s: str, k: str):
        # 将密钥 k 拓展为与字符串 s 相同长度（密钥拓展）
        k = (k * (len(s) // len(k) + 1))[0:len(s)]
        # 对字符串 s 和拓展后的密钥 k 中的每一对字符进行异或运算，然后将结果连接成一个新的字符串
        return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s, k))

    def gen_z(self):
        self.r = random.randint(2 ** 127, 2 ** 128)
        z = gmpy2.powmod(self.g, self.r, self.p)
        return z

    def gen_and_enc(self, sid, A, T):
        m0 = hash_bignumber256(str(sid) + str(gmpy2.powmod(A, self.r, self.p)))
        T_inv = gmpy2.invert(T, self.p)
        m1 = hash_bignumber256(str(sid) + str(gmpy2.powmod(A * T_inv, self.r, self.p)))
        sid_m0 = hash_bignumber512(str(sid) + str(m0))
        sid_m1 = hash_bignumber512(str(sid) + str(m1))
        chall = self.str_xor(str(sid_m0), str(sid_m1)).encode()
        gama = hash_bignumber512(str(sid) + str(hash_bignumber512(str(sid) + str(m0))))
        m = [m0, m1]
        return chall, gama, m


class Bob(object):
    def __init__(self, p, g):
        self.p = p
        self.g = g

    def str_xor(self, s: str, k: str):
        k = (k * (len(s) // len(k) + 1))[0:len(s)]
        return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s, k))

    def enc_data(self):
        self.want_messsage = random.randint(0, 1)
        self.sid = os.getpid()
        s = ''.join(str(random.randint(0, 1)) for _ in range(1024))
        T = hash_bignumber(str(self.sid) + s)
        self.a = random.randint(2 ** 127, 2 ** 128)
        A = (gmpy2.powmod(self.g, self.a, self.p) * gmpy2.powmod(T, self.want_messsage, self.p)) % self.p
        return s, A, self.sid, T, self.want_messsage

    def get_message(self, z, chall):
        mc = hash_bignumber256(str(self.sid) + str(gmpy2.powmod(z, self.a, self.p)))
        temp = hash_bignumber512(str(sid) + str(mc))
        if self.want_messsage != 0:
            Ans = self.str_xor(str(temp), chall.decode())
        else:
            Ans = temp
        return mc, Ans


if __name__ == '__main__':
    p = 320272671238909464478547551273142272013
    g = 317784432528923075244970559336684737753
    alice = Alice(p, g)
    bob = Bob(p, g)
    z = alice.gen_z()
    s, A, sid, T, c = bob.enc_data()
    chall, gama, m = alice.gen_and_enc(sid, A, T)
    print(m)
    print(f'要的第{c}个消息')
    mc, Ans = bob.get_message(z, chall)
    print(mc)
