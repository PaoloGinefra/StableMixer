from .Observed import Observed
from typing import List


class VolumeListener(Observed):
    def __init__(self, targetDeviceIndex: int = 12) -> None:
        super().__init__()
        self.__targetDeviceIndex = targetDeviceIndex

    def run(self):
        raise NotImplementedError

    def getTargetDeviceIndex(self):
        return self.__targetDeviceIndex

    def setTargetDeviceIndex(self, targetDeviceIndex: int):
        self.__targetDeviceIndex = targetDeviceIndex

    def getAvailableDevices(self) -> List[str]:
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError
