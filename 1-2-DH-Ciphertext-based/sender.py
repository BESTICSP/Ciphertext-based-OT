import random
import socket
import  time


class Alice():
    def __init__(self,p,g):
        self.p = p
        self.g = g

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

    def encrypt_message(self,gk):
        r = random.randint(2 ** 127, 2 ** 128)
        gr = pow(self.g, r, self.p)
        key_0 = int(gk[:-30])
        key_1 = int(gk[30:])
        s1 = pow(key_0, r,self.p)
        s2 = pow(key_1, r, self.p)
        messages = self.gen_messages()
        message0 = messages[0]
        message1 = messages[1]
        message_miwen = []  # store ciphertext
        en_message0 = self.str_xor(message0, str(s1) + 'lianqiao love study' )  # encrypt
        message_miwen.append(en_message0)
        en_message1 = self.str_xor( message1, str(s2) + 'lianqiao love study')  # decrypt
        message_miwen.append(en_message1)
        return message_miwen, gr


def main():
    p = 320272671238909464478547551273142272013
    g = 317784432528923075244970559336684737753
    alice = Alice(p,g)
    ip_port = ('127.0.0.1',9998)
    # 创建对象并绑定 IP 地址开始监听
    sk = socket.socket()
    sk.bind(ip_port)
    sk.listen(5)
    # 开始接收消息
    # conn 表示客户端与服务端建立连接后的专有通信线路
    conn,addr = sk.accept() # accept 属于阻塞式，没有收到连接请求就不会继续向下运行
    # 接收客户端发来的消息
    print(conn.recv(1024).decode())
    conn.sendall('OK, I\'m alce, please send the key.......\n'.encode())
    gk = conn.recv(1024).decode()
    conn.sendall('OK, I\'m alce, prepare to send the ciphertext, ready to get it! bob, OK?......\n'.encode())
    message_miwen, gr = alice.encrypt_message(gk)
    conn.sendall(str(message_miwen[0]).encode())
    conn.sendall(str(message_miwen[1]).encode())
    conn.sendall(str(gr).encode())
    conn.sendall('I\'alice，ciphertext already send to you，please give me a signal......\n'.encode())
    print(conn.recv(1024).decode())
    # 关闭连接
    conn.close()


if __name__=='__main__':
    main()