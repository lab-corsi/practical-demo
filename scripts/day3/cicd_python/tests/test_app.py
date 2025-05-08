# test_app.py

import threading
import socket
import time

import pytest
import requests
from http.server import HTTPServer

from app import SimpleHandler

@pytest.fixture(scope="module")
def http_server_port():
    # Trova una porta libera
    sock = socket.socket()
    sock.bind(("localhost", 0))
    port = sock.getsockname()[1]
    sock.close()

    # Avvia il server in un thread separato
    server = HTTPServer(("localhost", port), SimpleHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    # Attendi un attimo che il server sia up
    time.sleep(0.5)

    yield port

    # Shutdown del server
    server.shutdown()
    thread.join()

def test_root_get(http_server_port):
    url = f"http://localhost:{http_server_port}/"
    resp = requests.get(url)
    assert resp.status_code == 200
    assert resp.text == "Hello from Python HTTP server!"

def test_other_path(http_server_port):
    # Il comportamento è lo stesso su qualsiasi path
    url = f"http://localhost:{http_server_port}/foo/bar"
    resp = requests.get(url)
    assert resp.status_code == 200
    assert "Hello from Python HTTP server!" in resp.text
