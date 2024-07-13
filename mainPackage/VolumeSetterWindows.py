from .VolumeSetter import VolumeSetterInterface
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER


class VolumeSetterWindows(VolumeSetterInterface):
    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))

    def setVolume(self, volume):
        self.volume.SetMasterVolumeLevelScalar(volume, None)

    def getVolume(self):
        return self.volume.GetMasterVolumeLevelScalar()

    def mute(self):
        self.volume.SetMute(1, None)

    def unmute(self):
        self.volume.SetMute(0, None)

    def isMuted(self):
        return self.volume.GetMute()
