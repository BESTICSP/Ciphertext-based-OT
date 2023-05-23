import random
import socket
import  time

class Bob:
    def __init__(self,p):
        self.p = p

    def str_xor(self, s: str, k: str):
        k = (k * (len(s) // len(k) + 1))[0:len(s)]
        return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s, k))

    def random_encrypt(self,want_message, pk):
        e = pk[0]
        n = pk[1]
        r = random.randint(2 ** 150, 2 ** 151)  # generate a big random num
        en_r = pow(r, e, n)  # encrypt
        num = len(str(en_r))  # length of en_r
        L = num - 20
        s = ''
        for i in range(L):
            j = random.randint(1, 9)
            s = s + str(j)
        if want_message == 0:
            en_int_ext = str(en_r) + s
        else:
            en_int_ext = s + str(en_r)
        self.r = r
        return en_int_ext, num

    def de_message(self,want_message,message_miwen):
        de_messages = []
        for message in message_miwen:
            key = str(self.r) + 'lianqiao love study'
            de_msg = self.str_xor(message,str(key))
            de_messages.append(de_msg)
        return de_messages[int(want_message)]


def main():
    pk = []
    bob = Bob(45)
    # 以元组形式定义一个 IP 地址和端口
    ip_port = ('127.0.0.1',9998)
    # 创建对象并绑定 IP 地址开始监听
    sk = socket.socket()
    sk.connect(ip_port)
    sk.sendall('我是接收方bob，请求通信，执行协议.....'.encode())
    e = sk.recv(1024).decode()
    pk.append(int(e))
    n = sk.recv(1024).decode()
    pk.append(int(n))

    want_message = random.randint(0,1)
    en_int_ext, num = bob.random_encrypt(want_message, pk)
    sk.sendall(bytes(str(en_int_ext).encode()))
    sk.sendall(bytes(str(num).encode()))

    m_0 = sk.recv(1024).decode()
    m_1 = sk.recv(1024).decode()
    print(sk.recv(1024).decode())
    messages = []
    messages.append(m_0)
    messages.append(m_1)
    m = bob.de_message(want_message,messages)
    print('要的第{}个消息'.format(want_message),m)
    sk.sendall('我是接收方bob，协议执行,再见'.encode())
    sk.close()


if __name__=='__main__':
    main()
