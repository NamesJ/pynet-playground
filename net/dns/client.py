import socket
import sys
import json
import logging

from .. import util



class DNSClient:
    def __init__(self, name_ip='127.0.0.1', name_port=29371):
        self.name_ip = name_ip
        self.name_port = name_port
        self.s = None

    def _connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.debug('Socket successfully created')
        self.s.connect((self.name_ip, self.name_port))
        logging.debug('Socket connected to {}:{}'.format(
            self.name_ip, self.name_port))

    def _close(self):
        self.s.close()

    def send_request(self, request):
        result = None
        try:
            self._connect()
            self.s.sendall(json.dumps(request).encode())
            logging.debug('Sent request to server: {}'.format(request))
            result = self.s.recv(1024).decode()
            result = json.loads(result)
            logging.debug('Received response from server: {}'.format(result))
        except socket.error as err:
            logging.error('Something went wrong with error {}'.format(err))
        self._close()
        return result

    def get_status(self):
        # Send a query with opcode 2
        result = self.send_request({ 'opcode': 2 })
        return result

    def lookup_ip(self, ip):
        # Send query with opcode 1
        result = self.send_request({
            'opcode': 1,
            'question': ip
        })
        return result

    def lookup_name(self, name):
        # Send query with opcode 0
        result = self.send_request({
            'opcode': 0,
            'question': name
        })
        return result


def main():
    util.config_logging('dns-client.log', stream_level=logging.DEBUG)
    client = DNSClient()

    cmd = None
    while True:
        user_input = input('>>> ')
        if user_input == 'exit':
            break
        user_input = user_input.split()
        opcode = int(user_input[0])
        if opcode == 0:
            if len(user_input) != 2:
                logging.error('Invalid number of arguments for opcode 0')
                continue
            name = user_input[1]
            print(client.lookup_name(name))
        elif opcode == 1:
            if len(user_input) != 2:
                logging.error('Invalid number of arguments for opcode 1')
                continue
            ip = user_input[1]
            print(client.lookup_ip(ip))
        elif opcode == 2:
            if len(user_input) > 1:
                logging.warning('Opcode 2 does not require a question')
            print(client.get_status())
        else:
            logging.error('Invalid opcode provided: {}'.format(opcode))
            continue



if __name__ == '__main__':
    main()
