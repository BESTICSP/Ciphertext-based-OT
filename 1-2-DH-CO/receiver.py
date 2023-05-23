'''
lianqiao,  beijing, 2023.5.21
When using dual threads,
A*gb will have a memory overflow problem,
currently there is no good way to solve.
so an error will occur when want_messasge=1,
but it can run normally when using function simulation.
'''


import random
import socket
import  time
from gmpy2 import invert

class Bob:
    def __init__(self,p,g):
        self.p = p
        self.g = g

    def str_xor(self, s: str, k: str):
        k = (k * (len(s) // len(k) + 1))[0:len(s)]
        return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s, k))

    def gen_key(self,A):
        # self.want_message = random.randint(0,1)
        self.want_message = 0
        b = random.randint(10 ** 128, 10 ** 129)
        self.b = b
        if self.want_message == 0:
            B = pow(self.g, b, self.p)
        else:
            gb = pow(self.g, b, self.p)
            B = (A * gb) % self.p
            self.B = B
        return B

    def de_message(self,messages,A):
        A = int(A)
        key = pow(A,self.b,self.p)
        de_messages = []
        for message in messages:
            de_msg = self.str_xor(message, str(key) + 'lianqiao love study')
            de_messages.append(de_msg)
        return de_messages[int(self.want_message)]


def main():
    p = 320272671238909464478547551273142272013
    g = 317784432528923075244970559336684737753
    bob = Bob(p,g)
    # 以元组形式定义一个 IP 地址和端口
    ip_port = ('127.0.0.1',9978)
    # 创建对象并绑定 IP 地址开始监听
    sk = socket.socket()
    sk.connect(ip_port)
    sk.sendall('\nI am bob, requesting communication, executing the protocolt.....\n'.encode())
    print(sk.recv(1024).decode())
    A = sk.recv(1024).decode()

    B = bob.gen_key(A)
    sk.sendall(str(B).encode())

    print(sk.recv(1024).decode())
    m_0 = sk.recv(1024).decode()
    m_1 = sk.recv(1024).decode()
    messages = []
    messages.append(m_0)
    messages.append(m_1)
    print(sk.recv(1024).decode())
    m = bob.de_message(messages,A)
    print('要的第{}个消息'.format(bob.want_message),m)
    sk.sendall('I\'m bob, protocol is over, I will close the connect,see you again!\n'.encode())
    sk.close()


if __name__=='__main__':
    main()
