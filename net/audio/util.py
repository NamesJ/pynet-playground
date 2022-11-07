import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2**14
AUDIO_PACKET_SIZE = CHUNK * 2 + 33


def open_input_stream(audio, callback):
    return audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        stream_callback=callback,
        frames_per_buffer=CHUNK
    )


def open_output_stream(audio):
    return audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=False,
        output=True,
        frames_per_buffer=CHUNK
    )
