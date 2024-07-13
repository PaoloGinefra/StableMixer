from .Listened import Listened


class PcOutputHandler(Listened):
    def __init__(self) -> None:
        super().__init__()

    def handleNewOutput(self, output):
        self.notifyListeners(output)
