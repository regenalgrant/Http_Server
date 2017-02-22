 #-*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest

# the server must be running for these tests

CLIENT_MESSAGES = [
    (u"GET / HTTP/1.1\r\nHost: localhost:5000/\r\n", "HTTP/1.1 200 OK"),
    (u'GET / HTTP/1.1\r\nHost: localhost:5000/a_web_page.html\r\n', u'HTTP/1.1 200 OK'),
    (u'GET / HTTP/1.1\r\nHost: localhost:5000/make_time.py\r\n', u'HTTP/1.1 200 OK'),
    (u'GET / HTTP/1.1\r\nHost: localhost:5000/sample.txt\r\n', u'HTTP/1.1 200 OK'),
    (u'GET / HTTP/1.1\r\nHost: localhost:5000/images/JPEG_example.jpg\r\n', u'HTTP/1.1 200 OK'),
    (u'GET / HTTP/1.1\r\nHost: localhost:5000/images/sample_1.png\r\n', u'HTTP/1.1 200 OK'),
    (u'GET / HTTP/1.1\r\nHost: localhost:5000/images/Sample_Scene_Balls.jpg\r\n', u'HTTP/1.1 200 OK'),
    (u'GET / HTTP/1.1\r\nHost: localhost:5000/images/Sample_Scene_Balls.png\r\n', u'HTTP/1.1 200 OK'),
]


@pytest.mark.parametrize("req, resp", CLIENT_MESSAGES)
def test_client_request(req, resp):
    from client import client
    assert resp in client(req)
