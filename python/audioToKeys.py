import pyaudio
import requests
import sys
import uuid


# Settings
SERVER_URL = f"http://{sys.argv[1]}"

# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 4
RATE = 44100
CHUNK = 1024


# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)



with open("keywords.txt", "r") as file:
    for line in file:
        input(line.strip())
        # input("Press Enter to ...")
        # requests.post(f'{SERVER_URL}/audioToSpecificFile/{guid}', data=audio_stream_generator(stream))



# Stop and close the stream 
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
audio.terminate()
