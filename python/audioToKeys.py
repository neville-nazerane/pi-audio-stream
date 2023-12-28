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


def stream_until_seconds(stream: pyaudio.Stream, seconds):
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


def keep_streaming():
    while CURRENT_KEY != 'DEAD':
        if CURRENT_KEY != 'NADA':
            data = stream.read(CHUNK, exception_on_overflow=False)
            requests.post(f'{SERVER_URL}/audioToSpecificFile/{CURRENT_KEY}', data=data)
        

def show_me_the_money():
    for _ in range(60):
        requests.get(f'{SERVER_URL}/showthis/{CURRENT_KEY}')
        # print(f"function 1 says {CURRENT_KEY}")
        time.sleep(1)

def keep_reading_file():
    global CURRENT_KEY
    with open("keywords.txt", "r") as file:
        for line in file:
            line = line.strip();
            curr = CURRENT_KEY = f"{str(uuid.uuid4())}__{line.replace(' ', '_')}"
            input(line)
            CURRENT_KEY = 'NADA'
            requests.post(f'{SERVER_URL}/completeFile/{curr}')


fileReadThread = threading.Thread(target=keep_reading_file)
streamThread = threading.Thread(target=keep_streaming)

fileReadThread.start()
streamThread.start()

fileReadThread.join()
streamThread.join()

print('yah we done here')

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


stream.stop_stream()
stream.close()
audio.terminate()
