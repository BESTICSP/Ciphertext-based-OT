import random
import socket
import  time
from gmpy2 import invert
import json

class Bob:
    def __init__(self,p,g,n):
        self.p = p
        self.g = g
        self.n = n

    def str_xor(self, s: str, k: str):
        k = (k * (len(s) // len(k) + 1))[0:len(s)]
        return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s, k))

    def gen_key(self,C_list):
        self.want_message = random.randint(0,self.n)
        k = random.randint(2 ** 127, 2 ** 128)  # generate a big random num
        self.k = k
        gk = pow(self.g, k, self.p)
        inv = invert(gk,self.p)
        if self.want_message != 0:
            pk0 = (C_list[self.want_message - 1] * inv) % self.p
        else:
            pk0 = gk
        return pk0

    def de_message(self,messages,gr):
        gr = int(gr)
        key = pow(gr,self.k,self.p)
        de_messages = []
        for message in messages:
            de_msg = self.str_xor(message, str(key) + 'lianqiao love study')
            de_messages.append(de_msg)
            print(de_msg)
        return de_messages[int(self.want_message)]


def main():
    p = 320272671238909464478547551273142272013
    g = 317784432528923075244970559336684737753
    n = int(input('please input n:\n'))
    bob = Bob(p,g,n)
    # 以元组形式定义一个 IP 地址和端口
    ip_port = ('127.0.0.1',9988)
    # 创建对象并绑定 IP 地址开始监听
    sk = socket.socket()
    sk.connect(ip_port)
    sk.sendall('\nI am bob, requesting communication, executing the protocolt.....\n'.encode())
    print(sk.recv(1024).decode())
    json_C_list = sk.recv(2048).decode()
    gr = sk.recv(1024).decode()
    C_list= json.loads(json_C_list)
    pk_0 = bob.gen_key(C_list)
    sk.sendall(str(pk_0).encode())
    print(sk.recv(1024).decode())
    json_message_enc = sk.recv(2048).decode()
    messages = json.loads(json_message_enc)
    print(sk.recv(1024).decode())
    m = bob.de_message(messages,gr)
    print('要的第{}个消息'.format(bob.want_message),m)
    sk.sendall('I\'m bob, protocol is over, I will close the connect,see you again!\n'.encode())
    sk.close()


if __name__=='__main__':
    main()
