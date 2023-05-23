import random
import socket
import  time
import rsa
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

    def encrypt_message(self,gk):
        r = random.randint(2 ** 127, 2 ** 128)
        gr = pow(self.g, r, self.p)

        pk_list = []      # 计算密钥
        for i in range(self.n):
            x = gk[i: len(gk) - self.n + i ]
            x = int(x)
            C_r = pow(x,r,self.p)
            pk_list.append(C_r)

        messages = self.gen_messages()
        message_miwen = []  # store ciphertext
        for i in range(self.n):
            en_message = self.str_xor(messages[i], str(pk_list[i]) + 'lianqiao love study' )  # encrypt
            message_miwen.append(en_message)
        return message_miwen, gr


def main():
    n = int(input('please input n:\n'))
    p = 320272671238909464478547551273142272013
    g = 317784432528923075244970559336684737753
    alice = Alice(p,g,n)
    ip_port = ('127.0.0.1',9998)
    # 创建对象并绑定 IP 地址开始监听
    sk = socket.socket()
    sk.bind(ip_port)
    sk.listen(5)
    conn,addr = sk.accept() # accept 属于阻塞式，没有收到连接请求就不会继续向下运行
    # 接收客户端发来的消息
    print(conn.recv(1024).decode())
    conn.sendall('OK, I\'m alce, please send the key.......\n'.encode())
    gk = conn.recv(1024).decode()
    conn.sendall('OK, I\'m alce, prepare to send the ciphertext, ready to get it! bob, OK?......\n'.encode())
    message_enc, gr = alice.encrypt_message(gk)
    json_message_enc = json.dumps(message_enc).encode()
    conn.sendall(json_message_enc)
    conn.sendall(str(gr).encode())
    conn.sendall('I\'alice，ciphertext already send to you，please give me a signal......\n'.encode())
    print(conn.recv(1024).decode())
    # 关闭连接
    conn.close()


if __name__=='__main__':
    main()