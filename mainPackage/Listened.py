from .Listener import Listener


class Listened:
    def __init__(self) -> None:
        self.__listeners: Listener = []

    def addListener(self, listener: Listener) -> None:
        self.__listeners.append(listener)

    def removeListener(self, listener: Listener) -> None:
        self.__listeners.remove(listener)

    def notifyListeners(self, message) -> None:
        for listener in self.__listeners:
            listener.whisper(message)
