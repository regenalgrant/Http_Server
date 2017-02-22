# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import OrderedDict

import socket
import email.utils
import sys


def response_template():
    return [u"",
            u"" + str("Date: " + email.utils.formatdate(usegmt=True) + "\r\n"),
            u"Content-type: text/html; charset=utf-8\r\n",
            u"Content-length: \r\n\r\n",
            b"Body: "]


def response_check(error):
    response_dict = {
        "200": u"HTTP/1.1 200 OK\r\n",
        "400": u"HTTP/1.1 400 Bad Request\r\n",
        "404": u"HTTP/1.1 404 File Not Found\r\n",
        "405": u"HTTP/1.1 405 Method Not Allowed\r\n",
        "500": u"HTTP/1.1 500 Internal Server Error\r\n",
        "505": u"HTTP/1.1 505 HTTP Version Not Supported\r\n",
    }
    return response_dict[error]

def parse_request(request):
    split_request = request.split('\r\n')
    request_list = split_request[0].split(' ')
    if request_list[0] == 'GET':
        if request_list[2] == 'HTTP/1.1':
            if 'Host: localhost:' in split_request[1]:
                return request_list[1]
            else:
                raise ValueError
        else:
            raise TypeError
    else:
        raise NameError


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

        address = ('127.0.0.1', 5001)
        server_socket.bind(address)
        print("\nserver: ", server_socket)

        server_socket.listen(1)
        print("\nlistening...")

        conn = None

        try:
            while True:
                conn, addr = server_socket.accept()

# -----------------Buffered message recieve ------

                msg_response = response_template()
                buffer_length = 4096
                byte_msg = b''
                while True:
                    part = conn.recv(buffer_length)
                    byte_msg += part

                if len(part) < buffer_length:
                    try:
                        filepath = parse_request(byte_msg.decode('utf-8'))
                    except NameError:
                        pass
                    except TypeError:
                        pass
                    except ValueError:
                        pass
                    print("filepath: ", filepath)

                    if "/" in filepath:
                        msg_response[0] = response_check("200")
                        msg_response[3] = "Content-length: " + str(len(msg_response[4])) + "\r\n\r\n"
                        msg_response[4] = filepath
                        sys.stdout.write(msg_response[4])
                    else:
                        msg_response[0] = response_check(filepath)
                        msg_response[3] = "Content-length: " + str(len(msg_response[4])) + "\r\n\r\n"

                    for c in msg_response:
                        conn.send(c.encode('utf-8'))

#------------------stop listening-----------------
                    break
            conn.close()

        except KeyboardInterrupt:
            if conn is not None:
                conn.close()
            print('connection closed')
        finally:
            server_socket.close()
            print('server closed')



if __name__ == '__main__':
    server()

#--------------create Client ctrl+D to disconnect-----
