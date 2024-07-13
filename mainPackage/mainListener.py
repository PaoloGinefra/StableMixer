from .Listener import Listener
from .VolumeSetter import VolumeSetterInterface
from .VolumeSetterWindows import VolumeSetterWindows
from .PID import PID
import time


class MainListener(Listener):
    def __init__(self, targetVolume: float = 5) -> None:
        super().__init__()
        self.PID: PID = PID(0.001, 0, 0, 10)
        self.volumeSetter: VolumeSetterInterface = VolumeSetterWindows()
        self.targetVolume: float = targetVolume
        self.lastTime: float = time.time()
        self.runPID = True

    def whisper(self, message) -> None:
        if not self.runPID:
            return

        currentPcOutput = float(message)
        volume = self.volumeSetter.getVolume()

        error = self.targetVolume - currentPcOutput
        dt = self.lastTime - time.time()

        control = self.PID.getControl(error, dt)

        newVolume = volume + control
        newVolume = min(max(0, newVolume), 1)

        self.volumeSetter.setVolume(newVolume)

    def setTargetVolume(self, targetVolume: float) -> None:
        self.targetVolume = targetVolume
