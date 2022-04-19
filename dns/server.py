# this file constructs the frontend of a dns server to serve dns request
import socket
import socketserver
import sys

from dnslib import DNSRecord, RR, QTYPE, CLASS, A

NAME = sys.argv[2]


class Server(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        query, conn = DNSRecord.parse(self.request[0]), self.request[1]

        ans = query.reply()
        for q in query.questions:
            if q.qname == NAME:
                ans.add_answer(RR(q.qname, QTYPE.A, CLASS.IN, 60, A("50.116.41.109")))

        if len(ans.rr) != 0:
            conn.sendto(ans.pack(), self.client_address)

# class Server(object):
#     def __init__(self, port, name):
#         self.port = port
#         self.name = name
#
#         self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self.conn.bind(('0.0.0.0', self.port))
#
#     def serve(self) -> None:
#         while True:
#             self.__handle(self.conn.recvfrom(1024))
#
#     def __handle(self, req) -> None:
#         query, addr = DNSRecord.parse(req[0]), req[1]
#         print(query, addr)
#
#         ans = query.reply()
#         for q in query.questions:
#             if q.qname == NAME:
#                 ans.add_answer(RR(q.qname, QTYPE.A, CLASS.IN, 60, A("50.116.41.109")))
#
#         if len(ans.rr) != 0:
#             self.conn.sendto(ans.pack(), addr)
