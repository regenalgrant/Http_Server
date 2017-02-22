from __future__ import unicode_literals

import socket
import email.utils
import mimetypes
import io
import os


def build_file_structre_html(directory):
    print(directory)
    body = "<!DOCTYPE html>\r\n<html>\r\n<ul>\r\n<body>\r\n<h1>Code Fellows</h1>\r\n"
    for item in os.listdir(directory):
        print(item)
        if os.path.isdir(os.path.join(directory, item)):
            body += "<li><a href=\"{}/\">{}</a></li>\r\n".format(item, item)
        else:
            body += "<li><a href=\"{}\">{}</a></li>\r\n".format(item, item)
    body += "</ul>\r\n</body>\r\n</html>"
    return body


def response_template():
    return [u"",
            u"" + str("Date: " + email.utils.formatdate(usegmt=True) + "\r\n"),
            u"Content-type: text/html; charset=utf-8\r\n",
            u"Content-length: \r\n\r\n",
            u"Body: "]


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
            if 'Host: 127.0.0.1:' in split_request[1]:
                return request_list[1]
            else:
                raise ValueError # 400
        else:
            raise TypeError # 505
    else:
        raise NameError # 405


def handle_listening(conn):
    buffer_length = 4096
    byte_msg = b''
    decoded_msg = ""
    while True:
        part = conn.recv(buffer_length)
        byte_msg += part
        if len(part) < buffer_length:
            decoded_msg = byte_msg.decode('utf-8')
            break
    return decoded_msg


def response_ok(body, req_type):
    response = response_template()
    response[0] = response_check("200")
    response[2] = u"Content-type: " + req_type + "; charset=utf-8\r\n"
    response[4] = body
    return response
