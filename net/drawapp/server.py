import socket
import sys
import json
import logging
import tkinter as tk
#from multiprocessing.connection import Listener
import threading

from .. import server
from .. import util



class DrawAppServer:
    def __init__(self, ip='127.0.0.1', port=29271, width=600, height=400,
                 version=1.0):
        #self.ip = ip
        #self.port = port
        self.width = width
        self.height = height
        self.version = version
        self.running = True # use to have socket close if program is closing
        self.server = server.TCPServer(ip, port)
        self.th_listen = threading.Thread(target=self.listen, daemon=True)
        self.th_listen.start()

        self.win = tk.Tk()
        self.win.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.win.geometry('{}x{}'.format(self.width, self.height))
        self.c = tk.Canvas(self.win, width=self.width, height=self.height)
        self.c.pack()
        self.win.mainloop()

    def on_closing(self):
        self.running = False
        # Wait for server socket to be closed
        self.win.destroy()
        return
        if self.server.fileno() != -1:
            print(self.server.fileno())
        while self.server.fileno() != -1:
            pass
        self.win.destroy()

    def listen(self):
        self.server.listen(5)
        while True:
            if not self.running:
                logging.debug('Running is False. Closing server')
                self.server.close()
                break
            client, client_addr = self.server.accept()
            logging.debug('A new client connected {}'.format(client_addr))
            th_client = threading.Thread(target=self.handle, args=(client,),
                    daemon=True)
            th_client.start()
            logging.debug('Disconnected from client {}'.format(client_addr))

    def handle(self, client):
        # Send server info
        client.send(json.dumps({
            'width': self.width,
            'height': self.height
        }).encode())
        while True:
            if not self.running:
                logging.debug('Running is False. Disconnecting from client')
                break
            received = client.recv(1024).decode()
            logging.debug('Received from client: {}'.format(received))
            if received == 'exit':
                # If user sends exit command, stop handling commands
                if received == 'exit':
                    logging.debug('User requested to exit')
                    break
            try:
                command = json.loads(received)
            except json.JSONDecodeError:
                logging.warning('Received a non-JSON message from client')
            else:
                logging.debug('Received command from client: {}'.format(command))
                # Get canvas method and return
                result = self.call(command)
                #method = getattr(self.app.c, method_name)
                #result = method(*method_args)

                # Send results to client
                client.send(json.dumps(result).encode())


    def call(self, command):
        '''
        For the time being, the only commands accepted are methods to be called
        on the canvas object
        '''
        name = command['name']
        if not hasattr(self.c, name):
            logging.error('Invalid method name provided: {}'.format(name))
            return None
        method = getattr(self.c, name)
        result = None
        if 'args' not in command and 'kwargs' not in command: # neither
            result = method()
        if 'args' in command and 'kwargs' not in command: # args only
            result = method(*command['args'])
        if 'args' not in command and 'kwargs' in command: # kwargs only
            result = method(**command['kwargs'])
        if 'args' in command and 'kwargs' in command: # both
            result = method(*command['args'], **command['kwargs'])
        return result



def main():
    util.config_logging('drawapp-server.log', stream_level=logging.DEBUG)
    # Use default ip='' and port=28971
    # ip=socket.gethostbyname(socket.gethostname())
    app = DrawAppServer()


if __name__ == '__main__':
    main()
