import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class Buffer:
    def __init__(self, size, window: int = 1) -> None:
        self.size = size
        self.buffer = np.zeros(size)
        self.index = 0
        self.window = window
        plt.ion()
        sns.set_theme()
        self.fig, self.ax = plt.subplots(figsize=(10, 5))

    def add(self, value):
        self.buffer[self.index] = value
        self.index = (self.index + 1) % self.size

    def getBuffer(self):
        return np.concatenate([self.buffer[self.index:], self.buffer[:self.index]])

    def getSmoothBuffer(self):
        window = self.window
        return np.convolve(self.getBuffer(), np.ones(window) / window, mode='same')[window // 2:-window // 2]

    def __plot(self, data: np.ndarray):
        self.ax.clear()
        self.ax.plot(data)
        plt.pause(0.01)

    def plot(self):
        self.__plot(self.getBuffer())

    def plotSmooth(self):
        self.__plot(self.getSmoothBuffer())
