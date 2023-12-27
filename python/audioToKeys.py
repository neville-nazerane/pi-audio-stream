from calendar import c
import pyaudio
import requests
import sys
import uuid
import threading
import time

# Settings
SERVER_URL = f"http://{sys.argv[1]}"

# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 4
RATE = 44100
CHUNK = 1024




def record_audio(stop_event):
    frames = []
    while not stop_event.is_set():
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
    return frames


def stream_until_seconds(stream, seconds):
    for _ in range(0, int(RATE / CHUNK * seconds + 1)):
        data = stream.read(CHUNK)
        yield data

# def stream_until_seconds(stream, seconds):
#     frames = []
#     for _ in range(0, int(RATE / CHUNK * seconds)):
#         data = stream.read(CHUNK)
#         frames.append(data)
#     return frames



audio = pyaudio.PyAudio()

input("Hit enter to begin")


with open("keywords.txt", "r") as file:
    for line in file:

        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        
        start_time = time.time()
        input(line.strip())
        elapsed_time = time.time() - start_time

        print(f'gonna take {elapsed_time}')
        streamData = stream_until_seconds(stream, elapsed_time)
        
        guid = str(uuid.uuid4()) 
        
        # save on server
        requests.post(f'{SERVER_URL}/audioToSpecificFile/{guid}', data=streamData)
        requests.post(f'{SERVER_URL}/completeFile/{guid}')

        stream.stop_stream()
        stream.close()


audio.terminate()
