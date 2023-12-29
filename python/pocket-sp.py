import os
from pocketsphinx import LiveSpeech, get_model_path

# Set up the paths for PocketSphinx model and dictionary
model_path = get_model_path()

# Define the list of keywords to detect
keywords = [("batman", 20), ("smarty", 20), ("dyslexia", 20)]  # Update with your keywords and thresholds
keywords_str = "\n".join([f"{word} /1e-{threshold}/" for word, threshold in keywords])

# Configure speech recognition
speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(model_path, 'en-us/en-us'),
    lm=False,
    dic=os.path.join(model_path, 'en-us/cmudict-en-us.dict'),
    kws_threshold=1e-20,
    kws=keywords_str
)

# Process audio input and check for keywords
print("Listening for keywords...")
for phrase in speech:
    for word in phrase.segments(detailed=True):
        if word[0] in keywords:
            print(f"Keyword Detected: {word[0]}")
