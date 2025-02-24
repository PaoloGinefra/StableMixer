from .Observer import Observer
from .VolumeSetter import VolumeSetterInterface
from .VolumeSetterWindows import VolumeSetterWindows
from .VolumeListener import VolumeListener
from .VolumeListenerWindows import VolumeListenerWindows
from .Buffer import Buffer
from .PID import PID
from .GUI.GUI import GUI
import time


class Pipeline(Observer):
    def __init__(self, targetVolume: float = 5, bufferSize: int = 1000) -> None:
        super().__init__()
        self.PID: PID = PID(0.001, 0, 0, 10)
        self.volumeSetter: VolumeSetterInterface = VolumeSetterWindows()
        self.volumeListener: VolumeListener = VolumeListenerWindows()
        self.buffer = Buffer(bufferSize)
        self.gui = GUI(self)
        self.targetVolume: float = targetVolume
        self.lastTime: float = time.time()
        self.runPipeline = True
        self.lastVolume = 0

        self.volumeListener.attach(self)

    def update(self, volume: float) -> None:
        self.buffer.add(volume)

        # if (self.lastVolume != self.volumeSetter.getVolume()):
        #     self.targetVolume += (self.volumeSetter.getVolume() -
        #                           self.lastVolume) * 10
        #     print("Volume changed to: ", self.targetVolume)

        if not self.runPipeline:
            return

        dt = self.lastTime - time.time()

        control = self.PID.getControl(self.targetVolume, volume, dt)

        newVolume = self.volumeSetter.getVolume() + control
        newVolume = min(max(0, newVolume), 1)

        self.volumeSetter.setVolume(newVolume)
        self.lastVolume = newVolume

    def setTargetVolume(self, targetVolume: float) -> None:
        self.targetVolume = targetVolume

    def getTargetVolume(self) -> float:
        return self.targetVolume

    def setPIDParameters(self, P: float = None, I: float = None, D: float = None, maxI: float = None) -> None:
        self.PID = PID(P, I, D, maxI)

    def setTargetDeciveIndex(self, index: int) -> None:
        self.volumeListener.setTargetDeviceIndex(index)

    def getAvailableDevices(self) -> list:
        return self.volumeListener.getAvailableDevices()

    def getBuffer(self) -> float:
        return self.buffer.getBuffer()

    def start(self) -> None:
        self.volumeListener.run()
        self.gui.run()

        # When the GUI is closed, stop the listener
        self.volumeListener.stop()
        pass

    def setPipelineRunning(self, running: bool) -> None:
        self.runPipeline = running
        pass

    def isRunning(self) -> bool:
        return self.runPipeline
