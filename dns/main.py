import socketserver
import sys

from server import Server

if __name__ == '__main__':
    with socketserver.UDPServer(('0.0.0.0', int(sys.argv[1])), Server) as server:
        server.serve_forever()
    # Server(int(sys.argv[1]), sys.argv[2]).serve()
