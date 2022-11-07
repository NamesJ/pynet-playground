import socket
import sys
import json
import logging
import threading

from .. import server
from .. import util


class ProxyServer:
    def __init__(self, ip='127.0.0.1', port=29171):
        self.server = server.TCPServer(ip, port)

    def run(self):
        logging.debug('Listening for clients')
        self.server.listen(5)
        while True:
            client, client_addr = self.server.accept()
            logging.debug('New client connected: {}'.format(client_addr))
            t = threading.Thread(target=self.handle, args=(client,client_addr),
                                 daemon=True)
            t.start()

    def handle(self, client, client_addr):
        server = None
        while True:
            received = client.recv(1024).decode()
            if received == 'exit':
                break
            try:
                proxy_request = json.loads(received)
            except json.JSONDecodeError:
                logging.error('Received non-JSON request: {}'.format(received))
                return
            logging.debug('Received proxy request: {}'.format(proxy_request))
            # Unpack client request
            ip = proxy_request['ip']
            port = int(proxy_request['port'])
            request = proxy_request['request'].encode()
            # Forward request to desired host
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect((ip, port))
            logging.debug('Connecting to host ({}, {})'.format(ip, port))
            server.sendall(request)
            logging.debug('Forwarded client request to host')
            # Get response back from host
            response = server.recv(1024)
            logging.debug('Received response from host: {}'.format(response))
            # Send host response back to client
            client.sendall(response)
            logging.debug('Forwarded host response to client')
        # Cleanup
        if server: server.close()


def main():
    util.config_logging('proxy-server.log', stream_level=logging.DEBUG)
    ps = ProxyServer()
    ps.run()


if __name__ == '__main__':
    main()
