import sys
import json
import pickle
# WARNING: "The pickle module is not secure against erroneous or
#  maliciously constructed data"
import socket
import struct

import smallClass


# https://stackoverflow.com/a/17668009
def recv_msg(sock):
    raw_msglen = recvall(sock, 4)
    # raw_msglen = sock.recv(4)
    if not raw_msglen:
        print("didn't get a message length", file=sys.stderr)
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    return recvall(sock, msglen)


def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


def server():
    host = socket.gethostname()
    port = 4848

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))

    s.listen(1)
    client, address = s.accept()
    print("Connection from: " + str(address))

    while True:
        data = client.recv(1024).decode('utf-8')
        if not data:
            break
        print("DATA: "+ data)
        if data == "ping":
            data = "PONG"
        elif data == "incoming":
            data2 = client.recv(1024).decode('utf-8')
        # WIP:
        # elif data == "json":
            # data2 = client.recv(1024).decode('utf-8')
            # c = json.loads(data2, object_hook=smallClass.dict_to_obj)
        elif data == "small pickle":
            data2 = client.recv(1024)
            c = pickle.loads(data2)
            print(type(c))
            print(c)
        elif data == "big pickle":
            data2 = recv_msg(client)
            c = pickle.loads(data2)
            print(type(c))
            print(len(c))
        else:
            data = data.upper()
        client.send(data.encode('utf-8'))
        if data == "incoming":
            client.send(data2.upper().encode('utf-8'))
    client.close()
    s.close()

if __name__ == '__main__':
    server()
