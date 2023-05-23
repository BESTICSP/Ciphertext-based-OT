import random
import socket
import  time
from gmpy2 import invert
import json


class Alice():
    def __init__(self,p,g,n):
        self.p = p
        self.g = g
        self.n = n

    def str_xor(self, s: str, k: str):
        k = (k * (len(s) // len(k) + 1))[0:len(s)]
        return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s, k))

    def gen_messages(self):
        messages = []
        for i in range(self.n):
            msg = 'this is message ' + str(i)
            messages.append(msg)
        return messages

    def gen_C(self):
        C = []
        r = random.randint(2 ** 129, 2 ** 151)
        self.r = r
        gr = pow(self.g, r, self.p)
        for i in range(self.n):
            c = random.randint(2 ** 129, 2 ** 151)
            C.append(c)
        self.C = C
        return C,gr

    def encrypt_message(self,pk_0):
        pk_0 = int(pk_0)
        pk_0_r = pow(pk_0,self.r,self.p)
        inv = invert(pk_0_r,self.p)
        pk_i_r_list = []
        pk_i_r_list.append(pk_0_r)
        for i in range(self.n):
            pki = (pow(self.C[i], self.r, self.p) * inv) % self.p
            pk_i_r_list.append(pki)
        messages = self.gen_messages()
        message_miwen = []  # store ciphertext
        for i in range(self.n):
            en_message = self.str_xor(messages[i], str(pk_i_r_list[i]) + 'lianqiao love study' )  # encrypt
            message_miwen.append(en_message)
        # en_message1 = self.str_xor( message1, str(pk1_r) + 'lianqiao love study')  # decrypt
        # message_miwen.append(en_message1)
        return message_miwen


def main():
    p = 320272671238909464478547551273142272013
    g = 317784432528923075244970559336684737753
    n = int(input('please input n:\n'))
    alice = Alice(p,g,n)
    ip_port = ('127.0.0.1',9988)
    # 创建对象并绑定 IP 地址开始监听
    sk = socket.socket()
    sk.bind(ip_port)
    sk.listen(5)
    # 开始接收消息
    # conn 表示客户端与服务端建立连接后的专有通信线路
    conn,addr = sk.accept() # accept 属于阻塞式，没有收到连接请求就不会继续向下运行
    # 接收客户端发来的消息
    print(conn.recv(1024).decode())
    conn.sendall('\nOK, I\'m alce, please send the key.......\n'.encode())

    C_list, gr = alice.gen_C()
    json_C_list = json.dumps(C_list).encode()
    conn.sendall(json_C_list)
    conn.sendall(str(gr).encode())

    pk_0 = conn.recv(1024).decode()

    conn.sendall('OK, I\'m alce, prepare to send the ciphertext, ready to get it! bob, OK?......\n'.encode())

    message_enc = alice.encrypt_message(pk_0)
    json_message_enc = json.dumps(message_enc).encode()
    conn.sendall(json_message_enc)
    conn.sendall('I\'alice，ciphertext already send to you，please give me a signal......\n'.encode())

    print(conn.recv(1024).decode())
    # 关闭连接
    conn.close()


if __name__=='__main__':
    main()