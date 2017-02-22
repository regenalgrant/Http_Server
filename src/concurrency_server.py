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


def response_err(req_type):
    response = response_template()
    response[0] = response_check(req_type)
    response[4] = response_check(req_type)
    return response


def resolve_uri(uri, path='..'):
    """body and type based on uri as a tuple."""
    path_to_root = os.path.join(path, 'webroot', uri[1:])
    print("path to root: ", path_to_root)
    file_type = ""
    if os.path.isfile(path_to_root):
        print("is a file")
        filepath = io.open(path_to_root, 'rb')
        print("filepath :", filepath)
        body = filepath.read()
        print("body", body)
        file_type = mimetypes.guess_type(uri)
        print("file_type :", file_type[0])
        filepath.close()
        return body, file_type[0]
    elif os.path.isdir(path_to_root):
        print("is a directory", path_to_root)
        return build_file_structre_html(path_to_root), file_type
    else:
        raise OSError


def send_response(conn, response):
    for c in response:
        if isinstance(c, str):
            conn.send(c.encode('utf-8'))
        else:
            conn.send(c)

def server(conn, address):
    try:
        while True:
            # listen on socket
            client_request = handle_listening(conn)
            print(client_request)
            try:
                uri = parse_request(client_request)
                print('parsed uri: ', uri)
            except ValueError:
                client_response = response_err("400")
            except TypeError:
                client_response = response_err("505")
            except NameError:
                client_response = response_err("405")
            try:
                body, file_type = resolve_uri(uri)
                print("body :", body)
                print("file_type :", file_type)
                client_response = response_ok(body, file_type)
            except OSError:
                client_response = response_err("404")
            send_response(conn, client_response) # Send the message
            conn.close()
            break
    except KeyboardInterrupt:
        if conn is not None:
            conn.close()
        print('connection closed')
    finally:
        server_socket.close()
        print('server closed')
