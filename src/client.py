# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import socket
import sys

test_message = 'Test message!'


def client(message=test_message):
    infos = socket.getaddrinfo('127.0.0.1', 5001)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]

    client_socket = socket.socket(*stream_info[:3])
    client_socket.connect(stream_info[-1])
    client_socket.sendall(message.encode('utf-8'))
    client_socket.shutdown(socket.SHUT_WR)

    buffered_message = ""
    buffer_length = 8

#----------------listening--------------------
    while True:
        part = client_socket.recv(buffer_length)
        buffered_message += part.decode('utf-8')
        if len(part) == 0:
            break
    print(buffered_message)
    client_socket.close()
    return(buffered_message)


if __name__ == '__main__':
    client(sys.argv[1])
