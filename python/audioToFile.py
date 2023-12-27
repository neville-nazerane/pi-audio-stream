import pyaudio
import requests
import sys
import uuid


# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 4
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 10
SERVER_URL = f"http://{sys.argv[1]}"

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)


print("Recording and streaming...")

def keep_streaming(stream):
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        yield data

def audio_stream_generator(stream):
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS + 1)):
        data = stream.read(CHUNK)
        yield data

guid = str(uuid.uuid4())  

for i in range(6 * 4):
    try:

        response = requests.post(f'{SERVER_URL}/audioToSpecificFile/{guid}', data=audio_stream_generator(stream))

        if response.status_code == 200:
            print(f"Streaming {i} completed successfully.")
        else:
            print(f"Server returned status code: {response.status_code}")

    except requests.Timeout:
        print("Request timed out")

    except Exception as e:
        print(f"An error occurred: {e}")


# Stop and close the stream 
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
audio.terminate()

requests.post(f'{SERVER_URL}/completeFile/{guid}')

print("Finished recording and streaming.")
