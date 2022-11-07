import socket
import sys
import json
import logging

from .. import util


class ProxyClient:
    def __init__(self, proxy_ip='127.0.0.1', proxy_port=29171):
        self.proxy_ip = proxy_ip
        self.proxy_port = proxy_port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.proxy_ip, self.proxy_port))

    def close(self):
        self.s.close()

    def send_request(self, ip, port, request):
        result = None
        try:
            proxy_request = json.dumps({
                'ip': ip,
                'port': port,
                'request': request.decode()
            }).encode()
            self.s.sendall(proxy_request)
            logging.debug('Sent request to server: {}'.format(proxy_request))
            #self.s.sendall(request)
            #logging.debug('Forwarded request to server: {}'.format(request))
            response = self.s.recv(1024)
            logging.debug('Received response from server: {}'.format(response))
        except socket.error as err:
            logging.error('Something went wrong with error {}'.format(err))
        else:
            return response


def main():
    '''
    This example assumes that an instance of net.dns.server.DNSServer will be
    running on localhost at port 29371 (default).
    '''
    util.config_logging('proxy-client.log', stream_level=logging.DEBUG)
    client = ProxyClient()
    dns_request = json.dumps({
        'opcode': 0,
        'question': 'www.google.com'
    }).encode()
    for i in range(10):
        response = client.send_request('127.0.0.1', 29371, dns_request)
        response = json.loads(response.decode())
        logging.info('Received response from proxy server: {}'.format(response))
        time.sleep(0.1)
    client.close()


if __name__ == '__main__':
    import time
    main()
