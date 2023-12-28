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


def stream_until_seconds(stream: pyaudio.Stream, seconds):
    for _ in range(0, int(RATE / CHUNK * seconds + 1)):
        data = stream.read(CHUNK)
        yield data
        

audio = pyaudio.PyAudio()

input("Hit enter to begin")


def keep_reading_file():
    with open("keywords.txt", "r") as file:
        for line in file:
            line = line.strip();

            key = f"{str(uuid.uuid4())}__{line.replace(' ', '_')}"
            print(key)
            input(line)



keep_reading_file();


# with open("keywords.txt", "r") as file:
#     for line in file:
#         line = line.strip();
        


#         stream = audio.open(format=FORMAT, 
#                             channels=CHANNELS, 
#                             rate=RATE, 
#                             input=True, 
#                             frames_per_buffer=CHUNK)
        
#         # start_time = time.time()
#         # input(line.strip())
#         # elapsed_time = time.time() - start_time

#         # print(f'gonna take {elapsed_time}')
        
#         print(line)

#         guid = f"{str(uuid.uuid4())}__{line.replace(' ', '_')}"  # str(uuid.uuid4()) 
        
#         heardData = stream_until_seconds(stream, 3)

#         # save on server
#         requests.post(f'{SERVER_URL}/audioToSpecificFile/{guid}', data=heardData)
#         requests.post(f'{SERVER_URL}/completeFile/{guid}')

#         stream.stop_stream()
#         stream.close()


audio.terminate()
