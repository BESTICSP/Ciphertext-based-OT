import random
import socket
import  time

class Bob:
    def __init__(self,p,g):
        self.p = p
        self.g = g

    def str_xor(self, s: str, k: str):
        k = (k * (len(s) // len(k) + 1))[0:len(s)]
        return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s, k))

    def gen_key(self,gk):
        self.want_message = random.randint(0,1)
        k = random.randint(2 ** 127, 2 ** 128)  # generate a big random num
        self.k = k
        gk = pow(self.g, k, self.p)
        msg = ''
        for i in range(0, 30):
            msg = msg + str(random.randint(1, 9))
        if self.want_message == 0:
            gk = str(gk) + msg
        else:
            gk = msg + str(gk)
        return gk

    def de_message(self,messages,gr):
        gr = int(gr)
        key = pow(gr,self.k,self.p)
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
    ip_port = ('127.0.0.1',9998)
    # 创建对象并绑定 IP 地址开始监听
    sk = socket.socket()
    sk.connect(ip_port)
    sk.sendall('I am bob, requesting communication, executing the protocolt.....\n'.encode())
    print(sk.recv(1024).decode())
    gk = bob.gen_key(0)
    sk.sendall(gk.encode())
    print(sk.recv(1024).decode())
    m_0 = sk.recv(1024).decode()
    m_1 = sk.recv(1024).decode()
    messages = []
    messages.append(m_0)
    messages.append(m_1)
    gr =  sk.recv(1024).decode()
    print(sk.recv(1024).decode())
    m = bob.de_message(messages,gr)
    print('要的第{}个消息'.format(bob.want_message),m)
    sk.sendall('I\'m bob, protocol is over, I will close the connect,see you again!\n'.encode())
    sk.close()


if __name__=='__main__':
    main()
