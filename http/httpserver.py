#!/usr/bin/env python

import sys
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
from functools import lru_cache
import requests
from functools import lru_cache

port = int(sys.argv[2])
origin = 'cs5700cdnorigin.ccs.neu.edu'
# binding to all ip address.
host = '0.0.0.0'

cache = dict()


def get_page_from_origin(url):
    print("getting page from origin...")
    response = requests.get(url)
    return response


def get_page(url):
    print("looking up in cache...")
    if url not in cache:
        cache[url] = get_page_from_origin(url)
    return cache[url]


class CDNHTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        url = origin + ":" + str(port) + self.path
        page = get_page(url)
        self.wfile.write(page)

    def terminateConnection(self):
        self.server.shutdown()
        print('HTTP Server shutdown')


def main():
    server_address = ('0.0.0.0', port)
    server = HTTPServer(server_address, CDNHTTP)
    print('Serving on port %s' % port)
    server.serve_forever()
    server.shutdown()


if __name__ == '__main__':
    main()
