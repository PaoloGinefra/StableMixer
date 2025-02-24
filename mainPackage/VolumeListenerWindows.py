from .VolumeListener import VolumeListener
import sounddevice as sd
import numpy as np
from typing import List
import threading


class VolumeListenerWindows(VolumeListener):
    def __init__(self, rate: int = 48000, channels: int = 2, chunk: int = 1024, targetDeviceIndex: int = 12) -> None:
        super().__init__(targetDeviceIndex)
        self.rate = rate
        self.channels = channels
        self.chunk = chunk
        self.isRunning = False
        self.volumeListeningThread: threading.Thread = None

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        volume_norm = np.linalg.norm(indata) * 10
        self.notify(volume_norm)

    def run(self):
        def listen():
            with sd.InputStream(samplerate=self.rate, channels=self.channels, device=self.getTargetDeviceIndex(), callback=self.audio_callback, blocksize=self.chunk):
                while self.isRunning:
                    try:
                        sd.sleep(100)
                    except KeyboardInterrupt:
                        print("Stream stopped by user.")
                        break

        self.isRunning = True
        self.volumeListeningThread = threading.Thread(target=listen)
        self.volumeListeningThread.start()

    def getAvailableDevices(self) -> List[str]:
        # convert to string list
        deviceList = []
        for device in sd.query_devices():
            deviceList.append(str(device['name']))
        return deviceList

    def stop(self):
        self.isRunning = False
        self.volumeListeningThread.join()
        sd.stop()
