import socket
import sys
import json
import logging
import threading

from .. import server
from .. import util


class DNSServer():
    def __init__(self, ip='127.0.0.1', port=29371):
        self.server = server.TCPServer(ip, port)
        self.mapping = {}
        self.reverse_mapping = {}

    def load_mapping(self, filename):
        with open(filename, 'r') as f:
            self.mapping = json.load(f)
        for name, ip in self.mapping.items():
            self.reverse_mapping[ip] = name

    def run(self):
        logging.debug('Listening for clients')
        self.server.listen(5)
        while True:
            client, client_addr = self.server.accept()
            logging.debug('New client connected: {}'.format(client_addr))
            thrd = threading.Thread(target=self.handle,
                                    args=(client,client_addr),
                                    daemon=True)
            thrd.start()
        logging.debug('end of run()')

    def handle(self, client, client_addr):
        received = client.recv(1024).decode()
        try:
            request = json.loads(received)
        except json.JSONDecodeError:
            log.error('Received non-JSON request: {}'.format(received))
            return
        logging.debug('Received request: {}'.format(request))

        opcode = request['opcode']
        if opcode == 2:
            client.sendall(json.dumps({
                'answer': 'OK'
            }).encode())
            return

        key = request['question']
        if opcode == 0:
            mapping = self.mapping
        elif opcode == 1:
            mapping = self.reverse_mapping

        if key not in mapping:
            response = {
                'rcode': 3,
                'answer': ''
            }
            logging.debug('Answer not found. Sending response: {}'.format(
                    response))
            client.sendall(json.dumps(response).encode())
            return

        answer = mapping[key]
        response = {
            'rcode': 0,
            'answer': answer
        }
        client.sendall(json.dumps(response).encode())
        logging.debug('Answer found. Sending response: {}'.format(response))


def main():
    util.config_logging('dns-server.log', stream_level=logging.DEBUG)
    ns = DNSServer()
    ns.load_mapping('example.dns')
    ns.run()


if __name__ == '__main__':
    main()
