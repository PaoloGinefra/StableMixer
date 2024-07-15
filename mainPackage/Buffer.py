import numpy as np


class Buffer:
    def __init__(self, size, smoothingWindowSize: int = 1) -> None:
        self.size = size
        self.buffer = np.zeros(size)
        self.index = 0
        self.smoothingWindowSize = smoothingWindowSize

    def add(self, value):
        self.buffer[self.index] = value
        self.index = (self.index + 1) % self.size

    def get(self):
        return self.buffer[self.index - 1]

    def getBuffer(self):
        return np.concatenate([self.buffer[self.index:], self.buffer[:self.index]])

    def getSmoothBuffer(self):
        window = self.smoothingWindowSize
        return np.convolve(self.getBuffer(), np.ones(window) / window, mode='same')[window // 2:-window // 2]
