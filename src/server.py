# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import OrderedDict

import socket
import email.utils
import sys


def response_ok():
    return ["HTTP/1.1 200 OK\n",
            str("Date: " + email.utils.formatdate(usegmt=True) + "\n"),
            "Content-type: text/html; charset=utf-8\n",
            "Content-length: \n\n",
            "Body: "]


def response_error():
    return ["HTTP/1.1 500 Internal Server Error\n",
            str("Date: " + email.utils.formatdate(usegmt=True) + "\n"),
            "Content-type: text/html; charset=utf-8\n"
            ]


def server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP,)
        print("\nserver: ", server_socket)

        address = ('127.0.0.1', 5000)
        server_socket.bind(address)
        print("\nserver: ", server_socket)

        while True:
            server_socket.listen(1)
            print("\nlistening...")

            conn, addr = server_socket.accept()

            # Receive the buffered message
            msg_response = response_ok()
            buffer_length = 8
            while True:
                part = conn.recv(buffer_length)
                msg_response[4] += part.decode('utf-8')

                if len(part) < buffer_length:
                    # Get length
                    msg_response[3] = "Content-length: " + str(len(msg_response[4])) + "\n\n"
                    sys.stdout.write(msg_response[4])
                    for c in msg_response:
                        conn.send(c.encode('utf-8'))
                    break
            conn.close()

    except KeyboardInterrupt:
        conn.close()
        print('connection closed')
        server.close()
        print('server closed')


if __name__ == '__main__':
    server()

#--------------create-Client-ctrl+D-to-disconnect-----
