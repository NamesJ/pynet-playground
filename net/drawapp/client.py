import socket
import sys
import json
import logging
import string
import re

from .. import util


def parse_args(user_input):
    args = user_input.split()
    is_valid = True
    cmd = args[0]
    cmd_args = []
    cmd_kwargs = {}
    for arg in args[1:]:
        if '=' in arg: # kwarg
            key, val = kwargs.split('=')
            if (re.findall('(?==)') > 1
                or len(key) < 1
                or len(val) < 1):
                msg = 'Invalid kwarg passed {}'
                logging.warning(msg.format(arg))
                is_valid = False
                break
            if util.is_num(val):
                if '.' in val:
                    val = float(val)
                else:
                    val = int(val)
            cmd_kwargs[key] = val
        else: # arg
            if util.is_num(arg):
                if '.' in arg:
                    arg = float(arg)
                else:
                    arg = int(arg)
            cmd_args.append(arg)
    return is_valid, cmd, tuple(cmd_args), cmd_kwargs


class DrawAppClient:
    def __init__(self, draw_ip='127.0.0.1', draw_port=29271):
        self.draw_ip = draw_ip
        self.draw_port = draw_port
        self.config_options = None
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.debug('Socket successfully created')

        self.s.connect((self.draw_ip, self.draw_port))
        logging.debug('Socket connected to {}:{}'.format(
            self.draw_ip, self.draw_port))

        # Receive server info (1024 bytes)
        received = self.s.recv(1024)
        try:
            self.draw_server_options = json.loads(received)
            logging.debug('Received: {}'.format(self.draw_server_options))
        except json.JSONDecodeError:
            logging.error('Received non-JSON data for server options')
            self.close()
            sys.exit()


    def send_command(self, name, *args, **kwargs):
        command = { 'name': name }
        if len(args): command['args'] = list(args)
        if len(kwargs): command['kwargs'] = kwargs
        self.s.sendall(json.dumps(command).encode())

    def test_run(self):
        try:
            '''
            # Send config options message to server
            self.draw_config_options = {
                'width': self.draw_server_options['max_width'],
                'height': self.draw_server_options['max_height']
            }
            self.s.sendall(json.dumps(self.draw_config_options).encode())
            logging.debug('Sent config options to draw server')
            '''

            # Send 2 circle drawing messages to server then disconnect
            self.send_command('create_oval', 60, 60, 120, 210)
            logging.debug('Sent circle draw message to server')

            # Receive result from server
            result = self.s.recv(1024)
            logging.debug('Result from server: {}'.format(result))

            self.send_command('create_oval', 200, 200, 320, 310)
            logging.debug('Sent circle draw message to server')

            # Receive result from server
            result = self.s.recv(1024)
            logging.debug('Result from server: {}'.format(result))

            # Send exit message
            self.s.sendall('exit'.encode())
        except socket.error as err:
            logging.error('Socket creation failed with error {}'.format(err))
            sys.exit()
        finally:
            self.close()

    def exit(self):
        self.s.sendall('exit'.encode())

    def close(self):
        self.s.close()

    def recv_result(self):
        result = self.s.recv(1024).decode()
        return result

    def run_cmd(self, cmd, *args, **kwargs):
        self.send_command(cmd, *args, **kwargs)
        return self.recv_result()


def main():
    util.config_logging('drawapp-client.log', stream_level=logging.DEBUG)
    client = DrawAppClient()

    cmd = None
    while True:
        user_input = input('>>> ')
        if user_input == 'get on with it':
            # Just do a bunch of ovals
            rng = range(50, 400, 50)
            for x0 in range(50, 400, 50):
                for x1 in range(50, 400, 50):
                    for y0 in range(x0, 400, 50):
                        for y1 in range(y0, 400, 50):
                            args = (x0, y0, x1, y1)
                            result = client.run_cmd('create_oval', *args)
                            logging.info('Result: {}'.format(result))
            user_input = 'exit'
        is_valid, cmd, args, kwargs = parse_args(user_input)
        if not is_valid:
            continue
        try:
            if cmd == 'exit':
                client.exit()
                break
            result = client.run_cmd(cmd, *args, **kwargs)
            logging.info('Result: {}'.format(result))
        except ConnectionResetError as err:
            logging.error('Lost connection to server')
            break
    client.close()



if __name__ == '__main__':
    main()
