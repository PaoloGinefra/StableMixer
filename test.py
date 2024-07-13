import pyaudio
import numpy as np
import matplotlib.pyplot as plt


class Buffer:
    def __init__(self, size) -> None:
        self.size = size
        self.buffer = np.zeros(size)
        self.index = 0
        self.fig, self.ax = plt.subplots()
        plt.plot()

    def add(self, value):
        self.buffer[self.index] = value
        self.index = (self.index + 1) % self.size

    def getBuffer(self):
        return np.concatenate([self.buffer[self.index:], self.buffer[:self.index]])

    def plot(self):
        self.ax.clear()
        self.ax.plot(self.getBuffer())

        plt.pause(0.01)


# Constants
CHUNK = 1024 * 3  # Number of samples per chunk
FORMAT = pyaudio.paInt16  # Audio format (16-bit)
CHANNELS = 1  # Number of audio channels
RATE = 44100  # Sample rate (44.1kHz)


def calculate_rms(block):
    """Calculate the Root Mean Square (RMS) of a block of audio data."""
    rms = np.sqrt(np.mean(np.square(block)))
    return rms


def main():
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording...")

    mainBuffer = Buffer(250)

    try:
        while True:
            # Read data from the stream
            data = stream.read(CHUNK)
            # Convert data to numpy array
            audio_data = np.frombuffer(data, dtype=np.int16)
            # Calculate RMS volume
            rms = calculate_rms(audio_data)
            print(f"RMS Volume: {rms}")

            mainBuffer.add(rms)
            mainBuffer.plot()

    except KeyboardInterrupt:
        print("Stopped Recording")

    finally:
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        # Terminate PyAudio
        p.terminate()


if __name__ == "__main__":
    main()
