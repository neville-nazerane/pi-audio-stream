import pyaudio
import requests
import sys
import uuid
import threading

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





audio = pyaudio.PyAudio()

input("Hit enter to begin")

stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
with open("keywords.txt", "r") as file:
    for line in file:

        stop_event = threading.Event()
        recorder_thread = threading.Thread(target=record_audio, args=(stop_event,))
        recorder_thread.start()        

        input(line.strip())
        
        stop_event.set()  # Stop recording
        recorder_thread.join()  # Wait for the recording thread to finish

        talkedStream = record_audio(stop_event)  # Get the recorded data
        
        guid = str(uuid.uuid4()) 
        
        # save on server
        requests.post(f'{SERVER_URL}/audioToSpecificFile/{guid}', data=talkedStream)
        requests.post(f'{SERVER_URL}/completeFile/{guid}')


stream.stop_stream()
stream.close()
audio.terminate()
