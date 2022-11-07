import logging
import sys
import re
import string


def config_logging(filename, file_level=logging.DEBUG,
                   stream_level=logging.INFO):
    file_handler = logging.FileHandler(filename, mode='w')
    file_handler.setLevel(file_level)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(stream_level)

    logging.basicConfig(
        level=min(file_level, stream_level),
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            file_handler,
            stream_handler
        ]
    )


def is_num(s):
    dots = 0
    for c in s:
        if dots > 1:
            return False
        if c == '.':
            dots += 1
            continue
        if c not in string.digits:
            return False
    return True
