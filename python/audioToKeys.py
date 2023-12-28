from calendar import c
import pyaudio
import requests
import sys
import uuid
import threading
import time

# Settings
SERVER_URL = f"http://{sys.argv[1]}"
CURRENT_KEY = 'NADA'

# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 4
RATE = 44100
CHUNK = 1024


def stream_until_seconds(seconds):
    for _ in range(0, int(RATE / CHUNK * seconds + 1)):
        data = stream.read(CHUNK)
        yield data

audio = pyaudio.PyAudio()

input("Hit enter to begin")

stream = audio.open(format=FORMAT, 
                    channels=CHANNELS, 
                    rate=RATE, 
                    input=True, 
                    frames_per_buffer=CHUNK)

def readStream():
    key = CURRENT_KEY
    while key == CURRENT_KEY: # make sure the key at the starting is still the key
        data = stream.read(CHUNK, exception_on_overflow=False)
        yield data

def keep_streaming():
    while CURRENT_KEY != 'DEAD':
        # data = stream.read(CHUNK, exception_on_overflow=False)
        if CURRENT_KEY != 'NADA': 
            requests.post(f'{SERVER_URL}/audioToSpecificFile/{CURRENT_KEY}', data=readStream())
        

def keep_reading_file():
    count = 0
    global CURRENT_KEY
    while True:
        count += 1
        print(count)
        with open("keywords.txt", "r") as file:
            for line in file:
                line = line.strip().split(', ')[0];
                curr = CURRENT_KEY = f"{str(uuid.uuid4())}__{line.replace(' ', '_')}"
                input(line)
                time.sleep(1)
                CURRENT_KEY = 'NADA'
                requests.post(f'{SERVER_URL}/completeFile/{curr}')
    CURRENT_KEY = 'DEAD'


fileReadThread = threading.Thread(target=keep_reading_file)
streamThread = threading.Thread(target=keep_streaming)

fileReadThread.start()
streamThread.start()

fileReadThread.join()
streamThread.join()


# count = 0

# while True:
#     count += 1
#     print(f'Going for {count}...')
#     with open("keywords.txt", "r") as file:
#         for line in file:
#             items = line.strip().split(', ')
        
#             key = items[0]
#             seconds = 4
        
#             if (len(items) > 1):
#                 seconds = int(items[1])
        
#             print(key)

#             guid = f"{str(uuid.uuid4())}__{key.replace(' ', '_')}"  # str(uuid.uuid4()) 
        
#             # heardData = stream_until_seconds(stream, 3)

#             # save on server
#             requests.post(f'{SERVER_URL}/audioToSpecificFile/{guid}', data=stream_until_seconds(seconds))
#             requests.post(f'{SERVER_URL}/completeFile/{guid}')


print('yah we done here')

stream.stop_stream()
stream.close()
audio.terminate()
