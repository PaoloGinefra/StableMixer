class VolumeSetterInterface:
    '''Interface for volume handler classes.'''

    def setVolume(self, volume: float) -> None:
        """Set the volume to the given value.

        Args:
            volume (float): The volume value, from 0.0 to 1.0.
        """
        pass

    def getVolume(self) -> float:
        """Get the current volume.

        Returns:
            float: The current volume value, from 0.0 to 1.0.
        """
        pass

    def mute(self) -> None:
        """Mute the volume."""
        pass

    def unmute(self) -> None:
        """Unmute the volume."""
        pass

    def isMuted(self) -> bool:
        """Check if the volume is muted.

        Returns:
            bool: Whether the volume is muted or not.
        """
        pass
