import socket
import sys
import json
import logging
import threading
import pyaudio

from .. import server
from .. import util
from . import util as audio_util

'''
Current assumptions:
    - Only one client allowed to be connected
'''

class AudioServer:
    def __init__(self, ip='127.0.0.1', port=29471):
        self.server = server.UDPServer(ip, port)
        self.client = None
        self.audio = pyaudio.PyAudio()


    def run(self):
        logging.debug('Listening for clients')
        data, self.client = self.server.recvfrom(1024)
        logging.debug('New client connected: {}'.format(self.client))
        logging.debug('Client sent data: {}'.format(data))
        self.stream = audio_util.open_input_stream(self.audio, self.callback)
        # Now that self.client is set, data should start streaming
        # As of now, same as 'while True'
        while self.client:
            pass

    def callback(self, input_data, frame_count, time_info, flags):
        # Send data to client
        #logging.debug('Type of input_data: {}'.format(type(input_data)))
        #logging.debug('Size of input_data: {}'.format(sys.getsizeof(input_data)))
        if self.client:
            self.server.sendto(input_data, self.client)
        return input_data, pyaudio.paContinue


def main():
    util.config_logging('audio-server.log', stream_level=logging.DEBUG)
    s = AudioServer()
    s.run()


if __name__ == '__main__':
    main()
