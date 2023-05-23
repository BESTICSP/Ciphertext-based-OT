import random
import socket
import  time
import rsa


class Alice():
    def __init__(self,p):
        self.p = p

    def str_xor(self, s: str, k: str):
        k = (k * (len(s) // len(k) + 1))[0:len(s)]
        return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s, k))

    def gen_messages(self):
        messages = []
        m0 = 'this is message 0'
        messages.append(m0)
        m1 = 'this is message 1'
        messages.append(m1)
        return messages

    def key_gen(self,RSA_bits):  # two pair public key
        (pk0, sk0) = rsa.newkeys(RSA_bits)
        (pk1, sk1) = rsa.newkeys(RSA_bits)
        self.pk0 = pk0
        self.sk0 = sk0
        self.pk1= pk1
        self.sk1 = sk1
        return pk0, pk1

    def random_decrypt(self,en_r):
        s1 = pow(en_r, self.sk0.d, self.sk0.n)
        s2 = pow(en_r, self.sk1.d, self.sk1.n)
        messages = self.gen_messages()
        message0 = messages[0]
        message1 = messages[1]
        message_miwen = []  # store ciphertext
        en_message0 = self.str_xor(message0, str(s1) + 'dihuang love study' )  # encrypt
        message_miwen.append(en_message0)
        en_message1 = self.str_xor(message1, str(s2) + 'dihuang love study' )  # decrypt
        message_miwen.append(en_message1)
        return message_miwen


def main():
    ip_port = ('127.0.0.1',9998)
    # 创建对象并绑定 IP 地址开始监听
    sk = socket.socket()
    sk.bind(ip_port)
    sk.listen(5)
    # 开始接收消息
    # conn 表示客户端与服务端建立连接后的专有通信线路
    conn,addr = sk.accept() # accept 属于阻塞式，没有收到连接请求就不会继续向下运行
    # 接收客户端发来的消息
    alice = Alice(89)
    print(conn.recv(1024).decode())
    conn.sendall('我是alice，准备发送rsa公钥，请注意接收.....\n'.encode())
    pk0,pk1 = alice.key_gen(1024)
    conn.sendall(str(pk0.e).encode())
    conn.sendall(str(pk0.n).encode())
    conn.sendall(str(pk1.e).encode())
    conn.sendall(str(pk1.n).encode())
    # print('-------')
    print(conn.recv(1024).decode())

    conn.sendall('我是alice，对称公钥已接收，正在加密消息请稍后.....\n'.encode())
    en_r = conn.recv(1024).decode()
    message_miwen = alice.random_decrypt(int(en_r))

    conn.sendall(str(message_miwen[0]).encode())
    conn.sendall(str(message_miwen[1]).encode())
    conn.sendall('我是alice，密文消息发送完毕，再见\n'.encode())
    print(conn.recv(1024).decode())
    # 关闭连接
    conn.close()


if __name__=='__main__':
    main()