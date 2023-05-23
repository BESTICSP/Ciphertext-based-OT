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

    def key_gen(self,RSA_bits):
        (pk, sk) = rsa.newkeys(RSA_bits)
        self.pk = pk
        self.sk = sk
        return pk

    def random_decrypt(self,en_int_ext, num,):
        en_int_0 = en_int_ext[0:num]
        en_int_1 = en_int_ext[-num:]
        s1 = pow(int(en_int_0), self.sk.d, self.sk.n)
        s2 = pow(int(en_int_1), self.sk.d, self.sk.n)
        messages = self.gen_messages()
        message0 = messages[0]
        message1 = messages[1]
        message_miwen = []  # store ciphertext
        en_message0 = self.str_xor(message0, str(s1) + 'lianqiao love study' )  # encrypt
        message_miwen.append(en_message0)
        en_message1 = self.str_xor(message1, str(s2) + 'lianqiao love study' )  # decrypt
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
    pk = alice.key_gen(1024)
    conn.sendall(str(pk.e).encode())
    conn.sendall(str(pk.n).encode())

    en_int_ext = conn.recv(1024).decode()
    num = conn.recv(1024).decode()
    message_miwen = alice.random_decrypt(en_int_ext,int(num))

    conn.sendall(str(message_miwen[0]).encode())
    conn.sendall(str(message_miwen[1]).encode())
    conn.sendall('我是alice，密文消息发送完毕，再见'.encode())
    print(conn.recv(1024).decode())
    # 关闭连接
    conn.close()


if __name__=='__main__':
    main()
