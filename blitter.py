import redis
import time
import random
import struct
import cPickle

from pixelpusher import pixel, build_strip, send_strip

import sys

IP = '192.168.0.99'
PORT = 9897
    
MAX = 255
MID = 128
OFF = 0

FRAME_MASTER = 'master'
FRAME_KEY = 'frame'

def prep_client(client):
    client.delete(FRAME_KEY)

def main():
    client = redis.Redis()
    prep_client(client)

    pixel_width = 120
    delay = 0.0025

    while True:
        frame_name, frame = client.blpop(FRAME_KEY)
        frame = cPickle.loads(frame)
        lines = []
        
        lines.append(frame[0:pixel_width])
        lines.append(frame[pixel_width:pixel_width*2])
        lines.append(frame[pixel_width*2:pixel_width*3])
        lines.append(frame[pixel_width*3:pixel_width*4])
        lines.append(frame[pixel_width*4:pixel_width*5])
        lines.append(frame[pixel_width*5:pixel_width*6])
        lines.append(frame[pixel_width*6:pixel_width*7])
        lines.append(frame[pixel_width*7:pixel_width*8])

        for index in range(0, 4):
            s = struct.pack('!xxxxB', index) + ''.join(lines[index*2]) + ''.join(reversed(lines[(index*2)+1]))
            send_strip(''.join(s), (IP, PORT))
            time.sleep(delay)
    
if __name__ == "__main__":
    main()
