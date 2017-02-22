# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest
import sys
import os



FAILED_MESSAGES = [
    (u"SET / HTTP/1.1\r\nHost: localhost:5000", NameError),
    (u"GET / HTTP/1.0\r\nHost: localhost:5000", TypeError),
    (u"GET / HTTP/1.1\r\nNo Host", ValueError)
]


ERROR_RESPONSE = [
    ("200", u"HTTP/1.1 200 OK\r\n"),
    ("400", u"HTTP/1.1 400 Bad Request\r\n"),
    ("404", u"HTTP/1.1 404 File Not Found\r\n"),
    ("405", u"HTTP/1.1 405 Method Not Allowed\r\n"),
    ("500", u"HTTP/1.1 500 Internal Server Error\r\n"),
    ("505", u"HTTP/1.1 505 HTTP Version Not Supported\r\n"),
]

SUCCESS_MESSAGE = [(u"GET / HTTP/1.1\r\nHost: localhost:5000", "/")]


URI_RESPONSE = [
    (u"/", ("<!DOCTYPE html>", "")),
    (u"/a_web_page.html", (b"<!DOCTYPE html>", "text/html")),
    (u"/make_time.py", (b"#!/usr/bin/env python\n\n", "text/x-python")),
    (u"/sample.txt", (b"This is a very simple text file", "text/plain")),
    (u"/images/JPEG_example.jpg", (b"\xff\xd8\xff\xe0\x00\x10JFIF", "image/jpeg")),
    (u"/images/sample_1.png", (b"\x89PNG\r\n\x1a\n", "image/png")),
]


def test_response_template():
    from server import response_template
    response = response_template()
    assert 'Content-length: \r\n\r\n' in response


@pytest.mark.parametrize("error, response", ERROR_RESPONSE)
def test_response_check(error, response):
    from server import response_check
    assert response_check(error) == response


CLIENT_MESSAGES = [
    (u"SET / HTTP/1.1\r\nHost: localhost:5000", NameError),
    (u"GET / HTTP/1.0\r\nHost: localhost:5000", TypeError),
    (u"GET / HTTP/1.1\r\nNo Host", ValueError)
]


@pytest.mark.parametrize("error, response", CLIENT_MESSAGES)
def test_parse_request(error, response):
    from server import parse_request
    with pytest.raises(response):
        parse_request(error)


@pytest.mark.parametrize("error, response", SUCCESS_MESSAGE)
def test_parse_request_success(error, response):
    from server import parse_request
    assert parse_request(error) == response


def test_response_ok():
    from server import response_ok
    response = response_ok('test text', 'text/html')
    assert response[2] == 'Content-type: text/html; charset=utf-8\r\n'


@pytest.mark.parametrize("error, resp", ERROR_RESPONSE)
def test_response_err(error, resp):
    from server import response_err
    assert resp in response_err(error)


@pytest.mark.parametrize("req, resp", URI_RESPONSE)
def test_resolve_uri(req, resp):
    from server import resolve_uri
    body_type = resolve_uri(req, '')
    assert resp[0] in body_type[0]
    assert resp[1] == body_type[1]
