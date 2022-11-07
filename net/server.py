import socket
import sys
import json
import logging

from . import util


class TCPServer(socket.socket):
    def __init__(self, ip='', port=28971):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.bind((self.ip, self.port))
        logging.debug('Server bound to ({}, {})'.format(self.ip, self.port))


class UDPServer(socket.socket):
    def __init__(self, ip='', port=28971):
        super().__init__(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = ip
        self.port = port
        self.bind((self.ip, self.port))
        logging.debug('Server bound to ({}, {})'.format(self.ip, self.port))


def main():
    util.config_logging('server.log', logging.DEBUG)
    # Using any of these server IPs will make it visible only on the local machine
    #my_ip = ('localhost', '127.0.0.1')[0]
    # Using any of these will make it visible to the outside world
    my_ip = ('', socket.gethostname())[0]
    my_port = 28971
    server = Server(my_ip, my_port)
    logging.debug('Waiting for client to connect')
    server.listen(5)
    client, client_addr = self.server.accept()
    logging.debug('A new client connected {}'.format(client_addr))
    client.sendall('Hello there!'.encode())
    logging.debug('Disconnected from client {}'.format(client_addr))


    # bind() -- bind to specific ip and port so that it is capable of listening to incoming requests on that ip and port
    # listen() -- puts the server into listening mode allowing server to listen to incoming connections
    # accept() -- initiates a connection with the client
    # close() -- closes the connection with the client


if __name__ == '__main__':
    main()
