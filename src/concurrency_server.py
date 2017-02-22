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
