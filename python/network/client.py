import json
import pickle
# WARNING: "The pickle module is not secure against erroneous or
#  maliciously constructed data"
import socket
import struct

import smallClass


def send_msg(sock, msg):
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)


def client():
    host = socket.gethostname()
    port = 4848

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    message = input('-> ')

    while message != 'q':
        s.send(message.encode('utf-8'))
        if message == "incoming":
            s.send("\nlots more text!".encode('utf-8'))
        # elif message == "json":
            # cj = json.dumps(c, default=smallClass.obj_to_dict, indent=4)
            # s.sendall(cj.encode('utf-8'))
        elif message == "small pickle":
            c = smallClass.OuterClass()
            cp = pickle.dumps(c)
            s.sendall(cp)
        elif message == "big pickle":
            l = list(range(0, 2000))
            lp = pickle.dumps(l)
            send_msg(s, lp)
        data = s.recv(1024).decode('utf-8')
        print("DATA: " + data)
        message = input('-> ')
    s.close()

if __name__ == '__main__':
    client()
