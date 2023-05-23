import random
import socket
import  time

class Bob:
    def __init__(self,p):
        self.p = p

    def str_xor(self, s: str, k: str):
        k = (k * (len(s) // len(k) + 1))[0:len(s)]
        return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s, k))

    def random_encrypt(self, pk):
        self.want_message = random.randint(0,1)
        # self.want_message = 1
        r = random.randint(2 ** 127, 2 ** 128)  # generate a big random num
        self.r = r
        if self.want_message == 0:
            e0 = pk[0]
            n0 = pk[1]
            en_r0 = pow(r, e0, n0)  # encrypt
            return en_r0
        else:
            e1 = pk[2]
            n1 = pk[3]
            en_r1 = pow(r, e1, n1)
            return en_r1

    def de_message(self,message_miwen):
        de_messages = []
        for message in message_miwen:
            key = str(self.r) + 'dihuang love study'
            de_msg = self.str_xor(message, str(key))
            de_messages.append(de_msg)
        return de_messages[int(self.want_message)]


def main():
    pk = []
    bob = Bob(45)
    # 以元组形式定义一个 IP 地址和端口
    ip_port = ('127.0.0.1',9998)
    # 创建对象并绑定 IP 地址开始监听
    sk = socket.socket()
    sk.connect(ip_port)
    sk.sendall('我是接收方bob，请求通信，执行协议.....\n'.encode())
    print(sk.recv(1024).decode())

    e0 = sk.recv(1024).decode()
    pk.append(int(e0))
    n0 = sk.recv(1024).decode()
    pk.append(int(n0))
    e1 = sk.recv(1024).decode()
    pk.append(int(e1))
    n1 = sk.recv(1024).decode()
    pk.append(int(n1))
    # print('------')
    sk.sendall('我是接收方bob，rsa公钥接收完毕，即将发送对称公钥.....\n'.encode())
    print(sk.recv(1024).decode())

    en_r = bob.random_encrypt( pk)
    sk.sendall(bytes(str(en_r).encode()))

    m_0 = sk.recv(1024).decode()
    m_1 = sk.recv(1024).decode()
    print(sk.recv(1024).decode())
    messages = []
    messages.append(m_0)
    messages.append(m_1)
    m = bob.de_message(messages)
    print('我是bob，在本地展示，要的第{}个消息'.format(bob.want_message),m)
    sk.sendall('我是接收方bob，协议完毕，我已经获取到消息，再见alice!\n'.encode())
    sk.close()


if __name__=='__main__':
    main()
