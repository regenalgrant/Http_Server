# -*- coding: utf-8 -*-

import pytest


# ----------the server has to work to test

def test_client_shorter_than_buffer(capfd):
    from client import client
    client("test_string")
    out, err = capfd.readouterr()
    assert "HTTP/1.1 200 OK" in out

def test_response_ok():
  from server import response_ok
  ok_output = response_ok()
  assert ok_output[0] == "HTTP/1.1 200 OK\n"
  assert ok_output[2] == "Content-type: text/html; charset=utf-8\n"


def test_response_error():
  from server import response_error
  error_output = response_error()
  assert error_output[0] == "HTTP/1.1 500 Internal Server Error\n"
  assert error_output[2] == "Content-type: text/html; charset=utf-8\n"
