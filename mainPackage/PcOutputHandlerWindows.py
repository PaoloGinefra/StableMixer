from .PcOutputHandler import PcOutputHandler
import sounddevice as sd
import numpy as np
from .Buffer import Buffer


class PcOutputHandlerWindows(PcOutputHandler):
    def __init__(self, rate: int = 48000, channels: int = 2, chunk: int = 1024, deviceIndex: int = 12) -> None:
        super().__init__()
        self.rate = rate
        self.channels = channels
        self.chunk = chunk
        self.deviceIndex = deviceIndex
        self.buffer = Buffer(1000, 10)

    def handleNewOutput(self, output):
        self.notifyListeners(output)

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        volume_norm = np.linalg.norm(indata) * 10

        self.buffer.add(volume_norm)
        self.handleNewOutput(self.buffer.getSmoothBuffer()[-1])

    def run(self):
        with sd.InputStream(samplerate=self.rate, channels=self.channels, device=self.deviceIndex, callback=self.audio_callback, blocksize=self.chunk):
            print("Streaming... Press Ctrl+C to stop.")
            while True:
                try:
                    sd.sleep(2)
                    self.buffer.plotSmooth()
                except KeyboardInterrupt:
                    print("Stream stopped by user.")
                    break
