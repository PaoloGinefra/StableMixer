import sounddevice as sd
import numpy as np


# Parameters
RATE = 48000  # Default sample rate for the chosen device
CHANNELS = 2
CHUNK = 1024  # Number of frames per buffer
# Device index for "Missaggio stereo (Realtek HD Audio Stereo input)"
DEVICE_INDEX = 12


def audio_callback(indata, frames, time, status):
    global mainBuffer
    if status:
        print(status)
    # Calculate the RMS value of the audio signal
    volume_norm = np.linalg.norm(indata) * 10
    print(f"Volume: {volume_norm:.2f}")
    mainBuffer.add(volume_norm)


# Start the audio stream
with sd.InputStream(samplerate=RATE, channels=CHANNELS, device=DEVICE_INDEX, callback=audio_callback, blocksize=CHUNK):
    print("Streaming... Press Ctrl+C to stop.")
    while True:
        try:
            # Keep the script running
            sd.sleep(2)  # Stream for an hour, adjust as needed
        except KeyboardInterrupt:
            print("Stream stopped by user.")
            break
