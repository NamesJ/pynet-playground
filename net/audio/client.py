import socket
import sys
import json
import logging
import threading
import pyaudio

from .. import util
from . import util as audio_util


class AudioClient:
    def __init__(self, ip='127.0.0.1', port=29471):
        self.server = (ip, port)
        self.audio = pyaudio.PyAudio()

    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Content of intro message doesn't matter, it just kicks things off
        # So here we tell the server what to do with the data
        intro = 'Pour it on me bb'.encode()
        self.s.sendto(intro, self.server)
        logging.debug('Sent introduction message to server: {}'.format(intro))
        self.stream = audio_util.open_output_stream(self.audio)
        logging.debug('Starting stream and streaming audio from server')
        while True:
            data, addr = self.s.recvfrom(audio_util.AUDIO_PACKET_SIZE)
            #logging.debug('Received data from server: {}'.format(data))
            self.stream.write(data)



def main():
    '''
    This example assumes that an instance of net.dns.server.DNSServer will be
    running on localhost at port 29371 (default).
    '''
    util.config_logging('audio-client.log', stream_level=logging.DEBUG)
    c = AudioClient()
    t = threading.Thread(target=c.run, daemon=True)
    t.start()
    t.join()


if __name__ == '__main__':
    main()
